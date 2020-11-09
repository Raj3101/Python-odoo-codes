from odoo import models
import datetime

class InvReport(models.AbstractModel):
    _name = 'report.invoice_report.invreport'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, invoices):

        worksheet = workbook.add_worksheet('Invoice')
        start_date = invoices.start_date
        end_date = invoices.end_date

        invoice_id = self.env['account.invoice'].search([('date_invoice','>=',start_date),
                                                        ('date_invoice','<=',end_date)])


        worksheet.set_column('A:B',15)
        date_format = workbook.add_format({'num_format': 'd-mmm-yyyy'})

        row = 1
        col = 0
        new_row = row + 1


        worksheet.write('A%s' %(row), 'Invoice No.')

        for obj in invoice_id:
            worksheet.write('A%s' %(new_row), obj.number)
            new_row += 1
