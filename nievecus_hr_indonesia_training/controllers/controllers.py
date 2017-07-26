# -*- coding: utf-8 -*-
from odoo import http

# class NievecusHrIndonesiaTraining(http.Controller):
#     @http.route('/nievecus_hr_indonesia_training/nievecus_hr_indonesia_training/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/nievecus_hr_indonesia_training/nievecus_hr_indonesia_training/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('nievecus_hr_indonesia_training.listing', {
#             'root': '/nievecus_hr_indonesia_training/nievecus_hr_indonesia_training',
#             'objects': http.request.env['nievecus_hr_indonesia_training.nievecus_hr_indonesia_training'].search([]),
#         })

#     @http.route('/nievecus_hr_indonesia_training/nievecus_hr_indonesia_training/objects/<model("nievecus_hr_indonesia_training.nievecus_hr_indonesia_training"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('nievecus_hr_indonesia_training.object', {
#             'object': obj
#         })