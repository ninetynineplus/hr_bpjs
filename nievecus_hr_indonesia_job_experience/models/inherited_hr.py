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

    detail_job_experience_ids = fields.One2many('nievecus_hr_indonesia.job.experience','employee_id', string='job_experience List')
    count_job_experience = fields.Integer('Count job_experience', compute='_compute_job_experience_count')
    last_company = fields.Many2one('nievecus_hr_indonesia.job.experience','Emergency Person',
                                       compute='compute_get_employee_job_experience',store=True)

    @api.multi
    def act_show_log_job_experience(self):
        """ This opens log view to view and add new log for this employee, groupby default to only show job_experience Member
            @return: the job_experience member log view
        """
        self.ensure_one()
        res = self.env['ir.actions.act_window'].for_xml_id('nievecus_hr_indonesia_job_experience',
                                                           'nievecus_job_experience_action2')
        res.update(
            context=dict(self.env.context, default_employee_id=self.id, search_default_parent_false=True),
            domain=[('employee_id', '=', self.id)]
        )
        return res

    @api.multi
    def get_employee_last_job_experience(self):
        """
        this method use to get employee last job_experience
        :return: job_experience_id
        """
        Employeejob_experience = self.env['nievecus_hr_indonesia.job.experience']
        for job_experience in self:
            employee_job_experience = Employeejob_experience.search([('employee_id', '=', job_experience.id)], limit=1,
                                                          order='id desc')

            if employee_job_experience:
                job_experience_id = employee_job_experience.id
            else:
                job_experience_id = 0

            return job_experience_id

    @api.multi
    @api.depends('detail_job_experience_ids')
    def compute_get_employee_job_experience(self):

        """onchange value contract from  employee last job_experience"""
        for job_experience in self:
            job_experience.last_company = job_experience.get_employee_last_job_experience()

    @api.multi
    @api.depends('detail_job_experience_ids')
    def _compute_job_experience_count(self):
        # read_group as sudo, since job_experience count is displayed on form view
        for employee in self:

            job_experience_data = employee.env['nievecus_hr_indonesia.job.experience'].search(
                [('employee_id', '=', employee.id)])

            try:
                count_job_experience = len(job_experience_data)
            except:
                count_job_experience = 0
            employee.count_job_experience = count_job_experience
