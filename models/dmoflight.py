from odoo import api, fields, models
import requests
import json
from flask import Flask,render_template,request,redirect,url_for,flash
import sqlite3 as sql
import platform
import urllib.parse
from bs4 import BeautifulSoup
app=Flask(__name__)

class Dmoflight(models.Model):
   _name = 'dmoflight.service'
   _description = 'Flight Reference'

   dmoflight_line = fields.One2many('dmoflight.line', 'dmoflight_id', string='DmoFlight ID')
   CLIENT = fields.Char(string='CLIENT')
   CARRIER_ID = fields.Char(string='Carrier ID')
   CONNECTION_ID = fields.Char(string='Connection ID')
   FLIGHT_DATE = fields.Char(string='Flight Date')
   PRICE = fields.Char(string='Flight Price')
   CURRENCY_CODE = fields.Char(string='Currency Code')
   PLANE_TYPE_ID = fields.Char(string='Plane Type ID')
   SEATS_MAX = fields.Char(string='Plane Seats Max')
   SEATS_OCCUPIED = fields.Char(string='Plane Seats Occupied')
   V_URL = fields.Char(string='V_URL', default='http://vhcala4hci:50000/sap/bc/abap/zzdemo_flight?sap-client=001&carrier_id=')
   P_URL = fields.Char(string='URL Parm', compute='_compute_name')
   state = fields.Selection([('draft', 'Draft'), ('open', 'Open'), ('done', 'Done')], string='Status', readonly=True, default='draft')
  

   def get_dmoflight(self):
       self.write({'state': 'draft'})  
       for record in self:      
           record.P_URL = f"{record.V_URL or ''} {record.CARRIER_ID or ''}".strip()
       record.P_URL = record.P_URL.replace(" ", "")         
       username = 'DEVELOPER'
       password = 'ABAPtr1909'
       response = requests.get(self.P_URL, auth=(username, password)).content
       soup = BeautifulSoup(response, 'html.parser')
       print('====debugg=====', response)
       for tag in soup.find_all('body'):
           json_res = json.loads(tag.text)
       rplace = []
       for item in json_res:           
           val = {'CLIENT' : item["CLIENT"],
                  'CARRIER_ID' : item["CARRIER_ID"],
                  'CONNECTION_ID' : item["CONNECTION_ID"],
                  'FLIGHT_DATE' : item["FLIGHT_DATE"] ,
                  'PRICE' : item["PRICE"],
                  'CURRENCY_CODE' : item["CURRENCY_CODE"],
                  'PLANE_TYPE_ID' : item["PLANE_TYPE_ID"],  
                  'SEATS_MAX' : item["SEATS_MAX"],
                  'SEATS_OCCUPIED' : item["SEATS_OCCUPIED"]}    
           rplace.append((0,0,val))          
       self.dmoflight_line = rplace 

class Dmoflight_Line(models.Model):
    _name = 'dmoflight.line'
    _description = 'Flight Reference'

    dmoflight_id = fields.Many2one('dmoflight.service', string='DmoFlight ID')
    CLIENT = fields.Char(string='CLIENT')
    CARRIER_ID = fields.Char(string='CARRIER_ID')
    CONNECTION_ID = fields.Char(string='CONNECTION_ID')
    FLIGHT_DATE = fields.Char(string='FLIGHT_DATE')
    PRICE = fields.Char(string='PRICE')
    CURRENCY_CODE = fields.Char(string='CURRENCY_CODE')
    PLANE_TYPE_ID = fields.Char(string='PLANE_TYPE_ID')
    SEATS_MAX = fields.Char(string='SEATS_MAX')
    SEATS_OCCUPIED = fields.Char(string='SEATS_OCCUPIED')