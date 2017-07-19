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

