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



class NievecusFormIllness(models.Model):

    @api.model
    def _get_default_requested_by(self):
        return self.env['res.users'].browse(self.env.uid)

    _name = 'nievecus.form.illness'
    _description = 'This module provide to request illness employee'

    name = fields.Char('Medical Form Name')
    created_by = fields.Many2one('res.user',default=_get_default_requested_by)
    employee_id = fields.Many2one('hr.employee','Employee')
    department_id = fields.Many2one('hr.department','Department Employee',related='employee_id.department_id')
    job_id = fields.Many2one('hr.job','Jobs Employee',related='employee_id.job_id')
    hospital_id = fields.Many2one('nievecus.medical.hospital','Hospital')
    age_employee = fields.Integer('Employee Age')
    pathology_id = fields.Many2one('nievecus.general.pathology','Pathology')
    description = fields.Text('Description disease')
    date_start = fields.Date('Date Start Illness',default=fields.Date.context_today)
    date_end = fields.Date('Date End Illness',default=fields.Date.context_today)
    state = fields.Selection([('draft','Draft'),('pay','Pay'),('approve','Approved')],default='draft')
    treatment_description = fields.Char()
    file_disease = fields.Char('Disease Name')
    image_disease = fields.Binary('Upload File Disease')
    file_medical_prescription = fields.Char('Medical Prescription File')
    image_medical_prescription = fields.Binary('Upload Medical Prescription')
    type_rembursment = fields.Selection([('bpjs','BPJS'),('company','Company')],
                                        string='Rembursment',compute='_change_type_rembursment')
    prescription_ids = fields.One2many('nievecus.illness.prescription','illness_id','Line of illsenss prescription')
    total_amount_prescription = fields.Float('Total Amount',compute='_compute_amount_prescription')
    total_company_contribution = fields.Float('Company Contribution',compute='_compute_amount_prescription')
    total_employee_contribution = fields.Float('Employee Contribution',compute='_compute_amount_prescription')

    @api.multi
    def _get_value_employee_contribution(self):
        """
            this method to searching parameter employee contribution in 'ir.parameters'
        :return: employee_parameter
        """
        Parameters = self.env['ir.config_parameter']
        for item in self:
            params = item._name + '.employee'

            try:
                employee_parameter = Parameters.search([('key','like',params)]).value
            except:
                employee_parameter = 0
            return employee_parameter

    @api.multi
    def _get_value_company_contribution(self):
        """
            this method to searching parameter company contribution in 'ir.parameters'
        :return: company_parameter
        """
        Parameters = self.env['ir.config_parameter']
        for item in self:
            params = item._name + '.company'
            try:
                company_parameter = Parameters.search([('key', 'like', params)]).value
            except:
                company_parameter = 0
            return company_parameter

    @api.multi
    @api.depends('prescription_ids')
    def _compute_amount_prescription(self):
        """
            this method use to compute amount , employee contribution and company contribution
        :return:
        """
        for item in self:
            employee_params = item._get_value_employee_contribution()
            company_params = item._get_value_company_contribution()
            item.total_amount_prescription = sum(record.total_amount for record in item.prescription_ids)

            if employee_params == 0:
                raise exceptions.ValidationError('Please Set your illness employee parameter in (ir.parameters), '
                                                 'or call your system support')

            item.total_employee_contribution = float(item.total_amount_prescription) * \
                                               (float(employee_params) / float(100.0))

            if company_params == 0:
                raise exceptions.ValidationError('Please Set your illness company parameter in (ir.parameters), '
                                                 'or call your system support')

            item.total_company_contribution = float(item.total_amount_prescription) * \
                                               (float(company_params) / float(100.0))

    @api.multi
    def _get_employee_list_bpjs(self):
        for item in self:
            """This method to get list of bpjs from rel_bpjs"""

            item.env.cr.execute('select hr_employee_general_bpjs_id from rel_bpjs where'
                                ' hr_employee_id = %s and hr_employee_general_bpjs_id in ('
                                'select id from hr_employee_general_bpjs where type_kesehatan = True'
                                ')' % (item.employee_id.id))

            return [i[0] for i in item.env.cr.fetchall()]

    @api.multi
    @api.depends('employee_id')
    def _change_type_rembursment(self):
        Bpjs = self.env['hr.employee.general.bpjs']
        for item in self:
            arrBpjs = []
            bpjs_kesehatan = Bpjs.search([('type_kesehatan','=',True)])
            for record in bpjs_kesehatan:
                arrBpjs.append(record.id)

            list_employee_bpjs = set(item._get_employee_list_bpjs())
            list_bpjs = set(arrBpjs)

            if list_bpjs == list_employee_bpjs:
                item.type_rembursment = 'bpjs'
            else:
                item.type_rembursment = 'company'

class NievecusIllnessPrescription(models.Model):

    _name = 'nievecus.illness.prescription'

    illness_id = fields.Many2one('nievecus.form.illness','Illness Form')
    name = fields.Char('Name Recipt')
    qty = fields.Float('Qty')
    amount = fields.Float('Amount')
    total_amount = fields.Float('Total Amount',compute='compute_total_amount',store=True)

    @api.multi
    @api.depends('qty','amount')
    def compute_total_amount(self):
        """
            this method to compute total amount
            depends on qty and amount
        :return:
        """
        for record in self:
            total = record.qty * record.amount
            record.total_amount = total