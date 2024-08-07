from odoo import api, fields, models
import requests
import json
from flask import Flask,render_template,request,redirect,url_for,flash
import sqlite3 as sql
import platform
import urllib.parse
from bs4 import BeautifulSoup
app=Flask(__name__)

class Spfli(models.Model):
   _name = 'spfli.service'
   _description = 'Flight Schedule'

   spfli_line = fields.One2many('spfli.line', 'spfli_id', string='Flight Schedule')
   MANDT = fields.Char(string='MANDT')
   CARRID = fields.Char(string='Airline Code')
   CONNID = fields.Char(string='CONNID')
   COUNTRYFR = fields.Char(string='COUNTRYFR')
   CITYFROM = fields.Char(string='CITYFROM')
   AIRPFROM = fields.Char(string='AIRPFROM')
   COUNTRYTO = fields.Char(string='COUNTRYTO')
   CITYTO = fields.Char(string='CITYTO')
   AIRPTO = fields.Char(string='AIRPTO')
   FLTIME = fields.Char(string='FLTIME')
   DEPTIME = fields.Char(string='DEPTIME')
   ARRTIME = fields.Char(string='ARRTIME')
   DISTANCE = fields.Char(string='DISTANCE')
   DISTID = fields.Char(string='DISTID')
   FLTYPE = fields.Char(string='FLTYPE')
   PERIOD = fields.Char(string='PERIOD')
   V_URL = fields.Char(string='V_URL', default='http://vhcala4hci:50000/sap/bc/abap/zzdemo_spfli?sap-client=001&carrid=')
   P_URL = fields.Char(string='URL Parm', compute='_compute_name')
   state = fields.Selection([('draft', 'Draft'), ('open', 'Open'), ('done', 'Done')], string='Status', readonly=True, default='draft')
  

   def get_spfli(self):
       self.write({'state': 'draft'})  
       for record in self:      
           record.P_URL = f"{record.V_URL or ''} {record.CARRID or ''}".strip()
       record.P_URL = record.P_URL.replace(" ", "")         
       username = 'DEVELOPER'
       password = 'ABAPtr1909'
       response = requests.get(self.P_URL, auth=(username, password)).content
       soup = BeautifulSoup(response, 'html.parser')
       for tag in soup.find_all('body'):
           json_res = json.loads(tag.text)
       rplace = []
       for item in json_res:           
           val = {'MANDT' : item["MANDT"],
                  'CARRID' : item["CARRID"],
                  'CONNID' : item["CONNID"],
                  'COUNTRYFR' : item["COUNTRYFR"] ,
                  'CITYFROM' : item["CITYFROM"],
                  'AIRPFROM' : item["AIRPFROM"],
                  'COUNTRYTO' : item["COUNTRYTO"],  
                  'CITYTO' : item["CITYTO"],
                  'AIRPTO' : item["AIRPTO"],
                  'FLTIME' : item["FLTIME"],
                  'DEPTIME' : item["DEPTIME"],
                  'ARRTIME' : item["ARRTIME"],
                  'DISTANCE' : item["DISTANCE"],
                  'DISTID' : item["DISTID"],
                  'FLTYPE' : item["FLTYPE"],
                  'PERIOD' : item["PERIOD"]}    
           rplace.append((0,0,val))          
       self.spfli_line = rplace 

class Spfli_Line(models.Model):
    _name = 'spfli.line'
    _description = 'Flight Schedule'

    spfli_id = fields.Many2one('spfli.service', string='Spfli ID')
    MANDT = fields.Char(string='MANDT')
    CARRID = fields.Char(string='CARRID')
    CONNID = fields.Char(string='CONNID')
    COUNTRYFR = fields.Char(string='COUNTRYFR')
    CITYFROM = fields.Char(string='CITYFROM')
    AIRPFROM = fields.Char(string='AIRPFROM')
    COUNTRYTO = fields.Char(string='COUNTRYTO')
    CITYTO = fields.Char(string='CITYTO')
    AIRPTO = fields.Char(string='AIRPTO')
    FLTIME = fields.Char(string='FLTIME')
    DEPTIME = fields.Char(string='DEPTIME')
    ARRTIME = fields.Char(string='ARRTIME')
    DISTANCE = fields.Char(string='DISTANCE')
    DISTID = fields.Char(string='DISTID')
    FLTYPE = fields.Char(string='FLTYPE')
    PERIOD = fields.Char(string='PERIOD')