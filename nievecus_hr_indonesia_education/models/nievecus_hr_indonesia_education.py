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


class NievecusHrEducation(models.Model):

    _name = 'nievecus_hr_indonesia.education'
    _description = 'This module to provide HT'
    _rec_name = 'name'

    name = fields.Char('Name')
    education_type = fields.Many2one('nievecus_hr_indonesia.education.type','Education Type')
    country_id = fields.Many2one('res.country', string='Country')


class NievecusHrEducationDetail(models.Model):

    _name = 'nievecus_hr_indonesia.education.detail'

    name = fields.Char('Name')
    education_type = fields.Many2one('nievecus_hr_indonesia.education.type','Education Type')
    education_id = fields.Many2one('nievecus_hr_indonesia.education', 'Education ID')
    employee_id = fields.Many2one('hr.employee', 'Employee')
    start_date = fields.Date('Start Date')
    end_date = fields.Date('End Date')
    country_id = fields.Many2one('res.country', string='Country')
    gpa = fields.Float('Index/GPA')
    image_certificate = fields.Binary('Upload certificate')
    certificate_name = fields.Char('Certificate')
    type = fields.Selection([
        ('staterun', 'State Run School'),
        ('private', 'Private School')],'Type School')

    @api.multi
    @api.onchange('education_id', 'country_id')
    def _onchange_education_id(self):
        """
        this method use to onchange education by country
        :return: domain
        """
        for item in self:
            if item.education_type and item.country_id:
                return {
                    'domain': {
                        'education_id': [('education_type', '=', item.education_type.id),
                                         ('country_id', '=', item.country_id.id)]
                    }
                }

    @api.one
    @api.constrains('certificate_name')
    def _check_certificate_name(self):
        """
            this method use to Constraint certificate
        :return: Constraint
        """
        if self.certificate_name:
            if not self.certificate_name:
                raise exceptions.ValidationError("There is no file")
            else:
                # Check the file's extension
                tmp = self.certificate_name.split('.')
                ext = tmp[len(tmp) - 1]
                if ext != 'jpg' and ext != 'img' and ext != 'jpeg' and ext != 'png' and ext != 'pdf':
                    raise exceptions.ValidationError(
                        "Certificate file must be a img, png, jpg, jpeg, or pdf file")

    @api.multi
    @api.constrains('gpa', 'education_type')
    def _check_gpa(self):
        """
            this method use to Constraint GPA Check
        :return: Constraint
        """
        for item in self:
            val = item.gpa
            edutype = item.education_type
            if val > 100:
                raise exceptions.ValidationError("Range Index/GPA is 0.00-100.00")
            elif val < 0:
                raise exceptions.ValidationError("Range Index/GPA is 0.00-100.00")


class NievecusHrEducationType(models.Model):

    _name = 'nievecus_hr_indonesia.education.type'

    name = fields.Char('Education Type')