# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions


class InheritResCountryState(models.Model):

    _inherit = 'res.country.state'
    _order = 'name asc'

    regional_level  = fields.Selection([
        ('province', 'Province'),
        ('city', 'City'),
        ('district', 'District'),
        ('subdistrict', 'Sub-District')])
    parent_id = fields.Many2one('res.country.state')

    @api.multi
    @api.onchange('regional_level','parent_id')
    def _onchange_parent_id(self):
        """
        To onchange Regional Level in indonesia
        :return:
        """
        for item in self:
            arrParent = []
            if item.regional_level=='city':
                parent=item.env['res.country.state'].search([('regional_level','=','province')])
                for record in parent:
                    arrParent.append(record.id)
                return {
                    'domain':{'parent_id':[('id','in',arrParent)]}
                }
            elif item.regional_level=='district':
                parent=item.env['res.country.state'].search([('regional_level','=','city')])
                for record in parent:
                    arrParent.append(record.id)
                return {
                    'domain':{'parent_id':[('id','in',arrParent)]}
                }
            elif item.regional_level=='subdistrict':
                parent=item.env['res.country.state'].search([('regional_level','=','district')])
                for record in parent:
                    arrParent.append(record.id)
                return {
                    'domain':{'parent_id':[('id','in',arrParent)]}
                }

