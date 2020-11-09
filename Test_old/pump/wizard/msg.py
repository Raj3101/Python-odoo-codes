# -*- coding: utf-8 -*-
from odoo import models, fields, api

class wizard(models.TransientModel):
    _name = "msg.wizard"
    _inherit = "sale.wizard"

    msg = fields.Text(string="Your Selling is done", readonly=True, store=True)
    quantity = fields.Float(string="qty", readonly=True)



