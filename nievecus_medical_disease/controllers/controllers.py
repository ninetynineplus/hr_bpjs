# -*- coding: utf-8 -*-
from odoo import http

# class NievecusMedicalDisease(http.Controller):
#     @http.route('/nievecus_medical_disease/nievecus_medical_disease/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/nievecus_medical_disease/nievecus_medical_disease/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('nievecus_medical_disease.listing', {
#             'root': '/nievecus_medical_disease/nievecus_medical_disease',
#             'objects': http.request.env['nievecus_medical_disease.nievecus_medical_disease'].search([]),
#         })

#     @http.route('/nievecus_medical_disease/nievecus_medical_disease/objects/<model("nievecus_medical_disease.nievecus_medical_disease"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('nievecus_medical_disease.object', {
#             'object': obj
#         })