#-*- coding: utf-8 -*-
from odoo import models, fields, api,_

class UpdateWizard(models.TransientModel):
    _name = "prescription.updatewizard"

    customer_id = fields.Many2one('prescriptions.prescription',string='Patient Name', store=True)
    diagnosis = fields.Char(string='Diagnosis', store=True)
    age = fields.Float(string='Age')
    date = fields.Date(string='Date')
    visitagain = fields.Boolean(string='Visit Again')

    @api.multi                                  #for add values in some id from wizard
    def update_data(self):
        obj = self.customer_id.write({'diagnosis': self.diagnosis,
                                                            'age':self.age,
                                                            'date':self.date,
                                                            'visitagain':self.visitagain})


