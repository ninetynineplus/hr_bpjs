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

    detail_education_ids = fields.One2many('nievecus_hr_indonesia.education.detail','employee_id',string='Education')
    count_education = fields.Integer('Count Education',compute='_compute_education_count')

    @api.multi
    @api.depends('detail_education_ids')
    def _compute_education_count(self):
        # read_group as sudo, since Education count is displayed on form view
        for employee in self:

            education_data = employee.env['nievecus_hr_indonesia.education.detail'].search([('employee_id', '=', employee.id)])

            try:
                count_education = len(education_data)
            except:
                count_education = 0
            employee.count_education = count_education

    @api.multi
    def act_show_log_education(self):
        """ This opens log view to view and add new log for this employee, groupby default to only show Education
            @return: the Education log view
        """
        self.ensure_one()
        res = self.env['ir.actions.act_window'].for_xml_id('nievecus_hr_indonesia_education',
                                                           'nievecus_hr_indonesia_education_view_action_2')
        res.update(
            context=dict(self.env.context, default_employee_id=self.id, search_default_parent_false=True),
            domain=[('employee_id', '=', self.id)]
        )
        return res