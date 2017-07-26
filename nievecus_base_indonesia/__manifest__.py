# -*- coding: utf-8 -*-
{
    'name': "Base Indonesia",

    'summary': """
        Module base for indonesian country""",

    'description': """
        Base Indonesia
    """,

    'author': "Arya and Mahroza",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Base',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/inherit_res_country_state_view.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/res.country.state.csv',
    ],
}