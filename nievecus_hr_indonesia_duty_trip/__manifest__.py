# -*- coding: utf-8 -*-
{
    'name': "HR Duty Trip",

    'summary': """
        Duty Trip""",

    'description': """
        This module provide duty trip in indonesia
    """,

    'author': "Ninetynine Plus",
    'website': "http://www.ninetynine-plus.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Human Resources',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','nievecus_hr_allowance'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',

        'views/nievecus_hr_indonesia_duty_trip_view.xml',
        'views/inherited_hr.xml',
        'views/nievecus_hr_indonesia_duty_trip_sequence.xml',
        'views/inherited_hr_employee_general_allowance_view.xml'
        # 'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
}