# -*- coding:utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class HrContract(models.Model):
    """
    Employee contract based on the visa, work permits
    allows to configure different Salary structure
    """
    _inherit = 'hr.contract'
    _description = 'Employee Contract'

    hra = fields.Monetary(string='HRA', help="House rent allowance.")
    tra = fields.Monetary(string="Transportation Allowance")
    tel = fields.Monetary(string="Telephone Allowance")
    meal_allowance = fields.Monetary(string="Food Allowance")
    other_allowance = fields.Monetary(string="Other Allowance", help="Other allowances")
