#-*- coding: utf-8 -*-
from odoo import models, fields, api,_

class wizard(models.TransientModel):
    _name = "sale.wizard"

    name = fields.Many2one('product.product', string='Name', store=True)
    customer = fields.Many2one('res.partner', string='Customer', store=True)
    quantity = fields.Integer(string="Quantity", store=True, default=1)

    @api.multi
    @api.onchange('name.qty_available','quantity')
    def create_sale_order(self):
        for i in self.name:
            new_qty = i.qty_available - self.quantity
            i.qty_available = new_qty
            print(i.qty_available)
            i.write({'qty_available':new_qty})

    @api.multi
    def open_msg_wizard(self):
        view_id = self.env.ref('pump.msg_wizard_view').id
        return {
            'name': _('msg wizard'),
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'msg.wizard',
            'view_id': self.env.ref('pump.msg_wizard_view').id,
            'type': 'ir.actions.act_window',
            'context': {'default_quantity': self.quantity},
            'target': 'new',
                }



