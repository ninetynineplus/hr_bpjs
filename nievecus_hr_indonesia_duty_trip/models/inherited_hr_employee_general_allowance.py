import calendar
from datetime import datetime, date,time,timedelta as td
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

class InheritHrEmployeeGeneralAllowance(models.Model):

    _inherit = 'hr.employee.general.allowance'

    is_duty = fields.Boolean('Is Duty',help='Allowance duty ?')