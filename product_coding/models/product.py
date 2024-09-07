# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProductCategory(models.Model):
    _inherit = "product.category"

    category_code = fields.Char("Code")

    @api.model_create_multi
    def create(self, vals_list):
        for val in vals_list :
            if not val['parent_id'] :
                val['category_code'] = self.env['ir.sequence'].next_by_code('product.category.sequence')
            
        category = super().create(vals_list)  
        return category

    @api.onchange('parent_id')
    def onchange_parent_id(self):
        if self.parent_id :
            category_id = self.search([('parent_id', '=', self.parent_id.id),('category_code', '!=', False)], order="name DESC", limit=1)
            if category_id : 
                last_code = category_id.category_code.split("-")
                code = int(last_code[-1]) + 1
            else :
                code = 1
            if self.parent_id.category_code :
                self.category_code = self.parent_id.category_code + '-' + str(code)
        else :
            category_id = self.search([('id', '<', self._origin.id)], order="id DESC", limit=1)
            if category_id :
                self.category_code = int(category_id.category_code) + 1
            else :
                self.category_code = 1

class ProductTemplate(models.Model):
    _inherit = "product.template"

    product_code = fields.Char("Code")

    @api.onchange('categ_id')
    def onchange_categ_id(self):
        print ("JJJJJJJJJJJJteeeeeeeest")
        if self.categ_id :
            product_id = self.search([('categ_id', '=', self.categ_id.id),('id', '!=', self._origin.id),('product_code', '!=', False)], order="id DESC", limit=1)
            print ("JJJJJJJJproduct_id",product_id)
            if product_id.product_code : 
                last_code = product_id.product_code.split("-")
                code = int(last_code[-1]) + 1
            else :
                code = 1
            if self.categ_id.category_code :
                self.product_code = self.categ_id.category_code + '-' + str(code)
