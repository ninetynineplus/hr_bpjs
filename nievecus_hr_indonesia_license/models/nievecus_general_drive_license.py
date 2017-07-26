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


class GeneralDriveLicense(models.Model):

    _name = 'general.driver.licence'
    _description = 'This class of general license'

    name = fields.Char('License Name')
    complete_name = fields.Char("Complete Name", compute="_complete_name", store=True)
    parent_id = fields.Many2one('general.driver.licence', "Parent Category",domain=[('type','=','view')],ondelete='restrict')
    type_license = fields.Selection([('air', 'Air'), ('land', 'Land'),('water','Water'),('other','Other')], 'Type License',
                                    defaults='view')
    type = fields.Selection([('view', 'View'), ('normal', 'Normal')], 'Type', defaults='view')

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