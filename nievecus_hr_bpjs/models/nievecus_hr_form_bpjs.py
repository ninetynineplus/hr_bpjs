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

class HrEmployeeBpjsForm(models.Model):

    @api.multi
    def get_bpjs_employee_contribution(self):
        for item in self:
            """this method use to get value contribution employee from bpjs_id"""

            employee_contribution = float(item.bpjs_id.contribution_employee_id.name) \
                if item.bpjs_id.contribution_employee_id.name > 0 else 0

            return employee_contribution

    @api.multi
    def get_bpjs_company_contribution(self):
        for item in self:
            """this method use to get value contribution company from bpjs_id"""

            company_contribution = float(item.bpjs_id.contribution_company_id.name) \
                if item.bpjs_id.contribution_company_id.name > 0 else 0


            return company_contribution

    @api.multi
    def get_employee_active_id(self):
        """this method to get employee id from hr.employee
            @:return employee_id
        """
        for employee in self:
            employee_id = employee.env['hr.employee'].browse(
                self._context.get('active_id'))

            return employee_id

    @api.multi
    def get_employee_contract(self):
        """
        this method use to get employee last contract
        :return: contract_id
        """
        EmployeeContract = self.env['hr.contract']
        for contract in self:
            employee_contract = EmployeeContract.search([('employee_id', '=', contract.employee_id.id)], limit=1,
                                                        order='id desc')

            if employee_contract:
                contract_id = employee_contract.id
            else:
                contract_id = 0

            return contract_id

    @api.multi
    def get_list_of_bpjs(self):
        for record in self:
            """This method to get list of bpjs from rel_bpjs"""

            record.env.cr.execute('select hr_employee_general_bpjs_id '
                                           'from rel_bpjs where hr_employee_id = %d' % (record.get_employee_active_id()))

            return [i[0] for i in record.env.cr.fetchall()]

    @api.multi
    def get_list_of_employee(self):
        for record in self:
            """This method to get list of bpjs from rel_bpjs"""

            record.env.cr.execute('select hr_employee_id '
                                  'from rel_bpjs where hr_employee_id = %d' % (record.get_employee_active_id()))

            return [i[0] for i in record.env.cr.fetchall()]


    _name = 'hr.employee.form.bpjs'
    _description = "this module to provide bpjs indonesia"


    bpjs_id = fields.Many2one('hr.employee.general.bpjs','Bpjs ID',domain=[('type','=','normal')])
    contract_id = fields.Many2one('hr.contract','Employee Contract',
                                  compute='compute_get_employee_last_contract',store=True)
    employee_id = fields.Many2one('hr.employee','Employee ID')
    company_id = fields.Many2one('res.company','Employee Company')
    job_id = fields.Many2one('hr.job','Employee Jobs',related="employee_id.job_id")
    department_id = fields.Many2one('hr.department','Employee Department',related="employee_id.department_id")
    nik_employee = fields.Char('Employee NIK')
    employee_status = fields.Char('Employee Status')
    period_start = fields.Date('Period')
    period_end = fields.Date('Period')
    generate_bpjs = fields.Boolean('Generate BPJS')
    registered_date = fields.Date('Registered BPJS')
    take_home_pay = fields.Float('Employee Take Home Pay',compute='_compute_employee_wage')
    bpjs_pay = fields.Float('Employee total contribution',compute='_compute_bpjs_pay')
    employee_contribution_value = fields.Float('Employee Contribution Value',compute='_compute_contribution_value')
    company_contribution_value = fields.Float('Company Contribution Value',compute='_compute_contribution_value')

    @api.multi
    @api.depends('employee_id')
    def compute_get_employee_last_contract(self):

        """onchange value contract from  employee last contract"""
        for contract in self:
            contract.contract_id = contract.get_employee_contract()


    @api.multi
    @api.depends('bpjs_id','take_home_pay')
    def _compute_contribution_value(self):

        """this method to compute contribution value for employee and company"""

        for contribution in self:
            employee_contribution = contribution.get_bpjs_employee_contribution()
            company_contribution = contribution.get_bpjs_company_contribution()
            thp = contribution.take_home_pay

            contribution.employee_contribution_value = thp * (employee_contribution / 100)
            contribution.company_contribution_value = thp * (company_contribution / 100)

    @api.multi
    @api.depends('employee_contribution_value','company_contribution_value')
    def _compute_bpjs_pay(self):

        """this method to compute total bpjs pay
        #params : employee_contribution_value and company_contribution_value"""

        for bpjs in self:

            employee_contribution = bpjs.employee_contribution_value
            company_contribution = bpjs.company_contribution_value

            bpjs.bpjs_pay = employee_contribution + company_contribution

    @api.multi
    @api.onchange('bpjs_id')
    def _onchange_bpjs_id(self):
        for bpjs in self:

            return {
                'domain': {
                    'bpjs_id': [('id', 'in', bpjs.get_list_of_bpjs()), ('type', '=', 'normal')]
                }
            }

    @api.multi
    @api.depends('take_home_pay','contract_id')
    def _compute_employee_wage(self):

        """this method to get wage from last contract active employee"""

        for item in self:

            wage = item.contract_id.wage
            try:
                employee_thp = item.contract_id.takehomepay
            except:
                employee_thp = 0

            takehomepay = wage if employee_thp == 0 else employee_thp

            item.take_home_pay = takehomepay








