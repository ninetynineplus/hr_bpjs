# -*- coding: utf-8 -*-
{
    'name': "HR Education",

    'summary': """
        Education List""",

    'description': """
        This Module to provide HR Education in indonesia
    """,

    'author': "Arya and Mahroza",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Human Resources',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','hr'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/inherit_hr_view.xml',
        'views/nievecus_hr_indonesia_education.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/nievecus_hr_indonesia.education.type.csv',
        'demo/nievecus_hr_indonesia.education.csv'

    ],
}