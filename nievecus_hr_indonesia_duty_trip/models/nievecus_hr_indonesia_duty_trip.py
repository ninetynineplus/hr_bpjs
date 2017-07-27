import calendar
from datetime import datetime, date,time,timedelta as td
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

class DutyTrip(models.Model):
    
    _name = "duty.trip"
    _rec_name = 'name'
    _description = "Perjalanan Dinas"

    @api.model
    def _get_default_requested_by(self):
        return self.env['res.users'].browse(self.env.uid)

    @api.multi
    def approve(self):
        for item in self:
            return item.write({
            'state': 'approve'
        })

    @api.multi
    def paid(self):
        for item in self:
            return item.write({
            'state': 'paid'
        })

    @api.multi
    def settle(self):
        for item in self:
            return item.write({
            'state': 'settle'
        })

    @api.multi
    def done(self):
        for item in self:
            return item.write({
            'state': 'done'
        })

    @api.multi
    def cancel(self):
        for item in self:
            return item.write({'state': 'draft'})

    @api.multi
    def propose_payment(self):
        for item in self:
            return item.write({'state': 'wait_pay'})
    
    @api.multi
    def set_to_draft(self):
        for item in self:
            return item.write({'state': 'draft'})

    name = fields.Char('Name', size=64)
    no_number = fields.Char('Number', size=64)
    employee_id = fields.Many2one('hr.employee', 'Responsible')
    depart_id = fields.Many2one('hr.department',related='employee_id.department_id',readonly=True, store=True)
    job_id = fields.Many2one('hr.job',related='employee_id.job_id', string='Job Title',readonly=True, store=True)
    user_id = fields.Many2one('res.users', "Create By",default=_get_default_requested_by)
    date_start = fields.Date('Start Date',default=fields.Date.context_today)
    date_create = fields.Date('Date Create',default=fields.Date.context_today)
    date_end = fields.Date('End Date',default=fields.Date.context_today)
    total_days = fields.Integer(compute='_total_days', string='Total Days')
    departure = fields.Char("Departure", size=64)
    destination = fields.Char("Destination", size=64)
    departure_local = fields.Many2one("res.country.state", "Departure", size=64)
    destination_local = fields.Many2one("res.country.state", "Destination", size=64)
    
    route = fields.Char('Route', size=64)
    
    employee = fields.Many2many('hr.employee', 'hr_duty_rel', 'employee_id', 'duty_id'),
    description = fields.Text('Purposes', size=256)
    flight_ids = fields.One2many('flight.list', 'duty_id', 'Flight List')
    hotel_ids = fields.One2many('hotel.list', 'duty_id', 'Hotel List')
    duty_list = fields.One2many('duty.list', 'duty_id', 'Duty List')
    category_id = fields.Many2one('duty.category', "Category")
    type = fields.Selection([('domestik', 'Domestic'), ('int', 'International')], 'Type',default='domestik')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirm'),
        ('approve', 'Approve'),
        ('wait_pay', 'Payment Propose'),
        ('paid', 'Paid'),
        ('settle', 'Settle'),
        ('done', 'Done')
    ], 'State',default='draft')
    tot_amount_idr = fields.Float(compute='_total_idr', string='Total IDR', multi="all IDR", store=True)
    tot_amount_usd = fields.Float(compute='_total_usd', string='Total USD', multi="all USD", store=True)
    voucher_no = fields.Char("Voucher No", size=64)
    voucher_date = fields.Date("Payment Date")


    @api.multi
    @api.depends('duty_list')
    def _total_usd(self):
        """
            this method to get sub total from duty list in USD
        :return: total
        """
        total = 0.0

        for val in self:
            for line in val.duty_list:
                if line.currency_id.name == 'USD':
                    total += line.tot_amount
            val.tot_amount_usd = total

    @api.multi
    @api.depends('duty_list')
    def _total_idr(self):
        """
           this method to get sub total from duty list in IDR
        :return: total
        """
        total = 0.0
        for val in self:
            for line in val.duty_list:
                if line.currency_id.name == 'IDR':
                    total += line.tot_amount
            print "total", total
        val.tot_amount_idr = total

    @api.multi
    @api.depends('date_start', 'date_end')
    def _total_days(self):
        """
            this method use to compute total day trip
        :return: total
        """

        res = {}
        day = {
            'Monday': 0,
            'Tuesday': 1,
            'Wednesday': 2,
            'Thursday': 3,
            'Friday': 4,
            'Saturday': 5,
            'Sunday': 6,
        }
        for val in self:
            emp_data = val.env['hr.employee'].browse(val.employee_id.id)
            contract_id = val.env['hr.payslip'].get_contract(emp_data, val.date_start, val.date_end)
            if not contract_id:
                warning = {
                    "title": ("No Contract Found !"),
                    'message': ("You should define a contract for employee : %s!" % (emp_data.resource_id.name))
                }

            d1 = datetime.strptime(val.date_start, '%Y-%m-%d').date()
            d2 = datetime.strptime(val.date_end, '%Y-%m-%d').date()

            delta = d2 - d1
            total = 0
            for i in range(delta.days + 1):
                t1 = d1 + td(days=i)
                t1day = day[t1.strftime("%A")]

                contract = self.env['hr.contract'].browse(contract_id)[0]
                contractdaycheck = self.env['resource.calendar.attendance'].search([
                    ('calendar_id', '=', contract.working_hours.id), ('dayofweek', '=', str(t1day))])
                if contractdaycheck:
                    total += 1
            val.total_days = total

    @api.multi
    def confirm(self):
        for record in self:
            seq_name = 'duty.trip.order'
            return record.write({
                'state': 'confirm',
                # 'name': record.env['ir.sequence'].next_by_code(seq_name)
            })

    @api.model
    def create(self, vals):
        seq_name = 'duty.trip.order'
        vals['name'] = self.env['ir.sequence'].next_by_code(seq_name)
        request = super(DutyTrip, self).create(vals)
        return request

