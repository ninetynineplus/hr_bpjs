# 1 : imports of python lib

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

from openerp.exceptions import ValidationError, RedirectWarning

_logger = logging.getLogger(__name__)

class HrEmployeeGeneralBpjs(models.Model):

    _name = 'hr.employee.general.bpjs'
    _rec_name = 'complete_name'
    _description = "this module to provide bpjs indonesia"

    name = fields.Char('BPJS Name')
    complete_name = fields.Char("Complete Name", compute="_complete_name", store=True)
    parent_id = fields.Many2one('hr.employee.general.bpjs', "Parent Category", ondelete='restrict')
    contribution_employee_id = fields.Many2one('hr.employee.bpjs.contribution.value','Contribution Employee Value')
    contribution_company_id = fields.Many2one('hr.employee.bpjs.contribution.value', 'Contribution Company Value')
    type_contribution_employee = fields.Boolean('Contribution Type')
    type_contribution_company = fields.Boolean('Contribution Type')
    penalty = fields.Boolean('Bpjs Penalty')
    type_kesehatan = fields.Boolean('Type BPJS Kesehatan')
    type = fields.Selection([('view','View'),('normal','Normal')],'Type',defaults='view')

    @api.multi
    @api.depends('name', 'parent_id')
    def _complete_name(self):
        """ Forms complete name of location from parent category to child category.
        """
        for item in self:
            if item.parent_id:
                item.complete_name = item.parent_id.complete_name + ' / ' + item.name
            else:
                item.complete_name = item.name


class HrEmployeeBpjsContributionValue(models.Model):

    _name = 'hr.employee.bpjs.contribution.value'
    _rec_name = 'name'

    name = fields.Float('Value of Bpjs')
