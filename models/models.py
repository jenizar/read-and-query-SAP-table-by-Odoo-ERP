# -*- coding: utf-8 -*-

from odoo import api, fields, models
 
class TravelService(models.Model):
    _name = 'travel.service'
    _description = 'Travel Service'
     
    name = fields.Char(string='Travel Service', required=True)
    description = fields.Text(string='Description')