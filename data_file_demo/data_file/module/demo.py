# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class demo(models.Model):
    _name = "demo.demo"

    name = fields.Char(string='Name')
    city = fields.Char(string='City')










#this module is created for add some reords automatically at the time installation of module
