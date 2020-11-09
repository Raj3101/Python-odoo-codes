# -*- coding: utf-8 -*-
from odoo import models, fields, api

class pump(models.Model):
    _name = "pumps.pump"

    name = fields.Many2one('product.product', string='Name', store=True)
    pump_quntity = fields.Integer(string='model')
    product_id = fields.One2many('pumps.pump.line','pump_id', string='Product')
    price = fields.Float(compute='get_total_amount', string='Price')
    profit = fields.Float(string='Profit', store=True)
    cost_profit = fields.Float(compute='get_product_profit', string='Cost Profit')
    manufacturing_cost = fields.Float(compute='get_manufacturing_cost', string='Manufacturing_Cost')
    fetched_data = fields.Float(compute='get_fetched_data',string='Fetched data')

    @api.depends('product_id')
    def get_product_profit(self):
        for i in self:
            i.cost_profit = sum(i.product_id.mapped('price_costtotal')) - sum(i.product_id.mapped('price_subtotal'))

    @api.depends('product_id','profit','cost_profit')
    def get_total_amount(self):
        for i in self:
            i.price = sum(i.product_id.mapped('price_subtotal')) + i.profit + i.cost_profit

    @api.depends('profit')
    def get_fetched_data(self):
        self.fetched_data = self.profit

    @api.depends('product_id')
    def get_manufacturing_cost(self):
        for i in self:
            i.manufacturing_cost = sum(i.product_id.mapped('price_subtotal'))



class pump_line(models.Model):
    _name = "pumps.pump.line"

    pump_id = fields.Many2one('pumps.pump', string= 'Id')
    component = fields.Many2one('product.product', string='Component', store=True)
    standard_price = fields.Float(string='Price Unit', store=True)
    list_price = fields.Float(string='Sale Price', store=True)
    qty = fields.Integer(string='quntity', required=True, store=True, default=1)
    price_subtotal = fields.Float(compute="get_price_subtotal", string='Sub Total',store=True)
    price_costtotal = fields.Float(compute="get_price_costtotal", string='cost Total',store=True)
    amount = fields.Integer(compute='get_total_amount',string='price', store=True)

    @api.onchange('component')
    def get_product_price(self):
        self.standard_price = self.component.standard_price
        self.list_price = self.component.list_price

    @api.depends('standard_price','qty')
    def get_price_subtotal(self):
        for i in self:
            i.price_subtotal = i.standard_price * i.qty

    @api.depends('list_price','qty')
    def get_price_costtotal(self):
        for i in self:
            i.price_costtotal = i.list_price * i.qty
























   
