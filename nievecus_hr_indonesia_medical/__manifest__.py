# -*- coding: utf-8 -*-
{
    'name': "HR Employee Medical",

    'summary': """
       Employee, Medical , Disease , Form Illness""",

    'description': """
        This module 
    """,

    'author': "Arya and Mahroza",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Human Resources',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','hr','nievecus_medical_disease','nievecus_medical_hospital','nievecus_hr_indonesia'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/nievecus_form_illness_view.xml',
        'views/nievecus_form_medical_view.xml',
        'views/inherited_hr_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}