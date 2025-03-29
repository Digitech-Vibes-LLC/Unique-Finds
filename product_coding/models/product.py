# -*- coding: utf-8 -*-
import logging
import re
from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError

_logger = logging.getLogger(__name__)

class ProductCategory(models.Model):
    _inherit = "product.category"

    code = fields.Char("Category Code")
    category_code = fields.Char("Complete Code")

    @api.onchange('parent_id', 'code')
    def onchange_parent_id(self):
        self.category_code = self.code
        if self.parent_id and self.parent_id.category_code:
            self.category_code = self.parent_id.category_code + '-' + self.code

class Product(models.Model):
    _inherit = "product.product"

    product_code = fields.Char("Code")

    @api.onchange('categ_id')
    def onchange_categ_id(self):
        _logger.info("variant>>>>>>>>>>>>>1..%s", self.categ_id)
        if self.categ_id:
            product_id = self.search([
                ('categ_id', '=', self.categ_id.id),
                ('id', '!=', self._origin.id),
                ('default_code', '!=', False)
            ], order="product_code DESC", limit=1)

            code = int(product_id.product_code) + 1 if product_id else 1000

            if self.categ_id.category_code:
                variant_code = ''
                for variant in self.product_template_attribute_value_ids:
                    if variant.product_attribute_value_id.code:
                        variant_code += '-' + variant.product_attribute_value_id.code
                    else:
                        variant_code += '-' + variant.name

                self.default_code = self.categ_id.category_code + '-' + str(code) + variant_code
                self.product_code = code

    @api.model_create_multi
    def create(self, vals_list):
        products = super().create(vals_list)
        for product in products:
            variant_code = ''
            last_code = 1000

            product_id = self.search([
                ('categ_id', '=', product.categ_id.id),
                ('id', '!=', product._origin.id),
                ('default_code', '!=', False)
            ], order="id DESC", limit=1)

            if product_id and product_id.default_code:
                x = re.findall(r'\d+', product_id.default_code)
                if x:
                    last_code = int(x[-1]) + 1

            for variant in product.product_template_attribute_value_ids:
                if variant.product_attribute_value_id.code:
                    variant_code += '-' + variant.product_attribute_value_id.code
                else:
                    variant_code += '-' + variant.name

            if product.categ_id and product.categ_id.category_code:
                product.default_code = product.categ_id.category_code + '-' + str(last_code) + variant_code
            else:
                product.default_code = 'GEN-' + str(last_code) + variant_code

            product.product_code = last_code

        return products

class ProductTemplate(models.Model):
    _inherit = "product.template"

    @api.model_create_multi
    def create(self, vals_list):
        products = super().create(vals_list)
        for product in products:
            last_code = 1000
            variant_code = ''

            product_id = self.env['product.product'].search([
                ('categ_id', '=', product.categ_id.id),
                ('default_code', '!=', False)
            ], order="id DESC", limit=1)

            if product_id and product_id.default_code:
                x = re.findall(r'\d+', product_id.default_code)
                if x:
                    last_code = int(x[-1]) + 1

            if not product.attribute_line_ids:
                if product.categ_id and product.categ_id.category_code:
                    product.default_code = product.categ_id.category_code + '-' + str(last_code)
                else:
                    product.default_code = 'GEN-' + str(last_code)

        return products

    @api.onchange('categ_id', 'attribute_line_ids')
    def onchange_categ_id(self):
        last_code = 1000
        variant_code = ''

        product_id = self.env['product.product'].search([
            ('categ_id', '=', self.categ_id.id),
            ('default_code', '!=', False)
        ], order="id DESC", limit=1)

        if product_id and product_id.default_code:
            x = re.findall(r'\d+', product_id.default_code)
            if x:
                last_code = int(x[-1]) + 1

        if not self.attribute_line_ids:
            if self.categ_id and self.categ_id.category_code:
                self.default_code = self.categ_id.category_code + '-' + str(last_code)
            else:
                self.default_code = 'GEN-' + str(last_code)
        else:
            self.default_code = None

class ProductAttributeValue(models.Model):
    _inherit = "product.attribute.value"

    code = fields.Char("Code")

class ProductCodeWizard(models.TransientModel):
    _name = 'product.code'

    categ_id = fields.Many2one('product.category')

    def change(self):
        products = self.env['product.product'].search([])
        for line in products:
            if line.default_code:
                _logger.info("Product ID: %s", line)
                numbers = re.findall(r'\d+', line.default_code)
                line.product_code = None  # Clean or recalculate if needed
