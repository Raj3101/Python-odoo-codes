from odoo import models
import re

class InvoiceXlsx(models.AbstractModel):
    _name = 'report.prescription.report_invoice'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, invoices):
        sheet = workbook.add_worksheet("InvoiceXlsx")
        sheet.set_column('A:B',14)
        sheet.set_column('C:D',10)
        sheet.set_column('E:F',14)

        header1 = '&LYour LOGO'
        footer1 = '&C&P&L&A'
        sheet.set_header(header1)
        sheet.set_footer(footer1)

        merge_format = workbook.add_format({
            'bold': 1,
            'align': 'left',
            'valign': 'vcenter',})
        merge_format1 = workbook.add_format({
            'bold': 1,
            'align': 'left',
            'valign': 'vcenter'})
        merge_format2 = workbook.add_format({
            'bold': 1,
            'underline':1,
            'align': 'left',
            'valign': 'vcenter',})
        merge_format3 = workbook.add_format({
            'bold': 1,
            'bottom': 1,
            'align': 'left',
            'valign': 'vcenter'})
        merge_format4 = workbook.add_format({
            'bold': 1,
            'bottom': 1,
            'align': 'right',
            'valign': 'vcenter'})
        merge_format5 = workbook.add_format({
            'bold': 1,
            'top': 1,
            'align': 'left',
            'valign': 'vcenter'})
        merge_format6 = workbook.add_format({
            'bold': 1,
            'top': 1,
            'align': 'right',
            'valign': 'vcenter'})
        merge_format7 = workbook.add_format({
            'bold': 1,
            'align': 'right',
            'valign': 'vcenter'})
        merge_format.set_font_size(20)

        row = 1

        for obj in invoices:
                sheet.merge_range('A%s:B%s' %(row + 1,row + 1),self.env.user.company_id.partner_id.name,merge_format1)
                sheet.merge_range('A%s:B%s' %(row + 2,row + 2),obj.partner_id.street,merge_format1)
                sheet.merge_range('A%s:B%s' %(row + 3,row + 3),obj.partner_id.street2,merge_format1)
                sheet.merge_range('A%s:B%s' %(row + 4,row + 4),obj.partner_id.city ,merge_format1)
                sheet.merge_range('A%s:B%s' %(row + 5,row + 5),(obj.partner_id.zip + ', ' + obj.partner_id.country_id.name),merge_format2)


                sheet.write('E%s' %(row + 6),self.env.user.partner_id.name,merge_format1)
                sheet.write('E%s' %(row + 7),self.env.user.company_id.street,merge_format1)
                sheet.write('E%s' %(row + 8),self.env.user.company_id.street2,merge_format1)
                sheet.write('E%s' %(row + 9),(self.env.user.company_id.city + ', ' + self.env.user.company_id.state_id.name),merge_format1)
                sheet.write('E%s' %(row + 10),(self.env.user.company_id.zip + ', ' + self.env.user.company_id.country_id.name),merge_format2)

                sheet.merge_range('A%s:B%s' %(row+12,row+12),'Customer Invoices',merge_format)
                sheet.merge_range('C%s:E%s' %(row+12,row+12), obj.number,merge_format)

                sheet.write('A%s' %(row+16), 'Invoice_date:',merge_format1)
                sheet.write('B%s' %(row+16), obj.date_invoice,merge_format1)
                sheet.write('E%s' %(row+16), 'Due_date:',merge_format7)
                sheet.write('F%s' %(row+16), obj.date_due,merge_format7)

                sheet.merge_range('A%s:B%s' %(row + 19,row + 19), 'Description',merge_format3)
                sheet.write('C%s' %(row+19), 'Quntity',merge_format4)
                sheet.write('D%s' %(row+19), 'Unit Price',merge_format4)
                sheet.write('E%s' %(row+19), 'Tax',merge_format4)
                sheet.write('F%s' %(row+19), 'Amount',merge_format4)

                for invoice_line in obj.invoice_line_ids:

                    sheet.merge_range('A%s:B%s' %(row + 20,row + 20), invoice_line.name,merge_format1)
                    sheet.write('C%s' %(row+20), invoice_line.quantity,merge_format7)
                    sheet.write('D%s' %(row+20), invoice_line.price_unit,merge_format7)
                    sheet.write('E%s' %(row+20), ', '.join(map(lambda x:(x.name),invoice_line.invoice_line_tax_ids)),merge_format7)
                    sheet.write('F%s' %(row+20), invoice_line.price_subtotal,merge_format7)
                    row+=2


                sheet.write('E%s' %(row+23), 'Amount:',merge_format5)
                sheet.write('F%s' %(row+23), obj.amount_untaxed,merge_format6)
                sheet.write('E%s' %(row+24), 'Tax:',merge_format1)
                sheet.write('F%s' %(row+24), obj.amount_tax,merge_format7)
                sheet.write('E%s' %(row+25), 'Total:',merge_format5)
                sheet.write('F%s' %(row+25), obj.amount_total,merge_format6)





        
