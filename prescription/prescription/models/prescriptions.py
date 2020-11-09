# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime


class prescription(models.Model):
    _name = "prescriptions.prescription"
    _inherit = 'mail.thread'
    _order = "date desc, count"

    count = fields.Integer()
    name = fields.Many2one('res.partner', string='Patient Name', track_visibility='always')
    color = fields.Integer('Color')
    age = fields.Float(string='Age')
    diagnosis = fields.Char(string='Diagnosis', track_visibility='always')
    date = fields.Date(string='Date', default=datetime.today())
    visitagain = fields.Boolean(string='Visit Again')
    medicine_id = fields.One2many('prescriptions.line','medicines_id', string='Medicine Line')
    visitdate = fields.Date(string='Visit Date', default=datetime.today())
    totalqty = fields.Float(compute='get_total_qty', string='Total Quantity', track_visibility='always')
    mobile = fields.Char(string='Mobile', readonly=True)
    seq = fields.Char(readonly=True, index=True, default="New", string="Case No")
    active = fields.Boolean('Active', default=True, help="If unchecked, it will allow you to hide the product without removing it.")
    count_attachment = fields.Integer(compute='count_attachments')
    ir_ids = fields.One2many('ir.attachment', 'attachment_id', string='Task')
    state = fields.Selection([
        ('open', 'Open'),
        ('done', 'Done'),
        ], string='Status', readonly=True, copy=False, index=True, track_visibility='onchange', default='open')


    @api.model                           #for seqencing of form view
    def create(self, vals):
        if vals.get('seq', _('New')) == _('New'):
            if 'seq' in vals:
                vals['seq'] = self.env['ir.sequence'].next_by_code('prescriptions.prescription') or _('New')
            else:
                vals['seq'] = self.env['ir.sequence'].next_by_code('prescriptions.prescription') or _('New')
        vals['visitagain'] = True
        return super(prescription,self).create(vals)


    @api.multi                   #for write state in statusbar
    def action_done(self):
        return self.write({'state': 'done'})

    @api.depends('medicine_id')  #for calculate total qantity
    def get_total_qty(self):
        for i in self:
            i.totalqty = sum(i.medicine_id.mapped('qty'))

    @api.onchange('name')     #for fetching mobile number from customer form view
    def get_mobile(self):
        self.mobile = self.name.mobile

    @api.depends('count_attachment')   #for calculate how many file/url attachments available for that id
    def count_attachments(self):
        for i in self:
            attachment = i.env['ir.attachment'].search([('attachment_id', '=', i.id)])
            i.count_attachment = len(attachment)

    @api.multi                         #for attach new file/url to that id
    def attachment(self):
        self.ensure_one()
        return{
              "name": 'Attachment',
              "type": "ir.actions.act_window",
              "res_model": "ir.attachment",
              "views": [[False,"form"]],
              "context":  {'default_attachment_id': self.id},
              "target": "current",
                }

    @api.multi
    def attachment_kanban(self):     #for open a kanban view of ir.attachment for that id
        self.ensure_one()
        return{
            'type': 'ir.actions.act_window',
            'name': _('Attachments'),
            'res_model': 'ir.attachment',
            "views": [[False,'kanban']],
            'target': 'current',
            'domain': [('attachment_id', '=', self.id)],
            }
    @api.multi                     #for creating automatically sale order for that id
    def create_sale_order(self):
        print("+++++++++++++++++")
        obj = self.env['sale.order'].create({'partner_id':self.name.id})
        var = self.env['sale.order'].search([('partner_id','=',self.name.id)])
        for i in self.medicine_id:
            var.write({'order_line': [(0,0, {'product_id':i.medicine.id,
                                              'product_uom_qty':i.qty,})]
                      })

class prescriptionLine(models.Model):
    _name = "prescriptions.line"

    count = fields.Integer()
    medicines_id = fields.Many2one('prescriptions.prescription')
    medicine = fields.Many2one('product.product', string='Medicine Name')
    dosage = fields.Char(string='Dosage')
    qty = fields.Float(string='quntity', required=True, default=1)
    refillinterval = fields.Integer(string='Refill Interval')
    morning = fields.Boolean(string='Morning')
    afternoon = fields.Boolean(string='AfterNoon')
    evening = fields.Boolean(string='Evening')
    time = fields.Selection(selection=[('before','Before Meal'), ('after','After Meal')], string='Before/After Meal')

class patient(models.Model):
    _inherit = "res.partner"

    patient = fields.Boolean(string='Is Patient')
    prescription_count = fields.Integer(compute='compute_prescription_count', string='prescription', default=0)

    @api.depends('prescription_count')       #for counting number of prescription for that id
    def compute_prescription_count(self):
        for i in self:
            prescription_data = i.env['prescriptions.prescription'].search([('name', '=', i.id)])
            i.prescription_count = len(prescription_data)

    @api.multi
    def open_tree_view(self):               #for opaning a tree view of prescriptions for that id
        return{
              "name": 'Filter Data',
              "type": "ir.actions.act_window",
              "res_model": "prescriptions.prescription",
              "views": [[False,"tree"]],
              "target": "current",
              "domain" : [('name', '=', self.id)],
                }

class attachment(models.Model):
    _inherit = "ir.attachment"

    attachment_id = fields.Many2one('prescriptions.prescription', string='id')



