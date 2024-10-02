# -*- coding: utf-8 -*-
import logging
from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError

_logger = logging.getLogger(__name__)


class ProductCategory(models.Model):
    _inherit = "product.category"

    code =  fields.Char("Category Code")
    category_code = fields.Char("Category Code")

    # @api.model_create_multi
    # def create(self, vals_list):
    #     for val in vals_list :
    #         if not val['parent_id'] :
    #             val['category_code'] = self.env['ir.sequence'].next_by_code('product.category.sequence')
            
    #     category = super().create(vals_list)  
    #     return category

    @api.onchange('parent_id','code')
    def onchange_parent_id(self):
        self.category_code = self.code
        if self.parent_id :
            self.category_code = self.parent_id.category_code + '-' + self.category_code
            
class ProductTemplate(models.Model):
    _inherit = "product.template"

    product_code = fields.Char("Code")

class Product(models.Model):
    _inherit = "product.product"

    @api.onchange('categ_id')
    def onchange_categ_id(self):
        if self.categ_id :
            product_id = self.search([('categ_id', '=', self.categ_id.id),('id', '!=', self._origin.id),('default_code', '!=', False)], order="id DESC", limit=1)
            if product_id.default_code : 
                last_code = product_id.default_code.split("-")
                code = int(last_code[-1]) + 1
            else :
                code = 1
            if self.categ_id.category_code :
                self.default_code = self.categ_id.category_code + '-' + str(code)

class code(models.TransientModel):
    _name = 'product.code'
    categ_id = fields.Many2one('product.category')


    def change(self) :
        if self.categ_id :
            products = self.env['product.product'].search([('categ_id', '=', self.categ_id.id)])
            for line in products :
                code = 1
                variant_code = ''
                for variant in line.product_template_variant_value_ids :
                    _logger.info("variant>>>>>>>>>>>>>1..%s",variant_code)
                    variant_code += '-' + variant.name
                    
                line.default_code  = self.categ_id.category_code + '-' + str(code) + variant_code
                _logger.info("variant>>>>>>>>>>>>>..2 %s",code)
                code +=1

