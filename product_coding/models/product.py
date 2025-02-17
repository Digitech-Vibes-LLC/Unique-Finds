# -*- coding: utf-8 -*-
import logging
import re
from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError

_logger = logging.getLogger(__name__)     


class ProductCategory(models.Model):
    _inherit = "product.category"

    code =  fields.Char("Category Code")
    category_code = fields.Char("Complete Code")

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
            
# class ProductTemplate(models.Model):
#     _inherit = "product.template"

#     product_code = fields.Char("Code")

class Product(models.Model):
    _inherit = "product.product"
    
    product_code = fields.Char("Code")
    
    @api.onchange('categ_id')
    def onchange_categ_id(self):
        _logger.info("variant>>>>>>>>>>>>>1..%s",self.categ_id)
        if self.categ_id :
            product_id = self.search([('categ_id', '=', self.categ_id.id),('id', '!=', self._origin.id),('default_code','!=', False)], order="product_code DESC", limit=1)
            
            if product_id : 
                code = int(product_id.product_code)+ 1
            else :
                code = 1000
            if self.categ_id.category_code :
                variant_code = ''
                for variant in self.product_template_attribute_value_ids :
                    if variant.product_attribute_value_id.code :
                        variant_code += '-' + variant.product_attribute_value_id.code
                    else :
                        variant_code += '-' + variant.name
                    
                self.default_code  = self.categ_id.category_code + '-' + str(code) + variant_code
                self.product_code = code

    @api.model_create_multi
    def create(self, vals_list):
        products = super().create(vals_list)
        for product in products :
            variant_code = ''
            product_id = self.search([('categ_id', '=', product.categ_id.id),('id', '!=', product._origin.id),('default_code', '!=', False)], order="id DESC", limit=1)
            if product_id.default_code : #attribute_line_ids
                x = re.findall(r'\d+', product_id.default_code)
                
                last_code = int(x[-1]) +1
            else :
                last_code = 1000
            for variant in product.product_template_attribute_value_ids :
                    if variant.product_attribute_value_id.code :
                        variant_code += '-' + variant.product_attribute_value_id.code
                    else :
                        variant_code += '-' + variant.name
            product.default_code  = product.categ_id.category_code + '-' + str(last_code) +  variant_code
            product.product_code = last_code
            
        return products
                
class Product(models.Model):
    _inherit = "product.template"

    @api.model_create_multi
    def create(self, vals_list):
        products = super().create(vals_list)
        for product in products :
            variant_code = ''
            product_id = self.env['product.product'].search([('categ_id', '=', product.categ_id.id),('default_code', '!=', False)], order="id DESC", limit=1)
            if product_id.default_code : #attribute_line_ids
                x = re.findall(r'\d+', product_id.default_code)
                last_code = int(x[-1])+ 1
            else :
                last_code = 1000
            if not self.attribute_line_ids :
                product.default_code  = product.categ_id.category_code + '-' + str(last_code)
        return products
        
    @api.onchange('categ_id','attribute_line_ids')
    def onchange_categ_id(self):
            variant_code = ''
            product_id = self.env['product.product'].search([('categ_id', '=', self.categ_id.id),('default_code', '!=', False)], order="id DESC", limit=1)

            if product_id.default_code : #attribute_line_ids
                x = re.findall(r'\d+', product_id.default_code)
                
                last_code = int(x[-1]) +1
            else :
                last_code = 1000
            if not self.attribute_line_ids :
                if self.categ_id.category_code :
                    self.default_code  = self.categ_id.category_code + '-' + str(last_code)
            else :
                self.default_code = None

        
#     @api.onchange('categ_id')
#     def onchange_categ_id(self):
#         _logger.info("variant>>>>>>>>>>>>>1..%s",self.categ_id)
#         if self.categ_id :
#             product_id = self.search([('categ_id', '=', self.categ_id.id),('id', '!=', self._origin.id),('default_code','!=', False)], order="product_code DESC", limit=1)
            
#             if product_id : 
#                 code = int(product_id.product_code)+ 1
#             else :
#                 code = 1000
#             if self.categ_id.category_code :
#                 variant_code = ''
#                 for variant in self.attribute_line_ids :
#                     for value in self.value-ids :
#                     #_logger.info("variant>>>>>>>>>>>>>1..%s",variant.product_attribute_value_id.name)
#                         if value.code :
#                             variant_code += '-' + value.code
#                         else :
#                             variant_code += '-' + variant.name
#                 # for variant in self.product_template_variant_value_ids :
                    
#                 #     if variant.product_attribute_value_id.code :
#                 #         variant_code += '-' + variant.product_attribute_value_id.code
#                 #     else :
#                 #         variant_code += '-' + variant.name
                    
#                 self.default_code  = self.categ_id.category_code + '-' + str(code) + variant_code
#                 _logger.info("variant>>>>>>>>>>>>>1..%s",self.default_code)
#                 self.product_code = code

class ProductAttributeValue(models.Model):
    _inherit = "product.attribute.value"
    
    code =  fields.Char("Code")

class code(models.TransientModel):
    _name = 'product.code'
    categ_id = fields.Many2one('product.category')


    def change(self) :
        products = self.env['product.product'].search([])        
        for line in products:
            if line.default_code:
                _logger.info("Product ID: %s", line)
                numbers = re.findall(r'\d+', line.default_code)

                line.product_code = None # Assign the unique product code
                
                #last_code = line.default_code.split("-")
                    
                #_logger.info("code>>>>>>>>>>>>>..2 %s",last_code[2])
    
                # if isinstance(last_code[2], int):
                #if int(last_code[2]):
                    #line.product_code = None
                #line.product_code = last_code[2]
                #_logger.info("line.product_code>>>>>>>>>>>>>..2 %s",line.product_code)
        # if self.categ_id :
        #     products = self.env['product.product'].search([('categ_id', '=', self.categ_id.id)])
        # code = 1000
        # for line in products :
        #     # _logger.info("code>>>>>>>>>>>>>..2 %s",line.default_code)
        #     # last_code = line.default_code.split("-")
        #     # line.product_code = last_code[2]
        #     variant_code = ''
        #     for variant in line.product_template_variant_value_ids :
        #         _logger.info("variant>>>>>>>>>>>>>1..%s",variant_code)
        #         if variant.product_attribute_value_id.code :
        #             variant_code += '-' + variant.product_attribute_value_id.code
        #         else :
        #             variant_code += '-' + variant.name
                
        #     line.default_code  = self.categ_id.category_code + '-' + str(code) + variant_code
        #     line.product_code = code
        #     _logger.info("code>>>>>>>>>>>>>..2 %s",code)
        #     code +=1

