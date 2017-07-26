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

class PubliserLicense(models.Model):

    _name = 'nievecus_hr.publisher.license'
    _inherits = {'res.partner': 'partner_id'}

    partner_id = fields.Many2one('res.partner', 'Partner id')
    is_company = fields.Boolean('Company', defaults=True)

class NievecusHrDriveLicense(models.Model):

    _name = 'nievecus_hr.drive.license'
    _rec_name = 'name'
    _description = 'This class list of employee drive license'

    employee_id = fields.Many2one('hr.employee','Employee')
    name = fields.Char('License Name',related='license_id.name')
    license_id = fields.Many2one('general.driver.licence','Drive License',domain=[('type','=','normal')])
    publisher_license_id = fields.Many2one('nievecus_hr.publisher.license','Publisher')
    date_start = fields.Date('Date Start')
    date_end = fields.Date('Date End')
    no_license = fields.Char('License No')