DutyTrip()


class DutyCategory(models.Model):
    
    _name = "duty.category"
    
    name = fields.Char('Name', size=64)
    code = fields.Char('Code', size=12)
    
DutyCategory()


class DutyList(models.Model):
    
    _name = "duty.list"

    allowance = fields.Many2one('hr.employee.general.allowance','Allowance',
                                domain=[('is_duty','=',True),('type','=','normal')])
    name = fields.Char('Alloance Name',related='allowance.name')
    amount = fields.Float('Unit Price')
    tot_amount = fields.Float(compute='_amount_line', string='Subtotal',store=True)
    qty = fields.Float('Qty')
    duty_id = fields.Many2one('duty.trip', 'Duty Trip')
    currency_id = fields.Many2one('res.currency', 'Currency')

    @api.multi
    @api.depends('amount', 'qty')
    def _amount_line(self):
        """
            this method use to compute subtotal
        :return: sub_total
        """
        for line in self:
            sub_total = line.qty * line.amount

            line.tot_amount = sub_total

DutyList()


class FlightList(models.Model):

    _name = "flight.list"
    
    flight_num = fields.Char("Flight No", size=64)
    flight_dep = fields.Char("Departure City", size=64)
    flight_arr = fields.Char("Arrival City", size=64)
    flight_date = fields.Date("Flight Date", size=64)
    flight_time = fields.Float("Flight Time", size=64)
    arrival_time = fields.Float("Arrival Time", size=64)
    arrival_date = fields.Date("Arrival Date", size=64)
    duty_id = fields.Many2one('duty.trip', 'Duty Trip')

FlightList()


class HotelList(models.Model):

    _name = "hotel.list"
    
    hotel_name = fields.Char("Hotel Name", size=64)
    check_in_date = fields.Date("Check In Date")
    check_out_date = fields.Date("Check Out Date")
    note = fields.Text("Note")
    duty_id = fields.Many2one('duty.trip', 'Duty Trip')

HotelList()

