# -*- coding: utf-8 -*-
from ast import literal_eval
from odoo import models, fields, api, _

class MyConfigWizard(models.TransientModel):
    _inherit = 'res.config.settings'


    shipping_type = fields.Boolean("Shipping Type")


    @api.onchange('shipping_type')
    def actio_done(self):
        irModuleObj = self.env['ir.module.module']
        irModuleObj.update_list()
        moduleIds = self.env['ir.module.module'].search(
                                   [
                                    ('name', '=', 'auto_install')
                                   ]
                                  )
        if moduleIds:
            moduleIds[0].button_immediate_install()
