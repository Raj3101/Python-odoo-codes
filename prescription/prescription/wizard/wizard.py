#-*- coding: utf-8 -*-
from odoo import models, fields, api,_

class wizard(models.TransientModel):
    _name = "prescription.wizard"

    name = fields.Many2one('res.partner',string='Patient Name', store=True)
    diagnosis = fields.Char(string='Diagnosis', store=True)
    age = fields.Float(string='Age')
    date = fields.Date(string='Date')
    visitagain = fields.Boolean(string='Visit Again')
    int_id = fields.One2many('wizard.line','ext_id', string='Medicine Line')


    @api.multi                      #fro creating a new form id and add its one2many field value
    def insert_data(self):
        obj = self.env['prescriptions.prescription'].create({'name':self.name.id,
                                                             'diagnosis': self.diagnosis,
                                                             'age':self.age,
                                                             'date':self.date,
                                                             'visitagain':self.visitagain})
        var = self.env['prescriptions.prescription'].search([('name','=',self.name.id)])
        for i in self.int_id:
            var.write({'medicine_id': [(0,0, {'medicine':i.medicine.id,
                                              'dosage':i.dosage,
                                              'qty':i.qty,
                                              'refillinterval':i.refillinterval,
                                              'morning':i.morning,
                                              'afternoon':i.afternoon,
                                              'evening':i.evening,
                                              'time':i.time})]
                       })


class WizardLine(models.TransientModel):
    _name = "wizard.line"

    ext_id = fields.Many2one('prescription.wizard')
    medicine = fields.Many2one('product.product', string='Medicine Name')
    dosage = fields.Char(string='Dosage')
    qty = fields.Float(string='quntity', required=True, default=1)
    refillinterval = fields.Integer(string='Refill Interval')
    morning = fields.Boolean(string='Morning')
    afternoon = fields.Boolean(string='AfterNoon')
    evening = fields.Boolean(string='Evening')
    time = fields.Selection(selection=[('before','Before Meal'), ('after','After Meal')], string='Before/After Meal')
