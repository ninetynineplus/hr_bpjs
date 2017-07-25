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

_logger = logging.getLogger(__name__)


class Employee(models.Model):
    """Extend HR Employee to accommodate Indonesian Workforce.
    1. KHL is Daily PKWT.
    2. KHT is Daily PKWTT.
    3. Employee or Staf is Monthly PKWTT.
    4. Contract is Monthly PKWT.
    """
    _inherit = 'hr.employee'

    # Employee Information
    nik_number = fields.Char("Employee Identity Number", track_visibility="onchange")
    health_insurance_number = fields.Char("Health Insurance Number")
    npwp_number = fields.Char("NPWP Number")
    company_id = fields.Many2one('res.company', "Company", track_visibility="onchange")
    contract_type = fields.Selection([('1', 'PKWTT'), ('2', 'PKWT'),('3', 'PKWTT Probation')], "Contract Type",
                                       help="* PKWTT, Perjanjian Kerja Waktu Tidak Tertentu, "\
                                            "* PKWT, Perjanjian Kerja Waktu Tertentu.", track_visibility="onchange")
    contract_period = fields.Selection([('1', 'Monthly'), ('2', 'Daily')], "Contract Period",
                                       help="* Monthly, Karyawan Bulanan, "\
                                            "* Daily, Karyawan Harian.", track_visibility="onchange")
    outsource = fields.Boolean("Outsource employee", help="Activate to represent employee as Outsource.")
    internship = fields.Boolean("Internship", help="Activate to represent internship employee.")
    age = fields.Float("Employee Age", compute='_compute_age')
    joindate = fields.Date("Date of Join")
    religion_id = fields.Many2one('nievecus_hr_indonesia.religion', "Religion")
    ethnic_id = fields.Many2one('nievecus_hr_indonesia.ethnic', "Ethnic")
    tax_marital_id = fields.Many2one('nievecus_hr_indonesia.tax_marital', 'Tax Marital')
    tax_dependent = fields.Integer('Dependent')
    location_id = fields.Many2one('nievecus_hr_indonesia.location', 'Placement Location')
    office_level_id = fields.Many2one('nievecus_hr_indonesia.office', 'Office Level')
    supervisor_level_id = fields.Many2one('nievecus_hr_indonesia.supervisor', 'Supervisor Level')

    date_probation = fields.Char('Date of Probation', compute='_compute_probation')
    month_probation = fields.Integer('Month Probation')
    image_family_card = fields.Binary('Upload Family Card')
    family_card_name = fields.Char('Family Card Name')
    image_npwp = fields.Binary('Upload NPWP')
    npwp_name = fields.Char('NPWP Name')
    identif_num = fields.Char('Identification Number', related='identification_id')
    age_employee = fields.Char('Age', compute='_compute_age', readonly="True")
    resigndate = fields.Date('Date of Resign')
    hiredate = fields.Date('Date of Hired')
    grade_id = fields.Many2one('hr.indonesia.grade', 'Grade')
    religion = fields.Char('Religion', compute='_compute_religion')


    def _compute_age(self):
        for record in self:
            record.age = 1

    @api.multi
    @api.constrains('joindate', 'hiredate')
    def _check_joindate(self):
        """
            this method to contraint hire date not be higher than  join date
        :return: True or false
        """
        for item in self:
            if item.joindate == False:
                return True
            elif item.hiredate == False:
                raise exceptions.ValidationError("Input Date of Hired first")
            elif item.joindate < item.hiredate:
                raise exceptions.ValidationError("Date of join is Invalid")

    @api.multi
    @api.constrains('joindate', 'resigndate')
    def _check_resigndate(self):
        """
           this method to contraint join date not be higher than resign date
        :return: True or false
        """
        for item in self:
            if item.resigndate == False:
                return True
            elif item.joindate == False:
                raise exceptions.ValidationError("Input Date of Join first")
            elif item.resigndate < item.joindate:
                raise exceptions.ValidationError("Date of Resign is Invalid")

    @api.multi
    @api.constrains('place_of_birth')
    def _check_description(self):
        """
           this method to contraint place birthdate can be alphabet only
        :return: True or false
        """
        for item in self:
            if item.place_of_birth == False:
                return True
            elif bool(re.search(r'\d', item.place_of_birth)):
                raise exceptions.ValidationError("Fields place of birth contain aphabet only")

    @api.multi
    @api.constrains('emergency_person')
    def _check_person(self):
        """
           this method to contraint Emergency contact canbe aplhabet only
        :return: True or false
        """
        for item in self:
            if item.emergency_person == False:
                return True
            elif bool(re.search(r'\d', item.emergency_person)):
                raise exceptions.ValidationError("Fields Emergency Contact Person contain alphabet only")
            elif len(item.emergency_person) < 3 or len(item.emergency_person) > 30:
                raise exceptions.ValidationError('Emergency Contact Person must 3-30 character')

    @api.multi
    @api.constrains('emergency_phone')
    def _constraint_emergency_phone(self):
        """
           this method to contraint Emergency contact canbe integer only
        :return: True or false
        """
        for item in self:
            val = item.emergency_phone
            if val == False:
                return True
            elif not val.isdigit():
                raise exceptions.ValidationError('Emergency Contact Phone must be numeric')
            elif len(val) < 10 or len(val) > 14:
                raise exceptions.ValidationError('Emergency Contact Phone is not valid')

    @api.multi
    @api.constrains('mobile_phone')
    def check_numval_mobile_phone(self):
        """
           this method to contraint Mobile Phone contact canbe integer only
        :return: True or false
        """
        for item in self:
            val = item.mobile_phone
            if val == False:
                return True
            elif not val.isdigit():
                raise exceptions.ValidationError('Work Mobile must be numeric')

    @api.multi
    @api.constrains('identification_id')
    def check_numval_identification_id(self):
        """
          this method to contraint identification id contact canbe integer only
       :return: True or false
       """
        for item in self:
            val = item.identification_id
            if val == False:
                return True
            elif not val.isdigit():
                raise exceptions.ValidationError('Identification No. must be numeric')

    @api.one
    @api.constrains('family_card_name')
    def _check_filename(self):
        """
          this method to contraint format of family card name
       :return: True or false
       """
        if self.family_card_name:
            if not self.family_card_name:
                raise exceptions.ValidationError("There is no file")
            else:
                # Check the file's extension
                tmp = self.family_card_name.split('.')
                ext = tmp[len(tmp) - 1]
                if ext != 'jpg' and ext != 'img' and ext != 'jpeg' and ext != 'png' and ext != 'pdf':
                    raise exceptions.ValidationError(
                        "The family card file must be a img, png, jpg, jpeg, or pdf format file")

    @api.one
    @api.constrains('npwp_name')
    def _check_npwpname(self):
        """
         this method to contraint format of family card name
        :return: True or false
        """
        if self.npwp_name:
            if not self.npwp_name:
                raise exceptions.ValidationError("There is no file")
            else:
                # Check the file's extension
                tmp = self.npwp_name.split('.')
                ext = tmp[len(tmp) - 1]
                if ext != 'jpg' and ext != 'img' and ext != 'jpeg' and ext != 'png' and ext != 'pdf':
                    raise exceptions.ValidationError(
                        "The NPWP file must be a img, png, jpg, jpeg, or pdf file")

    @api.multi
    @api.depends('month_probation', 'joindate')
    def _compute_probation(self):
        """
           this method to compute Month probation
        :return: result
        """
        for item in self:
            if item.joindate == False:
                return True
            else:
                fmt = '%Y-%m-%d'

                conv_joindate = datetime.strptime(str(item.joindate), fmt)
                init_joindate = conv_joindate.date()

                result = init_joindate.month + item.month_probation

                item.date_probation = result

    @api.multi
    @api.depends('birthday')
    def _compute_age(self):
        """
           this method to compute Birthdate
        :return: age_employee
        """
        for item in self:
            if item.birthday == False:
                return True
            else:
                fmt = '%Y-%m-%d'
                datenow = datetime.today()
                birthday = item.birthday

                conv_bitrhday = datetime.strptime(str(birthday), fmt)
                init_birthday = conv_bitrhday.date()

                result_year = datenow.year - init_birthday.year - (
                    (datenow.month, init_birthday.day) < (init_birthday.month, init_birthday.day))
                if result_year < 18:
                    item.age_employee = str(result_year) + ' Under Age'
                else:
                    item.age_employee = str(result_year)


