# 1 : imports of python lib

import calendar
from datetime import datetime, date,time
from dateutil.relativedelta import *
import itertools
import logging
from psycopg2 import OperationalError
import re

# 2 :  imports of odoo
from odoo import models, fields, api, exceptions
from openerp import SUPERUSER_ID
import openerp
import openerp.addons.decimal_precision as dp
from openerp.tools import float_compare, float_is_zero
from openerp.exceptions import ValidationError
from openerp import tools

_logger = logging.getLogger(__name__)


class Employee(models.Model):
    """Extend HR Employee to accommodate Indonesian Workforce.
    1. KHL is Daily PKWT.
    2. KHT is Daily PKWTT.
    3. Employee or Staf is Monthly PKWTT.
    4. Contract is Monthly PKWT.
    """
    _inherit = 'hr.employee'

    # Employee Information
    nik_number = fields.Char("Employee Identity Number", track_visibility="onchange")
    health_insurance_number = fields.Char("Health Insurance Number")
    npwp_number = fields.Char("NPWP Number")
    company_id = fields.Many2one('res.company', "Company", track_visibility="onchange")
    contract_type = fields.Selection([('1', 'PKWTT'), ('2', 'PKWT')], "Contract Type",
                                       help="* PKWTT, Perjanjian Kerja Waktu Tidak Tertentu, "\
                                            "* PKWT, Perjanjian Kerja Waktu Tertentu.", track_visibility="onchange")
    contract_period = fields.Selection([('1', 'Monthly'), ('2', 'Daily')], "Contract Period",
                                       help="* Monthly, Karyawan Bulanan, "\
                                            "* Daily, Karyawan Harian.", track_visibility="onchange")
    outsource = fields.Boolean("Outsource employee", help="Activate to represent employee as Outsource.")
    internship = fields.Boolean("Internship", help="Activate to represent internship employee.")
    age = fields.Float("Employee Age", compute='_compute_age')
    joindate = fields.Date("Date of Join")
    religion_id = fields.Many2one('nievecus_hr_indonesia.religion', "Religion")
    ethnic_id = fields.Many2one('nievecus_hr_indonesia.ethnic', "Ethnic")
    tax_marital_id = fields.Many2one('nievecus_hr_indonesia.tax_marital', 'Tax Marital')
    tax_dependent = fields.Integer('Dependent')
    location_id = fields.Many2one('nievecus_hr_indonesia.location', 'Placement Location')
    office_level_id = fields.Many2one('nievecus_hr_indonesia.office', 'Office Level')
    supervisor_level_id = fields.Many2one('nievecus_hr_indonesia.supervisor', 'Supervisor Level')


    def _compute_age(self):
        for record in self:
            record.age = 1


class Religion(models.Model):
    """ Required to define THR allowance """
    _name = 'nievecus_hr_indonesia.religion'
    _description = 'Religion'

    name = fields.Char("Religion")
    sequence = fields.Integer('Sequence')


class Ethnic(models.Model):
    _name = 'nievecus_hr_indonesia.ethnic'
    _description = 'Ethnic'

    name = fields.Char('Ethnic')
    sequence = fields.Integer('Sequence')


class TaxMarital(models.Model):
    _name = 'nievecus_hr_indonesia.tax_marital'
    _description = 'Tax Marital'

    name = fields.Char('Tax Marital')
    code = fields.Char('Code', help='Displayed at report.')
    sequence = fields.Integer('Sequence')


class Location(models.Model):
    """ Do not used stock location.
    """
    _name = 'nievecus_hr_indonesia.location'
    _parent_store = True
    _parent_name = 'parent_id'
    _order = 'complete_name'
    _rec_name = 'name'  # complete_name too long for upkeep entry

    _description = 'Placement Location'

    name = fields.Char('Location Name', required=True)
    complete_name = fields.Char("Complete Name", compute="_complete_name", store=True)
    code = fields.Char('Code', help='Write location abbreviation')
    type = fields.Selection([('view', "View"),
                             ('normal', "Normal")], "Type",
                            required=True,
                            help="Select View to create group of location.")
    comment = fields.Text("Additional Information")
    sequence = fields.Integer("Sequence", help="Keep location in order.") # todo set as parent_left at create
    parent_id = fields.Many2one('nievecus_hr_indonesia.location', "Parent Category", ondelete='restrict')
    parent_left = fields.Integer("Parent Left",	index=True)
    parent_right = fields.Integer("Parent Right", index=True)
    child_ids = fields.One2many('nievecus_hr_indonesia.location', 'parent_id', "Child Locations")

    @api.multi
    @api.depends('name', 'parent_id')
    def _complete_name(self):
        """ Forms complete name of location from parent category to child category.
        """
        for record in self:
            if record.parent_id:
                record.complete_name = record.parent_id.complete_name + ' / ' + record.name
            else:
                record.complete_name = record.name


class Office(models.Model):
    """ Hierarchy of office - required by purchase"""
    _name = 'nievecus_hr_indonesia.office'
    _parent_store = True
    _parent_name = 'parent_id'
    _order = 'sequence'
    _description = 'Office Level'

    name = fields.Char('Name', required=True)
    code = fields.Char('Code', help='Write office level')
    comment = fields.Text("Additional Information")
    sequence = fields.Integer("Sequence", help="Small number higher position.")
    parent_id = fields.Many2one('nievecus_hr_indonesia.office', "Parent Office", ondelete='restrict')
    parent_left = fields.Integer("Parent Left", index=True)
    parent_right = fields.Integer("Parent Right", index=True)
    child_ids = fields.One2many('nievecus_hr_indonesia.office', 'parent_id', "Child Office Levels")


class SupervisorLevel(models.Model):
    """ Class of position such as Division Manager and Section Chief"""

    _name = 'nievecus_hr_indonesia.supervisor'
    _parent_store = True
    _parent_name = 'parent_id'
    _order = 'sequence'

    _description = 'Supervisor Level'

    name = fields.Char('Name', required=True)
    code = fields.Char('Code', help='Write supervisor level')
    comment = fields.Text("Additional Information")
    sequence = fields.Integer("Sequence", help="Small number higher position.")
    parent_id = fields.Many2one('nievecus_hr_indonesia.supervisor', "Parent Supervisor", ondelete='restrict')
    parent_left = fields.Integer("Parent Left", index=True)
    parent_right = fields.Integer("Parent Right", index=True)
    child_ids = fields.One2many('nievecus_hr_indonesia.supervisor', 'parent_id', "Child Supervisor Levels")

    @api.constrains('code')
    def _check_code(self):
        """Code max 3"""
        if self.code:
            if len(self.code) > 3:
                msg_error = _('Supervisor level code should be 3 character long or less.')
                raise ValidationError(msg_error)
        else:
            return True
