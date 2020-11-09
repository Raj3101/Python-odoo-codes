# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class MyConfigWizard(models.Model):
    _inherit = 'sale.order'


    shipping_type = fields.Selection(selection=[('air','Air'),
                                                ('rail','Rail'),
                                                ('transport','Transport'),
                                                ('ship','Ship')],
                                                string='Shiping')
    
