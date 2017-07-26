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
    count_family = fields.Integer('Count family', compute='_compute_family_count')
    emergency_person = fields.Many2one('nievecus_hr.family','Emergency Person',
                                       compute='compute_get_employee_emergency_person')
    children = fields.Integer('Children', compute='compute_children')
    emergency_phone = fields.Char('Emergency Contact Phone',related='emergency_person.family_phone')

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

    @api.multi
    def get_employee_last_family(self):
        """
        this method use to get employee last family
        :return: family_id
        """
        Employeefamily = self.env['nievecus_hr.family']
        for family in self:
            employee_family = Employeefamily.search([('employee_id', '=', family.id),('emergency','=',True)], limit=1,
                                                          order='id desc')

            if employee_family:
                family_id = employee_family.id
            else:
                family_id = 0

            return family_id

    @api.multi
    @api.depends('detail_family_ids')
    def compute_get_employee_emergency_person(self):

        """onchange value contract from  employee last family"""
        for Family in self:
            Family.emergency_person = Family.get_employee_last_family()

    @api.multi
    @api.depends('detail_family_ids')
    def _compute_family_count(self):
        # read_group as sudo, since family count is displayed on form view
        for employee in self:

            family_data = employee.env['nievecus_hr.family'].search(
                [('employee_id', '=', employee.id)])

            try:
                count_family = len(family_data)
            except:
                count_family = 0
            employee.count_family = count_family

    @api.multi
    @api.depends('children', 'detail_family_ids')
    def compute_children(self):
        """
        this method use to calculate employee children
        :return: count_child
        """
        for item in self:
            if item.detail_family_ids:
                arrChild = []
                status_child = item.env['nievecus_hr.status.family'].search([('child','=',True)], limit=1).id
                child = item.env['nievecus_hr.family'].search(
                    [('status','=',status_child),
                     ('employee_id', '=', item.id),
                     ('active_status', '=', True)])
                for record in child:
                    arrChild.append(record.id)
                count_child = len(arrChild)
                item.children = count_child

