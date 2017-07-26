# -*- coding: utf-8 -*-
{
    'name': "HR Family",

    'summary': """
        Detail Family employee""",

    'description': """
        This Module provide detail family employee
    """,

    'author': "Arya and Mahroza",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Human Resources',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','nievecus_base_indonesia','hr'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/inherit_hr_view.xml',
        'views/nievecus_hr_indonesia_family_view.xml',
        'views/nievecus_hr_family_job_view.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
}