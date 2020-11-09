#-*- coding: utf-8 -*-
from odoo import models, fields, api,_

class ProductWizard(models.TransientModel):
    _name = "product.wizard"

    product_name = fields.Char(string='Name')
    external_id = fields.One2many('product.line','internal_id')


    @api.multi                                # For create multiple new products in products from wizard
    def product_data(self):
        for i in self.external_id:
            obj = i.env['product.template'].create({'name':i.full_name,
                                                   'standard_price': i.cost,
                                                   'default_code': i.referance,
                                                   'categ_id':i.category.id})

class Product(models.TransientModel):
    _name = "product.line"

    internal_id = fields.Many2one('product.wizard', string="XYZ")
    name_product = fields.Char(string='Product Name')
    cost = fields.Float(string='Cost')
    referance = fields.Char(string='Referance')
    category = fields.Many2one('product.category')
    full_name = fields.Char(compute='get_name')

    @api.depends('internal_id','name_product')        #for merge two diffrent name fields value
    def get_name(self):
        for i in self:
            i.full_name = str(i.internal_id.product_name) + '/' + str(i.name_product)
        
