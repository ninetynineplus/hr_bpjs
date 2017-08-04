# -*- coding: utf-8 -*-
{
    'name': "HR Indonesia",

    'summary': """
        Status, Supervisor Level, Tax, Insurance.""",

    'description': """
        This module provide process human resource in indonesia
    """,

    'author': "Ninetynine Plus",
    'website': "http://www.ninetynine-plus.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Human Resource',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','hr_contract'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/nievecus_hr_indonesia_view.xml',
        'views/supervisorlevel_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
}