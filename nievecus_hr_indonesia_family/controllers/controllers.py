# -*- coding: utf-8 -*-
from odoo import http

# class NievecusHrIndonesiaFamily(http.Controller):
#     @http.route('/nievecus_hr_indonesia_family/nievecus_hr_indonesia_family/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/nievecus_hr_indonesia_family/nievecus_hr_indonesia_family/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('nievecus_hr_indonesia_family.listing', {
#             'root': '/nievecus_hr_indonesia_family/nievecus_hr_indonesia_family',
#             'objects': http.request.env['nievecus_hr_indonesia_family.nievecus_hr_indonesia_family'].search([]),
#         })

#     @http.route('/nievecus_hr_indonesia_family/nievecus_hr_indonesia_family/objects/<model("nievecus_hr_indonesia_family.nievecus_hr_indonesia_family"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('nievecus_hr_indonesia_family.object', {
#             'object': obj
#         })