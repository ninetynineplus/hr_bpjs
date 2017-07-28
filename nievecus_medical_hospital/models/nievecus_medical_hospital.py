import calendar
from datetime import datetime, date, time
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

class NievecusMedicalHospital(models.Model):

    _name = 'nievecus.medical.hospital'
    _inherits = {'res.partner': 'partner_id'}

    partner_id = fields.Many2one('res.partner', 'Partner id')
    is_company = fields.Boolean('Company', default=True)
    is_hospital = fields.Boolean('Hospital',default=True)
    type_hospital = fields.Selection([('rs','RS'),
                                      ('rsu','RSU'),
                                      ('rsud','RSUD'),
                                      ('rsia','RSIA'),
                                      ('rsab','RSAB'),
                                      ('rsb','RSB'),
                                      ('rsj','RSJ'),
                                      ('rsk','RSK')])
    hospital_address = fields.Text('Hospital Address')
    hospital_state = fields.Many2one('res.country.state','Hospital State')