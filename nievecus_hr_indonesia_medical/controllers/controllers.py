# -*- coding: utf-8 -*-
from odoo import http

# class NievecusHrIndonesiaMedical(http.Controller):
#     @http.route('/nievecus_hr_indonesia_medical/nievecus_hr_indonesia_medical/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/nievecus_hr_indonesia_medical/nievecus_hr_indonesia_medical/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('nievecus_hr_indonesia_medical.listing', {
#             'root': '/nievecus_hr_indonesia_medical/nievecus_hr_indonesia_medical',
#             'objects': http.request.env['nievecus_hr_indonesia_medical.nievecus_hr_indonesia_medical'].search([]),
#         })

#     @http.route('/nievecus_hr_indonesia_medical/nievecus_hr_indonesia_medical/objects/<model("nievecus_hr_indonesia_medical.nievecus_hr_indonesia_medical"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('nievecus_hr_indonesia_medical.object', {
#             'object': obj
#         })