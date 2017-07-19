# -*- coding: utf-8 -*-
from odoo import http

# class NievecusHrBpjs(http.Controller):
#     @http.route('/nievecus_hr_bpjs/nievecus_hr_bpjs/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/nievecus_hr_bpjs/nievecus_hr_bpjs/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('nievecus_hr_bpjs.listing', {
#             'root': '/nievecus_hr_bpjs/nievecus_hr_bpjs',
#             'objects': http.request.env['nievecus_hr_bpjs.nievecus_hr_bpjs'].search([]),
#         })

#     @http.route('/nievecus_hr_bpjs/nievecus_hr_bpjs/objects/<model("nievecus_hr_bpjs.nievecus_hr_bpjs"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('nievecus_hr_bpjs.object', {
#             'object': obj
#         })