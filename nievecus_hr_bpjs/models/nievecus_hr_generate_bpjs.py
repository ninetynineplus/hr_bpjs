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

from openerp.exceptions import ValidationError, RedirectWarning

_logger = logging.getLogger(__name__)

class HrGenerateBpjs(models.Model):

    _name = 'hr.generate.employee.bpjs'
    _rec_name = 'name'
    _description = "this module to provide generate bpjs indonesia"

    name = fields.Char('Generate Name')
    date = fields.Date('Date Generate')

