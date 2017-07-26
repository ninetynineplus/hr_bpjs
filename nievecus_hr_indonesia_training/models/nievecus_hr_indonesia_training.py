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

class NievecusInstiution(models.Model):

    _name = 'nievecus_hr.institution'
    _inherits = {'res.partner': 'partner_id'}

    partner_id = fields.Many2one('res.partner', 'Partner id')
    is_company = fields.Boolean('Company',defaults=True)


class NievecusHrIndonesiaJobExperience(models.Model):

    _name = 'nievecus_hr_indonesia.training'
    _rec_name = 'name'
    _description = 'this module provide history of training in indonesia'

    institution_name = fields.Many2one('nievecus_hr.institution','Institution')
    name = fields.Char('Name Training')
    employee_id = fields.Many2one('hr.employee','Employee')
    location = fields.Many2one('res.country.state','Location')
    training_detail = fields.Text('Training Detail')
    date_start = fields.Date('Date Start',store=True)
    date_end = fields.Date('Date End',store=True)
    image_certificate = fields.Binary('Upload certificate')
    certificate_name = fields.Char('certificate Name')

