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


class NievecusGeneralPathology(models.Model):

    _name = 'nievecus.general.pathology'
    _description = 'This class of general pathology'

    @api.one
    @api.constrains('code')
    def _check_unicity_name(self):
        domain = [
            ('code', '=', self.code),
        ]
        if len(self.search(domain)) > 1:
            raise ValidationError('"code" Should be unique per Pathology')

    name = fields.Char(required=True, translate=True)
    code = fields.Char(required=True)
    notes = fields.Text(translate=True)
    protein = fields.Char(string='Protein involved')
    chromosome = fields.Char(string='Affected Chromosome')
    gene = fields.Char()
    category_id = fields.Many2one(
        comodel_name='nievecus.medical.pathology.category',
        string='Category of Pathology', index=True)
    medical_pathology_group_m2m_ids = fields.Many2many(
        comodel_name='nievecus.medical.pathology.group', column1='pathology_id',
        colmun2='pathology_group_id', string='Medical Pathology Groups',
        relation="pathology_id_pathology_group_id_rel")