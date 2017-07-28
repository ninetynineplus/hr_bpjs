import calendar
from datetime import datetime, date, time
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

class NievecusGeneralPathologyCategory(models.Model):

    _name = 'nievecus.medical.pathology.category'
    _description = 'Medical Pathology Category'

    @api.one
    @api.constrains('parent_id')
    def _check_recursion_parent_id(self):
        if not self._check_recursion():
            raise ValidationError('Error! You can not create recursive zone.')

    name = fields.Char(required=True, translate=True)
    child_ids = fields.One2many(
        comodel_name='nievecus.medical.pathology.category', inverse_name='parent_id',
        string='Children Categories')
    parent_id = fields.Many2one(
        comodel_name='nievecus.medical.pathology.category', string='Parent Category',
        index=True)