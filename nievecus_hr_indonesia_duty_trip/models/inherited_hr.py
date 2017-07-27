import calendar
from datetime import datetime, date,time,timedelta as td
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

    detail_duty_trip_ids = fields.One2many('duty.trip','employee_id',string='duty_trip')
    count_duty_trip = fields.Integer('Count duty_trip',compute='_compute_duty_trip_count')
    last_duty_trip = fields.Many2one('duty.trip','duty_trip',
                                     compute='compute_get_employee_last_duty')

    @api.multi
    def get_employee_last_duty_trip(self):
        """
        this method use to get employee last duty_trip
        :return: duty_trip_id
        """
        Employeeduty_trip = self.env['duty.trip']
        for duty_trip in self:
            employee_duty_trip = Employeeduty_trip.search([('employee_id', '=',duty_trip.id)], limit=1,order='id desc')

            if employee_duty_trip:
                duty_trip_id = employee_duty_trip.id
            else:
                duty_trip_id = 0

            return duty_trip_id

    @api.multi
    @api.depends('detail_duty_trip_ids')
    def compute_get_employee_last_duty(self):

        """onchange value contract from  employee last duty_trip"""
        for duty in self:
            duty.last_duty_trip = duty.get_employee_last_duty_trip()

    @api.multi
    @api.depends('detail_duty_trip_ids')
    def _compute_duty_trip_count(self):
        # read_group as sudo, since duty_trip count is displayed on form view
        for employee in self:

            duty_trip_data = employee.env['duty.trip'].search([('employee_id', '=', employee.id)])

            try:
                count_duty_trip = len(duty_trip_data)
            except:
                count_duty_trip = 0
            employee.count_duty_trip = count_duty_trip

    @api.multi
    def act_show_log_duty_trip(self):
        """ This opens log view to view and add new log for this employee, groupby default to only show duty_trip
            @return: the duty_trip log view
        """
        self.ensure_one()
        res = self.env['ir.actions.act_window'].for_xml_id('nievecus_hr_indonesia_duty_trip',
                                                           'nievecus_hr_indonesia_duty_trip_view_action_2')
        res.update(
            context=dict(self.env.context, default_employee_id=self.id, search_default_parent_false=True),
            domain=[('employee_id', '=', self.id)]
        )
        return res