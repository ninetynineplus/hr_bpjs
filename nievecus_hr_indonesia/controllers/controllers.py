# -*- coding: utf-8 -*-
from odoo import http

# class NievecusHrIndonesia(http.Controller):
#     @http.route('/nievecus_hr_indonesia/nievecus_hr_indonesia/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/nievecus_hr_indonesia/nievecus_hr_indonesia/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('nievecus_hr_indonesia.listing', {
#             'root': '/nievecus_hr_indonesia/nievecus_hr_indonesia',
#             'objects': http.request.env['nievecus_hr_indonesia.nievecus_hr_indonesia'].search([]),
#         })

#     @http.route('/nievecus_hr_indonesia/nievecus_hr_indonesia/objects/<model("nievecus_hr_indonesia.nievecus_hr_indonesia"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('nievecus_hr_indonesia.object', {
#             'object': obj
#         })