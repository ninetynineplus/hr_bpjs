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

class InheritHrContract(models.Model):

    _inherit = 'hr.contract'

    allowance_ids = fields.One2many('hr.employee.form.allowance','contract_id','Employee Allowance')
    takehomepay = fields.Float('Employee Take Home Pay',compute='_compute_takehomepay')

    @api.multi
    def get_total_allowance(self):
        """Thie method use to get total value from allowance list
            @:return allowance_total
        """
        for contract in self:

            allowance_total = float(sum(allowance.value for allowance in contract.allowance_ids))

            return allowance_total

    @api.multi
    @api.depends('wage','allowance_ids')
    def _compute_takehomepay(self):

        """This method use to calculate take home pay for employee
            @params: wage, allowance_ids
        """

        for contract in self:
            wage = contract.wage

            try:
                allowance = contract.get_total_allowance()
            except:
                allowance = 0

            thp = wage + allowance

            contract.takehomepay = thp