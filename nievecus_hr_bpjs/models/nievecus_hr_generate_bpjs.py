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
from openerp.tools import (drop_view_if_exists)

from openerp.exceptions import ValidationError, RedirectWarning

_logger = logging.getLogger(__name__)

class HrGenerateBpjs(models.Model):

    _name = 'hr.generate.employee.bpjs'
    _rec_name = 'name'
    _description = "this module to provide generate bpjs indonesia"

    name = fields.Date('Date Generate',store=True)
    hr_employee_id = fields.Many2one('hr.employee', 'Employee',store=True)
    hr_employee_general_bpjs_id = fields.Many2one('hr.employee.general.bpjs', 'BPJS',domain=[('type','=','normal')],store=True)

    def create_bpjs(self,record,employee,date):
        """
        this method to create bpjs
        :param record:
        :param employee:
        :param date:
        :return: result
        """

        count_bpjs_id = len(self._get_listof_bpjs_employee())

        bpjs_data = {
            'employee_id': employee.id,
            'bpjs_id': self._get_listof_bpjs_employee()[0] if count_bpjs_id > 0 else record.id,
            'period_start': date,
            'registered_date': date
        }

        result = self.env['hr.employee.form.bpjs'].create(bpjs_data)
        return result

    @api.multi
    def generate_all_employee_bpjs(self):
        """
        this method use to generate all employee bpjs based on employee and date
        :return:
        """

        for list_employee in self:
            date = fields.Date.context_today(list_employee)
            bpjs_data = {
                'employee_id': list_employee.hr_employee_id.id,
                'bpjs_id':list_employee.hr_employee_general_bpjs_id.id,
                'period_start': date,
                'registered_date': list_employee.name
            }

            result = self.env['hr.employee.form.bpjs'].create(bpjs_data)

            # date = fields.Date.context_today(list_employee)
            # employee = list_employee.hr_employee_id.id
            # record = employee.hr_employee_general_bpjs_id.id
            #
            # employee.create_bpjs(record, employee, date)

    @api.model
    def create(self, data):
        vehicle = super(HrGenerateBpjs).create(data)
        self.generate_all_employee_bpjs()
        return vehicle










