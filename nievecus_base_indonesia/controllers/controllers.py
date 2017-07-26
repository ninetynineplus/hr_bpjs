# -*- coding: utf-8 -*-
from odoo import http

# class NievecusBaseIndonesia(http.Controller):
#     @http.route('/nievecus_base_indonesia/nievecus_base_indonesia/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/nievecus_base_indonesia/nievecus_base_indonesia/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('nievecus_base_indonesia.listing', {
#             'root': '/nievecus_base_indonesia/nievecus_base_indonesia',
#             'objects': http.request.env['nievecus_base_indonesia.nievecus_base_indonesia'].search([]),
#         })

#     @http.route('/nievecus_base_indonesia/nievecus_base_indonesia/objects/<model("nievecus_base_indonesia.nievecus_base_indonesia"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('nievecus_base_indonesia.object', {
#             'object': obj
#         })