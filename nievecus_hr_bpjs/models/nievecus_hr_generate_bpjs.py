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

    name = fields.Char('Name Generate',store=True)
    date_generate = fields.Date('Date Generate',store=True)
    generate_line_ids = fields.One2many('hr.generate.employee.bpjs.line','generate_id','Bpjs line')

    @api.multi
    def get_list_employee_id(self):
        """
        this method use to get employee id from generate_line_ids
        :return: arrEmployee
        """
        for record in self:

            arrEmployee=[]

            #search employee
            for employee in record.generate_line_ids:
                arrEmployee.append(employee.employee_id.id)

            return arrEmployee

    @api.multi
    def get_employee_list_last_contract(self):
        """
        this method use to get employee in generate_line_ids last contract
        :return: arrLastContract
        """
        EmployeeContract = self.env['hr.contract']
        for employee in self:
            arrLastContract = []
            for record in employee.generate_line_ids:
                arrLastContract.append(record.get_employee_last_contract())
            return arrLastContract

    @api.multi
    def get_employee_list_of_bpjs(self,generate,employee):
        """
            this method use to get list of bpjs in generate_line_ids
        :return:
        """
        for record in self:
            arrBPJS = []
            record.env.cr.execute('select '
                                  'generate_id, '
                                  'id as line_id , '
                                  'employee_id , '
                                  'rel_bpjs.hr_employee_general_bpjs_id bpjs_id '
                                  'from hr_generate_employee_bpjs_line hgebl '
                                  'inner join '
                                  '(select * from rel_general_bpjs)rel_bpjs '
                                  'on hgebl.id = rel_bpjs.hr_generate_employee_bpjs_line_id '
                                  'where generate_id = %d and employee_id = %d' %(generate,employee))
            res = record.env.cr.dictfetchall()

            for list_dict in res:
                arrBPJS.append(list_dict.get('bpjs_id'))
            print 'bisa'
            print arrBPJS
            return res

    @api.multi
    def get_list_of_general_bpjs(self,generate):
        for record in self:
            """This method to get list of bpjs from hr_employee_form_bpjs mapping to rel_general_bpjs"""
            arrBPJS = []
            record.env.cr.execute('select employee_id,bpjs_id from hr_employee_form_bpjs '
                                  'where bpjs_id in '
                                  '(select hr_employee_general_bpjs_id bpjs_id from rel_general_bpjs '
                                  'where hr_generate_employee_bpjs_line_id in (select id line_id '
                                  'from hr_generate_employee_bpjs_line where generate_id = %d)) '
                                  'and employee_id in '
                                  '( select employee_id from hr_generate_employee_bpjs_line where generate_id = %d)'
                                  % (generate, generate))

            res = record.env.cr.dictfetchall()

            for list_dict in res:
                arrBPJS.append(list_dict.get('bpjs_id'))

            return res

    @api.multi
    def _get_listof_bpjs_employee(self,):
        """
            Get list of new general bpjs employee
        :return: bpjs_id
        """

        for item in self:
            generate = item.id
            arrLineBpjs = []
            arrFormBpjs = []
            arrRes = []
            for record in self.generate_line_ids:
                employee = record.employee_id.id
                for employee_line_list in item.get_employee_list_of_bpjs(generate,employee):
                    emp = employee_line_list.get('employee_id')

                    if employee == emp:
                        arrLineBpjs.append(employee_line_list.get('bpjs_id'))

                for employee_form_list in item.get_list_of_general_bpjs(generate):
                    emp = employee_form_list.get('employee_id')

                    if employee == emp:
                        arrFormBpjs.append(employee_form_list.get('bpjs_id'))

                setRes = set(arrFormBpjs).difference(set(arrLineBpjs))
                print 'hasil'
                print setRes
                result = arrRes.append(list(setRes))

                print 'test'
                print item.get_employee_list_of_bpjs(generate,employee)
                print 'bpjs'
                print item.get_list_of_general_bpjs(generate)
                print 'hasil'
                print arrFormBpjs
                print arrLineBpjs
                print result
            # set_bpjs_id = set(self.get_list_of_general_bpjs()) - set(self.get_employee_list_of_bpjs())
            # bpjs_id = list(set_bpjs_id)

                return self.get_employee_list_of_bpjs(generate,employee)

    @api.multi
    def get_count_contract_employee(self):
        """
            this method use to get count contract employee from generate_line_ids
        :return: record.env.cr.dictfetchall()
        """
        for record in self:
            record.env.cr.execute('select '
                                  'generate_id, employee_id emp_id , contract_count '
                                  'from hr_generate_employee_bpjs_line hgebl inner join ('
                                  'select emp_id , count(cont_id) contract_count from ('
                                  'select '
                                  'hre.id emp_id , hrc.id cont_id '
                                  'from hr_employee hre left join (select * from hr_contract)'
                                  'hrc on hre.id = hrc.employee_id)'
                                  'hre_hrc group by emp_id order by emp_id asc)count_emp '
                                  'on hgebl.employee_id = count_emp.emp_id where generate_id = %d' % (record.id))
            return record.env.cr.dictfetchall()

    @api.multi
    def get_employee_not_have_contract(self):
        """
            this method use to get employee have no contract
        :return: employee_list
        """
        for item in self:
            employee_list = []
            item.env.cr.execute('select name_related, bpjs_count '
                                'from hr_generate_employee_bpjs_line hgebl '
                                'inner join (select emp_id , name_related,count(cont_id) bpjs_count from '
                                '(select hre.id emp_id , hre.name_related,hrc.id cont_id from hr_employee hre '
                                'left join (select  id,employee_id from hr_contract)hrc on hre.id = hrc.employee_id'
                                ')hre_hrc group by emp_id,name_related order by emp_id asc)count_emp '
                                'on hgebl.employee_id = count_emp.emp_id '
                                'where generate_id = %d and bpjs_count <= 0' % (item.id))
            result = item.env.cr.dictfetchall()

            for record in result:
                employee_list.append(record.get('name_related'))

            return employee_list

    @api.multi
    def create_bpjs(self, record, employee, date):
        """
        this method to create bpjs
        :param record:
        :param employee:
        :param date:
        :return: result
        """

        count_bpjs_id = len(self._get_listof_bpjs_employee())

        bpjs_data = {
            'employee_id': employee,
            'bpjs_id': record.id,
            'period_start': date,
            'registered_date': date
        }

        result = self.env['hr.employee.form.bpjs'].create(bpjs_data)
        return result

    @api.multi
    def generate_form_bpjs(self):
        """This method use to generate BPJS form"""
        #todo build generate bpjs
        len_line_ids = len(self.generate_line_ids)
        for all in self:
            print 'employee'
            print all.get_count_contract_employee()
            print all.get_list_employee_id()


            tempBpjs = []
            arrContract = []

            date = all.date_generate
            bpjs_form = self.env['hr.employee.form.bpjs']
            HrEmployee = self.env['hr.employee']

            bpjs_form_list = bpjs_form.search([
                ('employee_id', 'in', all.get_list_employee_id())])

            print bpjs_form_list
            print 'last contract'
            print all.get_employee_list_last_contract()

            # get employee last contract
            contract_employee = all.get_employee_list_last_contract()
            print 'contract employee'
            print contract_employee

            # get value of bpjs id
            # get value of contract
            for list in bpjs_form_list:
                arrContract.append(list.contract_id.id)
                tempBpjs.append(list.bpjs_id.id)

            print arrContract
            print tempBpjs
            print 'employee list bpjs'
            # print employee.get_employee_list_of_bpjs()
            print 'list general'
            # print employee.get_list_of_general_bpjs()
            print 'list result'
            print all._get_listof_bpjs_employee()

            #Check Line Generate
            if len_line_ids == 0:
                error_msg = "Please Fill Your Employee"
                raise exceptions.ValidationError(error_msg)

            #search employee contract
            list_no_contrct = ','.join(all.get_employee_not_have_contract())
            for contract in all.get_count_contract_employee():
                contract_count = contract.get('contract_count')
                emp_id = contract.get('emp_id')
                if contract_count == 0:
                    error_msg = "Employee cannot generate BPJS cause," + list_no_contrct + " have no contract"
                    raise exceptions.ValidationError(error_msg)
            # raise exceptions.ValidationError('lala')
            # count of list bpjs employee
            # count_bpjs_id = len(self._get_listof_bpjs_employee())

            # Create bpjs
            for generate_line in all.generate_line_ids:
                employee = generate_line.employee_id.id
                for record in generate_line.hr_employee_general_bpjs_ids:
                    all.create_bpjs(record, employee, date)
            #
            # if len(employee.get_list_of_general_bpjs()) == 0:
            #     error_msg = "Employee cannot generate BPJS cause, %s No one selected bpjs " % employee.name
            #     raise exceptions.ValidationError(error_msg)
            #
            # for record in employee.bpjs_rel_ids:
            #
            #     if contract_employee in arrContract and count_bpjs_id == 0:
            #         error_msg = "Employee cannot generate BPJS cause, BPJS for this %s is up to date" % employee.name
            #         raise exceptions.ValidationError(error_msg)
            #
            #     elif contract_employee not in arrContract:
            #         employee.create_bpjs(record, employee, date)
            #
            #     elif record.id not in tempBpjs and contract_employee in arrContract:
            #         employee.create_bpjs(record, employee, date)

        return True

    @api.multi
    @api.constrains('line_ids')
    def _constraint_product_line_not_null(self):
        len_line_ids = len(self.generate_line_ids)
        for item in self:
            if len_line_ids == 0:
                error_msg = "Please Fill Your Employee"
                raise exceptions.ValidationError(error_msg)

class HrGenerateBpjsLine(models.Model):

    @api.multi
    def get_employee_last_contract(self):
        """
        this method use to get employee last contract
        :return: contract_id
        """
        EmployeeContract = self.env['hr.contract']
        for employee in self:
            employee_contract = EmployeeContract.search([('employee_id', '=', employee.employee_id.id)],
                                                        limit=1,
                                                        order='id desc')

            if employee_contract:
                contract_id = employee_contract.id
            else:
                contract_id = 0

            return contract_id

    _name = 'hr.generate.employee.bpjs.line'
    _description = "this module to provide generate bpjs line indonesia"

    employee_id = fields.Many2one('hr.employee','Employee')
    generate_id = fields.Many2one('hr.generate.employee.bpjs','Generate ID')
    hr_employee_general_bpjs_ids = fields.Many2many('hr.employee.general.bpjs','rel_general_bpjs',
                                                    string='List Of BPJS',
                                    domain=[('type', '=', 'normal')])










