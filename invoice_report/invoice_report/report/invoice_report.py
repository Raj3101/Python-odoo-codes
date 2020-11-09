from odoo import models
import datetime

class GstrB2CSXlsx(models.AbstractModel):
    _name = 'report.invoice_report.invoice'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, invoices):

        worksheet = workbook.add_worksheet('Invoice')
        start_date = invoices.start_date
        end_date = invoices.end_date

        invoice_id = self.env['account.invoice'].search([('type','=','out_invoice'),
                                                        ('state', 'in', ['open', 'paid']),
                                                        ('date_invoice','>=',start_date),
                                                        ('date_invoice','<=',end_date)])

        worksheet.set_column('A',15)
        date_format = workbook.add_format({'num_format': 'd-mmm-yyyy'})

        row = 1

        worksheet.write('A%s' %(row), 'Invoice No.')

        for obj in invoice_id:

            worksheet.write('A%s' %(row+1), obj.sequence_number_next_prefix.vat)
            row += 1
