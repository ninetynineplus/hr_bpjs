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

class InheritHrEmployee(models.Model):

    _inherit = 'hr.employee'

    detail_form_medical_ids = fields.One2many('nievecus.form.medical','employee_id', string='Form Medical List')
    detail_form_illness_ids = fields.One2many('nievecus.form.illness','employee_id', string='Form illness List')
    count_form_medical = fields.Integer('Count Form Medical', compute='_compute_form_medical_count')
    count_form_illness = fields.Integer('Count Form Illness', compute='_compute_form_illness_count')
    last_medical = fields.Many2one('nievecus.form.medical','Last Company',
                                       compute='compute_get_employee_form_medical',store=True)
    last_blood_type = fields.Char('Blood Type', compute='compute_get_employee_form_medical')
    last_cholesterol = fields.Char('Cholesterol', compute='compute_get_employee_form_medical')
    last_employee_blood_presure = fields.Char('Blood Presure', compute='compute_get_employee_form_medical')
    last_employee_height = fields.Float('Last Height Employee',compute='compute_get_employee_form_medical')
    last_employee_weight =  fields.Float('Last Weight Employee',compute='compute_get_employee_form_medical')

    @api.multi
    def act_show_log_form_medical(self):
        """ This opens log view to view and add new log for this employee, groupby default to only show form_medical Member
            @return: the form_medical member log view
        """
        self.ensure_one()
        res = self.env['ir.actions.act_window'].for_xml_id('nievecus_hr_indonesia_medical',
                                                           'nievecus_form_medical_record_action2')
        res.update(
            context=dict(self.env.context, default_employee_id=self.id, search_default_parent_false=True),
            domain=[('employee_id', '=', self.id)]
        )
        return res

    @api.multi
    def act_show_log_form_illness(self):
        """ This opens log view to view and add new log for this employee, groupby default to only show form_illness Member
            @return: the form_illness member log view
        """
        self.ensure_one()
        res = self.env['ir.actions.act_window'].for_xml_id('nievecus_hr_indonesia_medical',
                                                           'nievecus_form_illness_action2')
        res.update(
            context=dict(self.env.context, default_employee_id=self.id, search_default_parent_false=True),
            domain=[('employee_id', '=', self.id)]
        )
        return res

    @api.multi
    def get_employee_last_form_medical(self):
        """
        this method use to get employee last form_medical
        :return: form_medical_id
        """
        Employeeform_medical = self.env['nievecus.form.medical']
        for form_medical in self:
            employee_form_medical = Employeeform_medical.search([('employee_id', '=', form_medical.id)], limit=1,
                                                          order='date_record desc')

            if employee_form_medical:
                form_medical_id = employee_form_medical.id
            else:
                form_medical_id = 0

            return form_medical_id

    @api.multi
    def get_employee_last_blood(self):
        """
        this method use to get employee last blood
        :return: blood
        """
        Employeeform_medical = self.env['nievecus.form.medical']
        for form_medical in self:
            employee_form_medical = Employeeform_medical.search([('employee_id', '=', form_medical.id)], limit=1,
                                                                order='id desc')

            if employee_form_medical:
                blood = employee_form_medical.employee_blood
            else:
                blood = 'Not Recorded'

            return blood

    @api.multi
    def get_employee_last_cholesterol(self):
        """
        this method use to get employee last cholesterol LDL
        :return: cholesterol
        """
        Employeeform_medical = self.env['nievecus.form.medical']
        for form_medical in self:
            employee_form_medical = Employeeform_medical.search([('employee_id', '=', form_medical.id)], limit=1,
                                                                order='id desc')

            if employee_form_medical:
                cholesterol = employee_form_medical.employee_cholesterol_LDL
            else:
                cholesterol = 'Not Recorded'

            return cholesterol

    @api.multi
    def get_employee_last_employee_blood_presure(self):
        """
        this method use to get employee blood presure
        :return: blood presure
        """
        Employeeform_medical = self.env['nievecus.form.medical']
        for form_medical in self:
            employee_form_medical = Employeeform_medical.search([('employee_id', '=', form_medical.id)], limit=1,
                                                                order='id desc')

            if employee_form_medical:
                blood_presure = employee_form_medical.employee_blood_presure
            else:
                blood_presure = 'Not Recorded'

            return blood_presure

    @api.multi
    def get_employee_last_employee_height(self):
        """
        this method use to get employee height
        :return: height
        """
        Employeeform_medical = self.env['nievecus.form.medical']
        for form_medical in self:
            employee_form_medical = Employeeform_medical.search([('employee_id', '=', form_medical.id)], limit=1,
                                                                order='id desc')

            if employee_form_medical:
                height = employee_form_medical.height_employee
            else:
                height = 0.0

            return height

    @api.multi
    def get_employee_last_employee_weight(self):
        """
        this method use to get employee height
        :return: weight
        """
        Employeeform_medical = self.env['nievecus.form.medical']
        for form_medical in self:
            employee_form_medical = Employeeform_medical.search([('employee_id', '=', form_medical.id)], limit=1,
                                                                order='id desc')

            if employee_form_medical:
                weight = employee_form_medical.weight_employee
            else:
                weight = 0.0

            return weight

    @api.multi
    @api.depends('detail_form_medical_ids')
    def compute_get_employee_form_medical(self):

        """onchange value contract from  employee last form_medical"""
        for form_medical in self:
            form_medical.last_medical = form_medical.get_employee_last_form_medical()
            form_medical.last_blood_type = form_medical.get_employee_last_blood()
            form_medical.last_cholesterol = form_medical.get_employee_last_cholesterol()
            form_medical.last_employee_blood_presure = form_medical.get_employee_last_employee_blood_presure()
            form_medical.last_employee_height = form_medical.get_employee_last_employee_height()
            form_medical.last_employee_weight = form_medical.get_employee_last_employee_weight()


    @api.multi
    @api.depends('detail_form_medical_ids')
    def _compute_form_medical_count(self):
        # read_group as sudo, since form_medical count is displayed on form view
        for employee in self:

            form_medical_data = employee.env['nievecus.form.medical'].search(
                [('employee_id', '=', employee.id)])

            try:
                count_form_medical = len(form_medical_data)
            except:
                count_form_medical = 0
            employee.count_form_medical = count_form_medical

    @api.multi
    @api.depends('detail_form_illness_ids')
    def _compute_form_illness_count(self):
        # read_group as sudo, since form_illness count is displayed on form view
        for employee in self:

            form_illness_data = employee.env['nievecus.form.illness'].search(
                [('employee_id', '=', employee.id)])

            try:
                count_form_illness = len(form_illness_data)
            except:
                count_form_illness = 0

            employee.count_form_illness = count_form_illness