# -*- coding: utf-8 -*-
from odoo import http

# class NievecusHrIndonesiaEducation(http.Controller):
#     @http.route('/nievecus_hr_indonesia_education/nievecus_hr_indonesia_education/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/nievecus_hr_indonesia_education/nievecus_hr_indonesia_education/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('nievecus_hr_indonesia_education.listing', {
#             'root': '/nievecus_hr_indonesia_education/nievecus_hr_indonesia_education',
#             'objects': http.request.env['nievecus_hr_indonesia_education.nievecus_hr_indonesia_education'].search([]),
#         })

#     @http.route('/nievecus_hr_indonesia_education/nievecus_hr_indonesia_education/objects/<model("nievecus_hr_indonesia_education.nievecus_hr_indonesia_education"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('nievecus_hr_indonesia_education.object', {
#             'object': obj
#         })