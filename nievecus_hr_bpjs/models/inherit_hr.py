# 1 : imports of python lib

import calendar
from datetime import datetime, date,time
from dateutil.relativedelta import *
import itertools
import logging
from psycopg2 import OperationalError
import re

# 2 :  imports of odoo
from openerp import models, fields, api, exceptions
from openerp import SUPERUSER_ID
import openerp
import openerp.addons.decimal_precision as dp
from openerp.tools import float_compare, float_is_zero
from openerp.exceptions import ValidationError
from openerp import tools

_logger = logging.getLogger(__name__)


class InheritHrEmployee(models.Model):

    @api.multi
    def get_employee_last_contract(self):
        """
        this method use to get employee last contract
        :return: contract_id
        """
        EmployeeContract = self.env['hr.contract']
        for employee in self:
            employee_contract = EmployeeContract.search([('employee_id', '=', employee.id)], limit=1,
                                                        order='id desc')

            if employee_contract:
                contract_id = employee_contract.id
            else:
                contract_id = 0

            return contract_id

    _inherit = 'hr.employee'

    bpjs_ids = fields.One2many('hr.employee.form.bpjs','employee_id','List Of BPJS')
    bpjs_rel_ids = fields.Many2many('hr.employee.general.bpjs','rel_bpjs',string='List Of BPJS',

                                    domain=[('type', '=', 'normal')])
    bpjs_count = fields.Integer(compute='_compute_bpjs_count', string='BPJS',store=True)

    @api.multi
    def _compute_bpjs_count(self):
        # read_group as sudo, since BPJS count is displayed on form view
        contract_data = self.env['hr.employee.form.bpjs'].sudo().read_group([('employee_id', 'in', self.ids)],
                                                                            ['employee_id'], ['employee_id'])
        result = dict((data['employee_id'][0], data['employee_id_count']) for data in contract_data)
        for employee in self:
            employee.bpjs_count = result.get(employee.id, 0)

    @api.multi
    def act_show_log_bpjs(self):
        """ This opens log view to view and add new log for this employee, groupby default to only show bpjs
            @return: the bpjs log view
        """
        self.ensure_one()
        res = self.env['ir.actions.act_window'].for_xml_id('nievecus_hr_bpjs', 'hr_employee_form_bpjs_action_2')
        res.update(
            context=dict(self.env.context, default_employee_id=self.id, search_default_parent_false=True),
            domain=[('employee_id', '=', self.id)]
        )
        return res

    @api.multi
    def get_list_of_bpjs(self):
        for record in self:
            """This method to get list of bpjs from rel_bpjs"""

            record.env.cr.execute('select bpjs_id from hr_employee_form_bpjs '
                                  'where bpjs_id in '
                                  '(select hr_employee_general_bpjs_id '
                                  'from rel_bpjs where employee_id = %s)and employee_id = %s' % (record.id, record.id))

            return [i[0] for i in record.env.cr.fetchall()]

    @api.multi
    def get_list_of_general_bpjs(self):
        for record in self:
            """This method to get list of bpjs from rel_bpjs"""

            record.env.cr.execute('select hr_employee_general_bpjs_id '
                                  'from rel_bpjs where hr_employee_id = %d' % (record.id))

            return [i[0] for i in record.env.cr.fetchall()]


    def _get_listof_bpjs_employee(self):
        """
            Get list of new general bpjs employee
        :return: bpjs_id
        """
        self.ensure_one()

        set_bpjs_id = set(self.get_list_of_general_bpjs()) - set(self.get_list_of_bpjs())
        bpjs_id = list(set_bpjs_id)

        return bpjs_id

    @api.multi
    def get_count_employee_contract(self):
        """
        this method use to get count total employee  contract
        :return: count_employee_contract
        """
        EmployeeContract = self.env['hr.contract']
        for employee in self:
            employee_contract = EmployeeContract.search([('employee_id', '=', employee.id)],
                                                        order='id desc')

            count_employee_contract = len(employee_contract)

            return count_employee_contract

    @api.multi
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
    def generate_form_bpjs(self):
        """This method use to generate BPJS form"""

        for employee in self:

            tempBpjs = []
            arrContract= []

            date = fields.Date.context_today(employee)
            bpjs_form = self.env['hr.employee.form.bpjs']

            bpjs_form_list= bpjs_form.search([
                ('employee_id', '=', employee.id)])

            #get employee last contract
            contract_employee = employee.get_employee_last_contract()

            #get value of bpjs id
            #get value of contract
            for list in bpjs_form_list:
                arrContract.append(list.contract_id.id)
                tempBpjs.append(list.bpjs_id.id)

            #count of list bpjs employee
            count_bpjs_id = len(self._get_listof_bpjs_employee())

            # Create bpjs
            if employee.get_count_employee_contract() == 0 :
                error_msg = "Employee cannot generate BPJS cause, %s have no contract" % employee.name
                raise exceptions.ValidationError(error_msg)

            if len(employee.get_list_of_general_bpjs()) == 0:
                error_msg = "Employee cannot generate BPJS cause, %s No one selected bpjs " % employee.name
                raise exceptions.ValidationError(error_msg)

            for record in employee.bpjs_rel_ids:

                if contract_employee in arrContract and count_bpjs_id == 0:
                    error_msg = "Employee cannot generate BPJS cause, BPJS for this %s is up to date" % employee.name
                    raise exceptions.ValidationError(error_msg)

                elif contract_employee not in arrContract:
                    employee.create_bpjs(record,employee,date)

                elif record.id not in tempBpjs and contract_employee in arrContract:
                    employee.create_bpjs(record,employee,date)

        return True

