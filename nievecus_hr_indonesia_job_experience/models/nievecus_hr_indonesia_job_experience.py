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

class NievecusCompanyExperience(models.Model):

    _name = 'nievecus_hr.company.experience'
    _inherits = {'res.partner': 'partner_id'}

    partner_id = fields.Many2one('res.partner', 'Partner id')
    is_company = fields.Boolean('Company',defaults=True)


class NievecusHrIndonesiaJobExperience(models.Model):

    _name = 'nievecus_hr_indonesia.job.experience'
    _rec_name = 'name'
    _description = 'this module provide history of job in indonesia'

    company_name = fields.Many2one('nievecus_hr.company.experience','Company')
    name = fields.Char('Char',related='company_name.display_name')
    employee_id = fields.Many2one('hr.employee','Employee')
    address = fields.Text('Company Address')
    location = fields.Many2one('res.country.state','Location')
    date_start = fields.Date('Date Start')
    date_end = fields.Date('Date End')
    work_here = fields.Boolean('Work Here',help=" I Currently Work Here")


