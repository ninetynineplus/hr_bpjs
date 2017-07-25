# -*- coding: utf-8 -*-

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


class Department(models.Model):
    """ Code required for sequence number"""
    _inherit = 'hr.department'

    code = fields.Char('Department Code', help='Capital letters 3 characters long.')

    @api.multi
    @api.constrains('code')
    def _check_code(self):
        for record in self:
            if record.code:
                if len(record.code) > 4:
                    msg_error = _('Maximum 4 characters long.')
                    raise ValueError(msg_error)