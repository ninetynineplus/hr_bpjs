# -*- coding: utf-8 -*-
from odoo import http

# class NievecusMedicalHospital(http.Controller):
#     @http.route('/nievecus_medical_hospital/nievecus_medical_hospital/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/nievecus_medical_hospital/nievecus_medical_hospital/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('nievecus_medical_hospital.listing', {
#             'root': '/nievecus_medical_hospital/nievecus_medical_hospital',
#             'objects': http.request.env['nievecus_medical_hospital.nievecus_medical_hospital'].search([]),
#         })

#     @http.route('/nievecus_medical_hospital/nievecus_medical_hospital/objects/<model("nievecus_medical_hospital.nievecus_medical_hospital"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('nievecus_medical_hospital.object', {
#             'object': obj
#         })