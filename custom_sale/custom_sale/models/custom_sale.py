# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime

class CustomSale(models.Model):
    _inherit = "sale.order"

    date_planned = fields.Datetime(string='Scheduled Date')
    min_date = fields.Datetime(compute='compute_date_planned', string='min_date')

    @api.multi
    def action_set_date_planned(self):
        for order in self:
            order.order_line.update({'date_planned': order.date_planned})

    @api.depends('order_line.date_planned')
    def compute_date_planned(self):
        for order in self:
            self.min_date = False
            for line in order.order_line:
                if not self.min_date or line.date_planned > self.min_date:
                    self.min_date = line.date_planned
        # var = self.env['stock.picking'].search([('partner_id','=',self.partner_id.id)])
        # print('----------------------', var)
        # for i in self.order_line:
        #     obj = var.write({'scheduled_date' : i.min_date})
        #     print('-----------++++-----------', obj)

    @api.multi
    def action_view_delivery(self):
        '''
        This function returns an action that display existing delivery orders
        of given sales order ids. It can either be a in a list or in a form
        view, if there is only one delivery order to show.
        '''
        action = self.env.ref('stock.action_picking_tree_all').read()[0]

        pickings = self.mapped('picking_ids')
        if len(pickings) > 1:
            action['domain'] = [('id', 'in', pickings.ids)]
        elif pickings:
            action['views'] = [(self.env.ref('stock.view_picking_form').id, 'form')]
            action['res_id'] = pickings.id
        elif
        return action


class CustomSaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    date_planned = fields.Datetime(string='Scheduled Date', default=datetime.now())
    
