from odoo import models

class InvoiceXlsx(models.AbstractModel):
    _name = 'report.account.invoice.resource_status'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, resource):

        sheet = workbook.add_worksheet("Invoices")
