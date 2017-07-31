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

class PubliserMedical(models.Model):

    _name = 'nievecus_hr.publisher.medical'
    _inherits = {'res.partner': 'partner_id'}

    partner_id = fields.Many2one('res.partner', 'Partner id')
    is_company = fields.Boolean('Company', defaults=True)

class NievecusFormMedical(models.Model):

    @api.model
    def _get_default_requested_by(self):
        return self.env['res.users'].browse(self.env.uid)

    _name = 'nievecus.form.medical'
    _description = 'This module provide to registered medical employee'

    name = fields.Char('Medical Form Name')
    employee_id = fields.Many2one('hr.employee')
    created_by = fields.Many2one('res.user', default=_get_default_requested_by)
    department_id = fields.Many2one('hr.department', 'Department Employee', related='employee_id.department_id')
    job_id = fields.Many2one('hr.job', 'Jobs Employee', related='employee_id.job_id')
    date_record = fields.Date('Date Record Medical')
    publisher_medical = fields.Many2one('nievecus_hr.publisher.medical','Publisher')
    age_employee = fields.Integer('Employee Age')
    employee_blood = fields.Char('Employee Blood')
    employee_cholesterol_HDL = fields.Char('Employee Cholesterol HDL ')
    employee_cholesterol_LDL = fields.Char('Employee Cholesterol LDL ')
    employee_cholesterol_VLDL = fields.Char('Employee Cholesterol VLDL ')
    employee_glukose = fields.Char('Employee Glukosa')
    employee_uric_acid = fields.Char('Employee Uric Acid')
    employee_blood_presure = fields.Char('Employee Blood Presure')
    height_employee = fields.Float('Employee Height')
    weight_employee = fields.Float('Employee Weight')
