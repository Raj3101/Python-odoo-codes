#-*- coding: utf-8 -*-
from odoo import models, fields, api,_

class FormData(models.TransientModel):
    _name = "form.data"

    name = fields.Many2one('res.partner',string='Patient Name', store=True)
    diagnosis = fields.Char(string='Diagnosis', store=True)
    age = fields.Float(string='Age')
    date = fields.Date(string='Date')
    visitagain = fields.Boolean(string='Visit Again')

    @api.multi              #for opaning a new form view of prescription with some filled values that entered in wizard
    def form_data(self):
        return {
              "name": 'Filter Data',
              "type": "ir.actions.act_window",
              "res_model": "prescriptions.prescription",
              "views": [[False,"form"]],
              "context": {"default_name": self.name.id,
                          "default_diagnosis": self.diagnosis,
                          "default_age": self.age,
                          "default_date": self.date,
                          "default_visitagain": self.visitagain,
                          },
              "target": "current",
                }

