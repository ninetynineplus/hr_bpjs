# -*- coding: utf-8 -*-
{
    'name': "HR Allowance",

    'summary': """
        This Module to provide many allowance in human resource in indonesia""",

    'description': """
        Add all information on the employee form to manage Allowance.
        =============================================================
        
            * Allowance
        
        You can assign several Allowance per employee.
    """,

    'author': "Ninetynine Plus",
    'website': "http://www.ninetynine-plus.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Human Resources',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','hr_contract'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/nievecus_hr_general_allowance_view.xml',
        'views/nievecus_hr_form_allowance_view.xml',
        'views/inherit_hr_contract.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
}