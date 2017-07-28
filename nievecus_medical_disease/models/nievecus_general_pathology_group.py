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


class NievecusGeneralPathologyGroup(models.Model):

    _name = 'nievecus.medical.pathology.group'
    _descriptionription = 'Nievecus Medical Pathology Group'

    name = fields.Char(required=True, translate=True)
    notes = fields.Text(translate=True)
    code = fields.Char(
        required=True, help='for example MDG6 code will contain'
                            ' the Millennium Development Goals # 6 diseases : Tuberculosis, '
                            'Malaria and HIV/AIDS')
    description = fields.Text(
        string='Short Description', required=True, translate=True)