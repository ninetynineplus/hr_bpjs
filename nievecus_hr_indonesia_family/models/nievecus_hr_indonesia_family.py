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

class NievecusHrFamily(models.Model):

    _name = 'nievecus_hr.family'
    _rec_name = 'name'

    name = fields.Char('Name', required=True)
    active_status = fields.Boolean('Active')
    status = fields.Many2one('nievecus_hr.status.family',required=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female','Female')], required=True)
    identif_no = fields.Char('Identification No')
    job_id = fields.Many2one('nievecus_hr.family.job','Last Job')
    employee_id = fields.Many2one('hr.employee', 'Employee')
    birthdate = fields.Date('Birth Date', required=True)
    birthplace = fields.Many2one('res.country.state', domain=[('regional_level','=','city')], required=True)
    birthplace_date = fields.Char(compute='compute_date_place')
    checking = fields.Boolean('Checking', compute='compute_checking')
    marital = fields.Selection([('single','Single'),('married','Married'),('divorced', 'Divorced')])
    age = fields.Integer('Age', compute='_compute_age')
    ticket = fields.Selection([('covered','Covered'),('not_covered','Not Covered')])
    health = fields.Selection([('covered', 'Covered'), ('not_covered', 'Not Covered')])
    emergency = fields.Boolean('Emergency Person')
    family_phone = fields.Char('Family Phone',defaults='+62')

    @api.multi
    @api.depends('birthdate')
    def _compute_age(self):
        """
            this method to compute date of birth family
        :return:result_year
        """
        for item in self:
            if item.birthdate == False:
                return True
            else:
                fmt='%Y-%m-%d'
                datenow= datetime.today()
                birthdate = item.birthdate

                conv_bitrhdate = datetime.strptime(str(birthdate),fmt)
                init_birthdate =conv_bitrhdate.date()

                result_year = datenow.year - init_birthdate.year - ((datenow.month, init_birthdate.day) < (init_birthdate.month, init_birthdate.day))

                item.age = result_year

    @api.multi
    @api.depends('birthdate','birthplace','birthplace_date', 'age')
    def compute_date_place(self):
        """
            this method to join bithtdate and  birthplace
        :return:place_date
        """
        for item in self:
            if item.birthdate and item.birthplace :
                place_date = item.birthplace.name + ', ' + str(item.birthdate)+' (Age '+str(item.age)+')'
                item.birthplace_date = place_date

    @api.multi
    @api.depends('checking','birthdate','birthplace','birthplace_date')
    def compute_checking(self):
        """
            this method to Check bithtdate and  birthplace
        :return:Checking
        """
        for item in self:
            if item.birthdate and item.birthplace :
                item.checking=True
            elif item.birthplace_date:
                item.checking=False
            else:
                item.checking=False

    @api.multi
    @api.constrains('name')
    def _constraint_name(self):
        """
            this method to Check Family name just only alphabet
        :return:Checking
        """
        for item in self:
            if bool(re.search(r'\d', item.name)):
                raise exceptions.ValidationError("Fields name family contain alphabet only")
            elif len(item.name) < 3 or len(item.name) > 30:
                raise exceptions.ValidationError('Name family must be 3-5 character')

    @api.multi
    @api.constrains('identif_no')
    def _constraint_identif_no(self):
        """
            this method to Check Family identification number  just only numeric
        :return:Checking
        """
        for item in self:
            val = item.identif_no
            if val == False:
                return True
            elif not val.isdigit():
                raise exceptions.ValidationError('Identification No. family must be numeric')

class NievecusHrFamilyJob(models.Model):

    _name = 'nievecus_hr.family.job'
    _inherits = {'hr.job' : 'job_id'}

    job_id = fields.Many2one('hr.job','Job')


class NievecusHrStatusFamily(models.Model):

    _name = 'nievecus_hr.status.family'
    _description = 'Status of Family '

    name = fields.Char('Status')
    child = fields.Boolean('Child')