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

    detail_training_ids = fields.One2many('nievecus_hr_indonesia.training','employee_id', string='training List')
    count_training = fields.Integer('Count training', compute='_compute_training_count')
    last_training = fields.Many2one('nievecus_hr_indonesia.training','Last Training',
                                       compute='compute_get_employee_training',store=True)

    @api.multi
    def act_show_log_training(self):
        """ This opens log view to view and add new log for this employee, groupby default to only show training Member
            @return: the training member log view
        """
        self.ensure_one()
        res = self.env['ir.actions.act_window'].for_xml_id('nievecus_hr_indonesia_training',
                                                           'nievecus_training_action2')
        res.update(
            context=dict(self.env.context, default_employee_id=self.id, search_default_parent_false=True),
            domain=[('employee_id', '=', self.id)]
        )
        return res

    @api.multi
    def get_employee_last_training(self):
        """
        this method use to get employee last training
        :return: training_id
        """
        Employeetraining = self.env['nievecus_hr_indonesia.training']
        for training in self:
            employee_training = Employeetraining.search([('employee_id', '=', training.id)], limit=1,
                                                          order='date_end desc')

            if employee_training:
                training_id = employee_training.id
            else:
                training_id = 0

            return training_id

    @api.multi
    @api.depends('detail_training_ids')
    def compute_get_employee_training(self):

        """onchange value contract from  employee last training"""
        for training in self:
            training.last_training = training.get_employee_last_training()

    @api.multi
    @api.depends('detail_training_ids')
    def _compute_training_count(self):
        # read_group as sudo, since training count is displayed on form view
        for employee in self:

            training_data = employee.env['nievecus_hr_indonesia.training'].search(
                [('employee_id', '=', employee.id)])

            try:
                count_training = len(training_data)
            except:
                count_training = 0
            employee.count_training = count_training