class Religion(models.Model):
    """ Required to define THR allowance """
    _name = 'nievecus_hr_indonesia.religion'
    _description = 'Religion'

    name = fields.Char("Religion")
    sequence = fields.Integer('Sequence')


class Ethnic(models.Model):
    _name = 'nievecus_hr_indonesia.ethnic'
    _description = 'Ethnic'

    name = fields.Char('Ethnic')
    sequence = fields.Integer('Sequence')


class TaxMarital(models.Model):
    _name = 'nievecus_hr_indonesia.tax_marital'
    _description = 'Tax Marital'

    name = fields.Char('Tax Marital')
    code = fields.Char('Code', help='Displayed at report.')
    sequence = fields.Integer('Sequence')


class Location(models.Model):
    """ Do not used stock location.
    """
    _name = 'nievecus_hr_indonesia.location'
    _parent_store = True
    _parent_name = 'parent_id'
    _order = 'complete_name'
    _rec_name = 'name'  # complete_name too long for upkeep entry

    _description = 'Placement Location'

    name = fields.Char('Location Name', required=True)
    complete_name = fields.Char("Complete Name", compute="_complete_name", store=True)
    code = fields.Char('Code', help='Write location abbreviation')
    type = fields.Selection([('view', "View"),
                             ('normal', "Normal")], "Type",
                            required=True,
                            help="Select View to create group of location.")
    comment = fields.Text("Additional Information")
    sequence = fields.Integer("Sequence", help="Keep location in order.") # todo set as parent_left at create
    parent_id = fields.Many2one('nievecus_hr_indonesia.location', "Parent Category", ondelete='restrict')
    parent_left = fields.Integer("Parent Left",	index=True)
    parent_right = fields.Integer("Parent Right", index=True)
    child_ids = fields.One2many('nievecus_hr_indonesia.location', 'parent_id', "Child Locations")

    @api.multi
    @api.depends('name', 'parent_id')
    def _complete_name(self):
        """ Forms complete name of location from parent category to child category.
        """
        for record in self:
            if record.parent_id:
                record.complete_name = record.parent_id.complete_name + ' / ' + record.name
            else:
                record.complete_name = record.name


