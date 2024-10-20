# -*- coding:utf-8 -*-

{
    'name': 'Odoo 16 HR Payroll',
    'category': 'Generic Modules/Human Resources',
    'version': '16.0.1.0.2',
    'sequence': 1,
    'author': '',
    'summary': '',
    'description': "",
    'website': '',
    'license': 'LGPL-3',
    'depends': [
        'mail',
        'hr_contract',
        'hr_holidays',
    ],
    'data': [
        'views/hr_contract_views.xml',
    ],

    'application': True,
}
