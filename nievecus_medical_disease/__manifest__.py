# -*- coding: utf-8 -*-
{
    'name': "Medical Disease",

    'summary': """
       Medical , Disease""",

    'description': """
        Medical Disease
    """,

    'author': "Ninetynine Plus",
    'website': "http://www.ninetynine-plus.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Medical',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/medical_pathology_category_view.xml',
        'views/medical_pathology_group_view.xml',
        'views/medical_pathology_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}