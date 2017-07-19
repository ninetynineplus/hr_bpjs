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

class HrEmployeeAllowanceRegister(models.Model):

    _name = 'hr.employee.allowance.register'
    _rec_name = 'employee_id'



    employee_id = fields.Many2one('hr.employee','Employee')
    allowance_ids = fields.Many2many('hr.employee.general.allowance',
                                     'employee_allowance_rel','employee_id','allowance_id',string='List Of BPJS',
                                     domain=[('type','=','normal')])

    # @api.multi
    # def create_purchase_requisition(self):
    #     # Create Contract
    #     for contract in self:
    #         date = fields.Date.context_today(contract)
    #         contrac_data = {
    #             'employee_id': contract.employee_id.id,
    #             'wage': 0,
    #             'date_start': date,
    #             'origin': purchase.complete_name,
    #             'request_id': purchase.id,
    #             'ordering_date': datetime.today(),
    #             'owner_id': purchase.id
    #         }
    #         res = self.env['purchase.requisition'].create(purchase_data)
    #
    #     for purchaseline in self.env['purchase.request.line'].search([('request_id.id', '=', self.id)]):
    #         purchaseline_data = {
    #             'product_id': purchaseline.product_id.id,
    #             'est_price': purchaseline.price_per_product,
    #             'product_uom_id': purchaseline.product_uom_id.id,
    #             'product_qty': purchaseline.product_qty if purchaseline.control_unit == 0 else purchaseline.control_unit,
    #             'requisition_id': res.id,
    #             'owner_id': res.owner_id
    #         }
    #         self.env['purchase.requisition.line'].create(purchaseline_data)
    #
    #     return True

class HrEmployeeAllowanceForm(models.Model):

    @api.multi
    def get_allowance_id_type(self):
        """Get type of allowance
            :return allowance_type
        """
        for item in self:

            allowance_type = item.allowance_id.type_allowance

            return allowance_type

    _name = 'hr.employee.form.allowance'
    _description = "this module to provide allowance indonesia"

    allowance_id = fields.Many2one('hr.employee.general.allowance','Employee Allowance',domain=[('type','=','normal')])
    contract_id = fields.Many2one('hr.contract','Employee Contract')
    employee_id = fields.Many2one('hr.employee','Employee',related='contract_id.employee_id')
    attendance_type = fields.Selection([('att','Attendance'),('natt','Not Attendance')],string='Attendance')
    type = fields.Selection([('fix','Fix Rate'),('nfix','Not Fix')],string='Type')
    type_allowance = fields.Boolean('Type Allowance',compute='onchange_allowance_type',store=True)
    value_attendance_day = fields.Float('Attendance Day')
    value_rate_day = fields.Integer('Day Value')
    value_price = fields.Float('Price')
    value = fields.Float('Value of Allowance',compute='_compute_value',store=True)

    @api.multi
    @api.depends('allowance_id')
    def onchange_allowance_type(self):
        """Change allowance type"""
        for item in self:

            if item.get_allowance_id_type() == True:
                item.type_allowance = True
            else:
                item.type_allowance = False

    @api.multi
    @api.depends('value_price','value_rate_day','value_attendance_day')
    def _compute_value(self):
        """this method use to compute value allowance"""
        for item in self:

            if item.type_allowance == True:
                if item.attendance_type == 'att':
                    if item.type == 'nfix':
                        item.value = item.value_attendance_day * item.value_price
                    else:
                        item.value = item.value_rate_day * item.value_price
                else:
                    item.value = item.value_price
            else:
                item.value = item.value_price



