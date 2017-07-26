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

class InheritHrEmployee(models.Model):

    _inherit = 'hr.employee'

    detail_drive_license_ids = fields.One2many('nievecus_hr.drive.license','employee_id', string='drive_license List')
    count_drive_license = fields.Integer('Count drive_license', compute='_compute_drive_license_count')
    last_license = fields.Many2one('nievecus_hr.drive.license','Last Company',
                                       compute='compute_get_employee_drive_license',store=True)

    @api.multi
    def act_show_log_drive_license(self):
        """ This opens log view to view and add new log for this employee, groupby default to only show drive_license Member
            @return: the drive_license member log view
        """
        self.ensure_one()
        res = self.env['ir.actions.act_window'].for_xml_id('nievecus_hr_indonesia_license',
                                                           'nievecus_drive_license_action2')
        res.update(
            context=dict(self.env.context, default_employee_id=self.id, search_default_parent_false=True),
            domain=[('employee_id', '=', self.id)]
        )
        return res

    @api.multi
    def get_employee_last_drive_license(self):
        """
        this method use to get employee last drive_license
        :return: drive_license_id
        """
        Employeedrive_license = self.env['nievecus_hr.drive.license']
        for drive_license in self:
            employee_drive_license = Employeedrive_license.search([('employee_id', '=', drive_license.id)], limit=1,
                                                          order='id desc')

            if employee_drive_license:
                drive_license_id = employee_drive_license.id
            else:
                drive_license_id = 0

            return drive_license_id

    @api.multi
    @api.depends('detail_drive_license_ids')
    def compute_get_employee_drive_license(self):

        """onchange value contract from  employee last drive_license"""
        for drive_license in self:
            drive_license.last_license = drive_license.get_employee_last_drive_license()

    @api.multi
    @api.depends('detail_drive_license_ids')
    def _compute_drive_license_count(self):
        # read_group as sudo, since drive_license count is displayed on form view
        for employee in self:

            drive_license_data = employee.env['nievecus_hr.drive.license'].search(
                [('employee_id', '=', employee.id)])

            try:
                count_drive_license = len(drive_license_data)
            except:
                count_drive_license = 0
            employee.count_drive_license = count_drive_license