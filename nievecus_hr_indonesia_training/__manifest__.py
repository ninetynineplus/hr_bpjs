# -*- coding: utf-8 -*-
{
    'name': "HR Training",

    'summary': """
        Detail Training Employee""",

    'description': """
        Detail of Human resource training Employee
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
        'views/inherited_hr.xml',
        'views/nievecus_hr_indonesia_training_view.xml',
        'views/nievecus_hr_institution_view.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
}