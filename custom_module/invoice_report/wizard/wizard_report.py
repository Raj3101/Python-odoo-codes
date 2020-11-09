# -*- coding: utf-8 -*-
from odoo import api, models, fields, _
import datetime

class WizardInvoice(models.TransientModel):
    _name = 'wizard.invoice'

    start_date = fields.Date('From Date', default=fields.Datetime.now(), required=True)
    end_date = fields.Date('To Date', default=fields.Datetime.now(), required=True)

    @api.multi
    def open_tree_view(self, data):
        self.ensure_one()
        treeview_id = self.env.ref('account.invoice_tree').id
        return {
              "name": 'Filter Data',
              "type": "ir.actions.act_window",
              "res_model": "account.invoice",
              "views": [[False,"tree"]],
              "target": "current",
              "domain" : ([('date_invoice','>=',self.start_date),('date_invoice','<=',self.end_date)]),
                }

