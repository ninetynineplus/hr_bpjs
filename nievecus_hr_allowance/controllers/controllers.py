# -*- coding: utf-8 -*-
from odoo import http

# class NievecusHrAllowance(http.Controller):
#     @http.route('/nievecus_hr_allowance/nievecus_hr_allowance/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/nievecus_hr_allowance/nievecus_hr_allowance/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('nievecus_hr_allowance.listing', {
#             'root': '/nievecus_hr_allowance/nievecus_hr_allowance',
#             'objects': http.request.env['nievecus_hr_allowance.nievecus_hr_allowance'].search([]),
#         })

#     @http.route('/nievecus_hr_allowance/nievecus_hr_allowance/objects/<model("nievecus_hr_allowance.nievecus_hr_allowance"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('nievecus_hr_allowance.object', {
#             'object': obj
#         })