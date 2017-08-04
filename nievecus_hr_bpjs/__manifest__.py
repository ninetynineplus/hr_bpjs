# -*- coding: utf-8 -*-
{
    'name': "HR BPJS",

    'summary': """
        Module to provide BPJS in indonesia""",

    'description': """
       Add all information on the employee form to manage BPJS.
        =============================================================
        
            * BPJS
        
        You can assign several BPJS per employee.
    """,

    'author': "Ninetynine Plus",
    'website': "http://www.ninetynine-plus.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full listre
    'category': 'Human Resource',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','hr_contract'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/nievecus_hr_form_bpjs_view.xml',
        'views/nievecus_hr_general_bpjs_view.xml',
        'views/inherit_hr_view.xml',
        'views/nievecus_hr_generate_bpjs_view.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/hr_general_bpjs.xml',
    ],
}