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

    detail_family_ids = fields.One2many('nievecus_hr.family','employee_id', string='Family List')
    count_family = fields.Integer('Count Education', compute='_compute_education_count')
    emergency_person = fields.Many2one('nievecus_hr.family','Emergency Person')
    emergency_phone = fields.Integer('Emergency Contact Phone',related='emergency_person.family_phone')

    @api.multi
    def act_show_log_family(self):
        """ This opens log view to view and add new log for this employee, groupby default to only show Family Member
            @return: the Family member log view
        """
        self.ensure_one()
        res = self.env['ir.actions.act_window'].for_xml_id('nievecus_hr_indonesia_family',
                                                           'nievecus_hr_family_action2')
        res.update(
            context=dict(self.env.context, default_employee_id=self.id, search_default_parent_false=True),
            domain=[('employee_id', '=', self.id)]
        )
        return res