class Office(models.Model):
    """ Hierarchy of office - required by purchase"""
    _name = 'nievecus_hr_indonesia.office'
    _parent_store = True
    _parent_name = 'parent_id'
    _order = 'sequence'
    _description = 'Office Level'

    name = fields.Char('Name', required=True)
    code = fields.Char('Code', help='Write office level')
    comment = fields.Text("Additional Information")
    sequence = fields.Integer("Sequence", help="Small number higher position.")
    parent_id = fields.Many2one('nievecus_hr_indonesia.office', "Parent Office", ondelete='restrict')
    parent_left = fields.Integer("Parent Left", index=True)
    parent_right = fields.Integer("Parent Right", index=True)
    child_ids = fields.One2many('nievecus_hr_indonesia.office', 'parent_id', "Child Office Levels")


class SupervisorLevel(models.Model):
    """ Class of position such as Division Manager and Section Chief"""

    _name = 'nievecus_hr_indonesia.supervisor'
    _parent_store = True
    _parent_name = 'parent_id'
    _order = 'sequence'

    _description = 'Supervisor Level'

    name = fields.Char('Name', required=True)
    code = fields.Char('Code', help='Write supervisor level')
    comment = fields.Text("Additional Information")
    sequence = fields.Integer("Sequence", help="Small number higher position.")
    parent_id = fields.Many2one('nievecus_hr_indonesia.supervisor', "Parent Supervisor", ondelete='restrict')
    parent_left = fields.Integer("Parent Left", index=True)
    parent_right = fields.Integer("Parent Right", index=True)
    child_ids = fields.One2many('nievecus_hr_indonesia.supervisor', 'parent_id', "Child Supervisor Levels")

    @api.constrains('code')
    def _check_code(self):
        """Code max 3"""
        if self.code:
            if len(self.code) > 3:
                msg_error = _('Supervisor level code should be 3 character long or less.')
                raise ValidationError(msg_error)
        else:
            return True
