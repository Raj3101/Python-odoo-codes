from odoo import models
from datetime import datetime, date
import datetime
import re

class GstrGSTR1Xlsx(models.AbstractModel):
    _name = 'report.gst.gstr1'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, invoices):

        start_date = invoices.start_date
        end_date = invoices.end_date

        invoice_id = self.env['account.invoice'].search([('type','=','out_invoice'),
                                                        ('state', 'in', ['open', 'paid']),
                                                        ('date_invoice','>=',start_date),
                                                        ('date_invoice','<=',end_date)])

        debit_note = self.env['debit.note'].search([('state', 'in', ['validate',]),
                                                   ('date','>=',start_date),
                                                   ('date','<=',end_date)])

        credit_note = self.env['credit.note'].search([('state', 'in', ['validate',]),
                                                     ('date','>=',start_date),
                                                     ('date','<=',end_date)])

        VALUES = [('discount','02-Post Sale Discount'),
            ('deficiency','03-Deficiency in services'),
            ('correction','04-Correction in Invoice'),
            ('pos' , '05-Change in POS'),
            ('assessment','06-Finalization of Provisional assessment'),
            ('others','07-Others'),]

        worksheet_b2b = workbook.add_worksheet('b2b')
        worksheet_b2cl = workbook.add_worksheet('b2cl')
        worksheet_b2cs = workbook.add_worksheet('b2cs')
        worksheet_hsn = workbook.add_worksheet('hsn')
        # worksheet_export = workbook.add_worksheet('export')
        worksheet_cdn = workbook.add_worksheet('cdnr')
        worksheet_cdnur = workbook.add_worksheet('cdnur')

        worksheet_b2b.set_column('A:K',15)
        worksheet_b2cl.set_column('A:H',15)
        worksheet_b2cs.set_column('A:H',15)
        worksheet_hsn.set_column('A:H',15)
        # worksheet_export.set_column('A:K',15)
        worksheet_cdn.set_column('A:L',15)
        worksheet_cdnur.set_column('A:L',15)

        date_format = workbook.add_format({'num_format': 'd-mmm-yyyy'})

        row = 1
        col = 0
        new_row = row + 1

        # B2B
        worksheet_b2b.write('A%s' %(row), 'GSTIN/UIN of Recipient')
        worksheet_b2b.write('B%s' %(row), 'Invoice Number')
        worksheet_b2b.write('C%s' %(row), 'Invoice date')
        worksheet_b2b.write('D%s' %(row), 'Invoice Value')
        worksheet_b2b.write('E%s' %(row), 'Place Of Supply')
        worksheet_b2b.write('F%s' %(row), 'Reverse Charge')
        worksheet_b2b.write('G%s' %(row), 'Invoice Type')
        worksheet_b2b.write('H%s' %(row), 'E-Commerce GSTIN')
        worksheet_b2b.write('I%s' %(row), 'Rate')
        worksheet_b2b.write('J%s' %(row), 'Taxable Value')
        worksheet_b2b.write('K%s' %(row), 'Cess Amount')

        # B2CL
        worksheet_b2cl.write('A%s' %(row), 'Invoice Number')
        worksheet_b2cl.write('B%s' %(row), 'Invoice date')
        worksheet_b2cl.write('C%s' %(row), 'Invoice Value')
        worksheet_b2cl.write('D%s' %(row), 'Place Of Supply')
        worksheet_b2cl.write('E%s' %(row), 'Rate')
        worksheet_b2cl.write('F%s' %(row), 'Taxable Value')
        worksheet_b2cl.write('G%s' %(row), 'Cess Amount')
        worksheet_b2cl.write('H%s' %(row), 'E-Commerce GSTIN')

        # B2CS
        worksheet_b2cs.write('A%s' %(row), 'Type')
        worksheet_b2cs.write('B%s' %(row), 'Place Of Supply')
        worksheet_b2cs.write('C%s' %(row), 'Rate')
        worksheet_b2cs.write('D%s' %(row), 'Taxable Value')
        worksheet_b2cs.write('E%s' %(row), 'Cess Amount')
        worksheet_b2cs.write('F%s' %(row), 'E-Commerce GSTIN')

        # HSN
        worksheet_hsn.write('A%s' %(row), 'HSN')
        worksheet_hsn.write('B%s' %(row), 'Description')
        worksheet_hsn.write('C%s' %(row), 'UQC')
        worksheet_hsn.write('D%s' %(row), 'Total Quantity')
        worksheet_hsn.write('E%s' %(row), 'Total Value')
        worksheet_hsn.write('F%s' %(row), 'Taxable Value')
        worksheet_hsn.write('G%s' %(row), 'Integrated Tax Amount')
        worksheet_hsn.write('H%s' %(row), 'Central Tax Amount')
        worksheet_hsn.write('I%s' %(row), 'State/UT Tax Amount')
        worksheet_hsn.write('J%s' %(row), 'Cess Amount')

        # Export
        # worksheet_export.write('A%s' %(row), 'Export Type')
        # worksheet_export.write('B%s' %(row), 'Invoice Number')
        # worksheet_export.write('C%s' %(row), 'Invoice Date')
        # worksheet_export.write('D%s' %(row), 'Invoice Value')
        # worksheet_export.write('E%s' %(row), 'Port Code')
        # worksheet_export.write('F%s' %(row), 'Shipping Bill No.')
        # worksheet_export.write('G%s' %(row), 'Shipping Bill Date')
        # worksheet_export.write('H%s' %(row), 'Rate')
        # worksheet_export.write('I%s' %(row), 'Taxable Value')

        # CDN
        worksheet_cdn.write('A%s' %(row), 'GSTIN of Supplier')
        worksheet_cdn.write('B%s' %(row), 'Note/Refund Voucher Number')
        worksheet_cdn.write('C%s' %(row), 'Note/Refund Voucher date')
        worksheet_cdn.write('D%s' %(row), 'Invoice/Advance Payment Voucher Number')
        worksheet_cdn.write('E%s' %(row), 'Invoice/Advance Payment Voucher date')
        worksheet_cdn.write('F%s' %(row), 'Pre GST')
        worksheet_cdn.write('G%s' %(row), 'Document Type')
        worksheet_cdn.write('H%s' %(row), 'Reason For Issuing document')
        worksheet_cdn.write('I%s' %(row), 'Note/Refund Voucher Value')
        worksheet_cdn.write('J%s' %(row), 'Rate')
        worksheet_cdn.write('K%s' %(row), 'Taxable Value')
        worksheet_cdn.write('L%s' %(row), 'Cess Amount')

        # CDNUR
        worksheet_cdnur.write('A%s' %(row), 'UR Type')
        worksheet_cdnur.write('B%s' %(row), 'Note/Refund Voucher Number')
        worksheet_cdnur.write('C%s' %(row), 'Note/Refund Voucher date')
        worksheet_cdnur.write('D%s' %(row), 'Document Type')
        worksheet_cdnur.write('E%s' %(row), 'Invoice/Advance Receipt Number')
        worksheet_cdnur.write('F%s' %(row), 'Invoice/Advance Receipt date')
        worksheet_cdnur.write('G%s' %(row), 'Place Of Supply')
        worksheet_cdnur.write('H%s' %(row), 'Note/Refund Voucher Value')
        worksheet_cdnur.write('I%s' %(row), 'Applicable % of Tax Rate')
        worksheet_cdnur.write('J%s' %(row), 'Rate')
        worksheet_cdnur.write('K%s' %(row), 'Taxable Value')
        worksheet_cdnur.write('L%s' %(row), 'Cess Amount')
        worksheet_cdnur.write('M%s' %(row), 'Pre GST')


        # B2B Report
        ls = []
        for obj in invoice_id:
            if obj.export_invoice == False and obj.partner_id.vat:
                for rec in obj.invoice_line_ids:
                    if rec.invoice_line_tax_ids:
                        for line in rec.invoice_line_tax_ids:
                            if line.children_tax_ids:
                                if sum(line.children_tax_ids.mapped('amount')) == 1:
                                    ls.append(1)
                                if sum(line.children_tax_ids.mapped('amount')) == 2:
                                    ls.append(2)
                                if sum(line.children_tax_ids.mapped('amount')) == 5:
                                    ls.append(5)
                                if sum(line.children_tax_ids.mapped('amount')) == 18:
                                    ls.append(18)
                                if sum(line.children_tax_ids.mapped('amount')) == 28:
                                    ls.append(28)
                            else:
                                if line.amount == 1:
                                    ls.append(1)
                                if line.amount == 2:
                                    ls.append(2)
                                if line.amount == 5:
                                    ls.append(5)
                                if line.amount == 18:
                                    ls.append(18)
                                if line.amount == 28:
                                    ls.append(28)


        for obj in invoice_id:
            if obj.export_invoice == False and obj.partner_id.vat:
                for rip in set(ls):
                    # r=0
                    sub_total=0
                    for rec in obj.invoice_line_ids:
                        if rec.invoice_line_tax_ids:
                            for line in rec.invoice_line_tax_ids:
                                if line.children_tax_ids:
                                    if sum(line.children_tax_ids.mapped('amount')) == rip:
                                        # r+=rec.price_subtotal
                                        sub_total+=rec.price_subtotal
                                else:
                                    if line.amount == rip:
                                        # r+=rec.price_subtotal
                                        sub_total+=rec.price_subtotal
                    # if r == 0:
                    if sub_total == 0:
                        pass
                    else:
                        worksheet_b2b.write('A%s' %(new_row), obj.partner_id.vat)
                        worksheet_b2b.write('B%s' %(new_row), obj.number)
                        worksheet_b2b.write('C%s' %(new_row), obj.date_invoice)
                        worksheet_b2b.write('D%s' %(new_row), obj.amount_total)
                        worksheet_b2b.write_rich_string('E%s' %(new_row), str(obj.partner_id.state_id.state_code) + str("-") + str(obj.partner_id.state_id.name))
                        worksheet_b2b.write('F%s' %(new_row), 'N')
                        worksheet_b2b.write('G%s' %(new_row), '')
                        worksheet_b2b.write('H%s' %(new_row), '')
                        worksheet_b2b.write('I%s' %(new_row), rip)
                        worksheet_b2b.write('J%s' %(new_row), sub_total)
                        worksheet_b2b.write('K%s' %(new_row), '')

                        new_row+=1

        # B2CL Report
        row = 1
        col = 0
        new_row = row + 1

        ls = []
        for obj in invoice_id:
            if obj.partner_id.vat == False and obj.amount_total > 250000 and obj.partner_id.property_account_position_id.name == 'Inter State' and obj.export_invoice == False:
                for rec in obj.invoice_line_ids:
                    if rec.invoice_line_tax_ids:
                        for line in rec.invoice_line_tax_ids:
                            if line.children_tax_ids:
                                if sum(line.children_tax_ids.mapped('amount')) == 1:
                                    ls.append(1)
                                if sum(line.children_tax_ids.mapped('amount')) == 2:
                                    ls.append(2)
                                if sum(line.children_tax_ids.mapped('amount')) == 5:
                                    ls.append(5)
                                if sum(line.children_tax_ids.mapped('amount')) == 18:
                                    ls.append(18)
                                if sum(line.children_tax_ids.mapped('amount')) == 28:
                                    ls.append(28)
                            else:
                                if line.amount == 1:
                                    ls.append(1)
                                if line.amount == 2:
                                    ls.append(2)
                                if line.amount == 5:
                                    ls.append(5)
                                if line.amount == 18:
                                    ls.append(18)
                                if line.amount == 28:
                                    ls.append(28)



        for obj in invoice_id:
            if obj.partner_id.vat == False and obj.amount_total > 250000 and obj.partner_id.property_account_position_id.name == 'Inter State' and obj.export_invoice == False:
                for rip in set(ls):
                    sub_total=0
                    for rec in obj.invoice_line_ids:
                        if rec.invoice_line_tax_ids:
                            for line in rec.invoice_line_tax_ids:
                                if line.children_tax_ids:
                                    if sum(line.children_tax_ids.mapped('amount')) == rip:
                                        sub_total+=rec.price_subtotal
                                else:
                                    if line.amount == rip:
                                        sub_total+=rec.price_subtotal
                    if sub_total == 0:
                        pass
                    else:
                        worksheet_b2cl.write('A%s' %(new_row), obj.number)
                        inv_date = datetime.datetime.strptime(obj.date_invoice, '%Y-%m-%d')
                        worksheet_b2cl.write('B%s' %(new_row), obj.date_invoice)
                        worksheet_b2cl.write('C%s' %(new_row), obj.amount_total)
                        worksheet_b2cl.write_rich_string('D%s' %(new_row), str(obj.partner_id.state_id.state_code) + str("-") + str(obj.partner_id.state_id.name))
                        worksheet_b2cl.write('E%s' %(new_row), rip)
                        worksheet_b2cl.write('F%s' %(new_row), sub_total)
                        worksheet_b2cl.write('G%s' %(new_row), '')

                        new_row+=1

        # B2CS Report
        row = 1
        col = 0
        new_row = row + 1

        ls = []
        supply = []
        for obj in invoice_id:
            if obj.partner_id.vat == False and ((obj.amount_total <= 250000 and obj.partner_id.property_account_position_id.name == 'Inter State') or obj.partner_id.property_account_position_id.name == 'Intra State'):
                for rec in obj.invoice_line_ids:
                    if rec.invoice_line_tax_ids:
                        for line in rec.invoice_line_tax_ids:
                            if line.children_tax_ids:
                                if sum(line.children_tax_ids.mapped('amount')) == 1:
                                    ls.append(1)
                                if sum(line.children_tax_ids.mapped('amount')) == 2:
                                    ls.append(2)
                                if sum(line.children_tax_ids.mapped('amount')) == 5:
                                    ls.append(5)
                                if sum(line.children_tax_ids.mapped('amount')) == 18:
                                    ls.append(18)
                                if sum(line.children_tax_ids.mapped('amount')) == 28:
                                    ls.append(28)
                            else:
                                if line.amount == 1:
                                    ls.append(1)
                                if line.amount == 2:
                                    ls.append(2)
                                if line.amount == 5:
                                    ls.append(5)
                                if line.amount == 18:
                                    ls.append(18)
                                if line.amount == 28:
                                    ls.append(28)
                supply.append([obj.partner_id.e_commerce,obj.partner_id.state_id.name,obj.partner_id.state_id.state_code,obj.partner_id.e_commerce_tin])


        for rip in set(ls):
            for s in set(map(tuple,supply)):
                sub_total=0
                for obj in invoice_id:
                    if obj.partner_id.vat == False and ((obj.amount_total <= 250000 and obj.partner_id.property_account_position_id.name == 'Inter State') or obj.partner_id.property_account_position_id.name == 'Intra State') and (obj.partner_id.e_commerce == s[0] and obj.partner_id.state_id.name == s[1] and obj.partner_id.e_commerce_tin == s[3]):
                        for rec in obj.invoice_line_ids:
                            if rec.invoice_line_tax_ids:
                                for line in rec.invoice_line_tax_ids:
                                    if line.children_tax_ids:
                                        if sum(line.children_tax_ids.mapped('amount')) == rip:
                                            sub_total+=rec.price_subtotal
                                    else:
                                        if line.amount == rip:
                                            sub_total+=rec.price_subtotal
                if sub_total == 0:
                    pass
                else:
                    worksheet_b2cs.write('A%s' %(new_row), 'E' if s[0] == True else 'OE')
                    worksheet_b2cs.write_rich_string('B%s' %(new_row), str(s[1]) + str("-") + str(s[2]))
                    worksheet_b2cs.write('C%s' %(new_row), rip)
                    worksheet_b2cs.write('D%s' %(new_row), sub_total)
                    worksheet_b2cs.write('E%s' %(new_row), '')
                    worksheet_b2cs.write('F%s' %(new_row), s[3])

                    new_row+=1


        # HSN Report
        row = 1
        col = 0
        new_row = row + 1

        partner_state = self.env.user.company_id.partner_id.state_id.name

        ls = []
        t = []
        for obj in invoice_id:
            for rec in obj.invoice_line_ids:
                ls.append(rec.product_id.l10n_in_hsn_code)

        l10n_in_hsn_code = set(ls)
        for hsn in l10n_in_hsn_code:
            qty = 0
            taxable = 0
            cgst = 0
            sgst = 0
            igst = 0
            uom=''

            for inv in invoice_id:
                for line in inv.invoice_line_ids:
                    if line.product_id.l10n_in_hsn_code == hsn:
                        qty+=line.quantity
                        name = line.name
                        uom = line.uom_id.name
                        if line.invoice_line_tax_ids:
                            for rec in line.invoice_line_tax_ids:
                                if 'GST' in rec.name:
                                    taxable+=line.price_subtotal
                                    if rec.children_tax_ids:
                                        cgst+=(((sum(rec.children_tax_ids.mapped('amount'))/100)*line.price_subtotal)/2)
                                        sgst+=(((sum(rec.children_tax_ids.mapped('amount'))/100)*line.price_subtotal)/2)
                                if 'IGST' in rec.name:
                                    igst+=((rec.amount/100)*line.price_subtotal)

            t_value = taxable+cgst+sgst+igst
            worksheet_hsn.write('A%s' %(new_row), hsn)
            worksheet_hsn.write('B%s' %(new_row), name)
            worksheet_hsn.write('C%s' %(new_row), uom)
            worksheet_hsn.write('D%s' %(new_row), qty)
            worksheet_hsn.write('E%s' %(new_row), t_value)
            worksheet_hsn.write('F%s' %(new_row), taxable)
            worksheet_hsn.write('G%s' %(new_row), igst)
            worksheet_hsn.write('H%s' %(new_row), cgst)
            worksheet_hsn.write('I%s' %(new_row), sgst)
            worksheet_hsn.write('J%s' %(new_row), '')

            new_row+=1

        # Export Report
        # row = 1
        # col = 0
        # new_row = row + 1

        # ls = []
        # for obj in invoice_id:


        #     if obj.export_invoice == True:
        #         for rec in obj.invoice_line_ids:
        #             for line in rec.invoice_line_tax_ids:
        #                 if line.children_tax_ids:
        #                     if sum(line.children_tax_ids.mapped('amount')) == 1:
        #                         ls.append(1)
        #                     if sum(line.children_tax_ids.mapped('amount')) == 2:
        #                         ls.append(2)
        #                     if sum(line.children_tax_ids.mapped('amount')) == 5:
        #                         ls.append(5)
        #                     if sum(line.children_tax_ids.mapped('amount')) == 18:
        #                         ls.append(18)
        #                     if sum(line.children_tax_ids.mapped('amount')) == 28:
        #                         ls.append(28)
        #                 else:
        #                     if line.amount == 1:
        #                         ls.append(1)
        #                     if line.amount == 2:
        #                         ls.append(2)
        #                     if line.amount == 5:
        #                         ls.append(5)
        #                     if line.amount == 18:
        #                         ls.append(18)
        #                     if line.amount == 28:
        #                         ls.append(28)

        # for obj in invoice_id:
        #     if obj.export_invoice == True:
        #         for rip in set(ls):
        #             sub_total=0
        #             for rec in obj.invoice_line_ids:
        #                 for line in rec.invoice_line_tax_ids:
        #                     if line.children_tax_ids:
        #                         if sum(line.children_tax_ids.mapped('amount')) == rip:
        #                             sub_total+=rec.price_subtotal
        #                     else:
        #                         if line.amount == rip:
        #                             sub_total+=rec.price_subtotal

        #             if sub_total == 0:
        #                 pass
        #             else:
        #                 line = re.sub('[-]', '', obj.date_invoice)
        #                 year = int(line[:4])
        #                 mon = int(line[4:6])
        #                 day = int(line[6:8])

        #                 worksheet_export.write('A%s' %(new_row), obj.export_type)
        #                 worksheet_export.write('B%s' %(new_row), obj.number)
        #                 worksheet_export.write('C%s' %(new_row), date(year,mon,day).strftime('%d %b %Y'))
        #                 worksheet_export.write('D%s' %(new_row), obj.amount_total)
        #                 worksheet_export.write('E%s' %(new_row), obj.port_code.name)
        #                 worksheet_export.write('F%s' %(new_row), obj.ship_bill_no)
        #                 worksheet_export.write('G%s' %(new_row), obj.ship_bill_date)
        #                 worksheet_export.write('H%s' %(new_row), rip)
        #                 worksheet_export.write('I%s' %(new_row), sub_total)

        #                 new_row+=1

        # Cdnr Report
        row = 1
        col = 0
        new_row = row + 1

        for obj in debit_note:
            if obj.invoice_no:
                if obj.partner_id.vat:
                    worksheet_cdn.write('A%s' %(new_row), obj.partner_id.vat)
                    worksheet_cdn.write('B%s' %(new_row), obj.number)
                    worksheet_cdn.write('C%s' %(new_row), obj.date)
                    worksheet_cdn.write('D%s' %(new_row), obj.invoice_no.number)
                    worksheet_cdn.write('E%s' %(new_row), obj.invoice_date)
                    worksheet_cdn.write('F%s' %(new_row), 'Y')
                    worksheet_cdn.write('G%s' %(new_row), 'D')
                    worksheet_cdn.write('H%s' %(new_row), dict(VALUES)[obj.rfid])
                    worksheet_cdn.write('I%s' %(new_row), obj.total)

                    Rate = 0
                    if obj.tax.children_tax_ids:
                        Rate = sum(obj.tax.children_tax_ids.mapped('amount'))
                    else:
                        Rate = obj.tax.amount
                    worksheet_cdn.write('J%s' %(new_row), Rate)

                    worksheet_cdn.write('K%s' %(new_row), obj.amount)
                    worksheet_cdn.write('L%s' %(new_row), '')

                    new_row+=1

        for obj in credit_note:
            if obj.invoice_no:
                if obj.partner_id.vat:
                    worksheet_cdn.write('A%s' %(new_row), obj.partner_id.vat)
                    worksheet_cdn.write('B%s' %(new_row), obj.number)
                    worksheet_cdn.write('C%s' %(new_row), obj.date)
                    worksheet_cdn.write('D%s' %(new_row), obj.invoice_no.number)
                    worksheet_cdn.write('E%s' %(new_row), obj.invoice_date)
                    worksheet_cdn.write('F%s' %(new_row), 'Y')
                    worksheet_cdn.write('G%s' %(new_row), 'C')
                    worksheet_cdn.write('H%s' %(new_row), dict(VALUES)[obj.rfid])

                    worksheet_cdn.write('I%s' %(new_row), obj.total)

                    Rate = 0
                    if obj.tax.children_tax_ids:
                        Rate = sum(obj.tax.children_tax_ids.mapped('amount'))
                    else:
                        Rate = obj.tax.amount
                    worksheet_cdn.write('J%s' %(new_row), Rate)

                    worksheet_cdn.write('K%s' %(new_row), obj.amount)
                    worksheet_cdn.write('L%s' %(new_row), '')

                    new_row+=1


        # Cdnur Report
        row = 1
        col = 0
        new_row = row + 1

        for obj in debit_note:
            if obj.invoice_no:
                if not obj.partner_id.vat:
                    inv_date = datetime.datetime.strptime(obj.invoice_date, '%Y-%m-%d')
                    note_date = datetime.datetime.strptime(obj.date, '%Y-%m-%d')
                    worksheet_cdnur.write('A%s' %(new_row), 'B2CL')
                    worksheet_cdnur.write('B%s' %(new_row), obj.number)
                    worksheet_cdnur.write('C%s' %(new_row), note_date,date_format)
                    worksheet_cdnur.write('D%s' %(new_row), 'D')
                    worksheet_cdnur.write('E%s' %(new_row), obj.invoice_no.number)
                    worksheet_cdnur.write('F%s' %(new_row), inv_date,date_format)
                    if self.env.user.company_id.country_id.id == obj.partner_id.country_id.id:
                        worksheet_cdnur.write_rich_string('G%s' %(new_row), obj.partner_id.state_id.state_code + "-" + obj.partner_id.state_id.name)
                    else:
                        worksheet_cdnur.write_rich_string('G%s' %(new_row), '')
                    worksheet_cdnur.write('H%s' %(new_row), obj.total)
                    if obj.applied_tax_rate == '65':
                        worksheet_cdnur.write('I%s' %(new_row), 65.0)
                    else:
                        worksheet_cdnur.write('I%s' %(new_row), 100.0)

                    Rate = 0
                    if obj.tax.children_tax_ids:
                        Rate = sum(obj.tax.children_tax_ids.mapped('amount'))
                    else:
                        Rate = obj.tax.amount
                    worksheet_cdnur.write('J%s' %(new_row), Rate)

                    worksheet_cdnur.write('K%s' %(new_row), obj.amount)
                    worksheet_cdnur.write('L%s' %(new_row), '')
                    worksheet_cdnur.write('M%s' %(new_row), 'Y')

                    new_row+=1

        for obj in credit_note:
            if obj.invoice_no:
                if not obj.partner_id.vat:
                    inv_date = datetime.datetime.strptime(obj.invoice_date, '%Y-%m-%d')
                    note_date = datetime.datetime.strptime(obj.date, '%Y-%m-%d')

                    worksheet_cdnur.write('A%s' %(new_row), 'B2CL')
                    worksheet_cdnur.write('B%s' %(new_row), obj.number)
                    worksheet_cdnur.write('C%s' %(new_row), note_date,date_format)
                    worksheet_cdnur.write('D%s' %(new_row), 'C')
                    worksheet_cdnur.write('E%s' %(new_row), obj.invoice_no.number)
                    worksheet_cdnur.write('F%s' %(new_row), inv_date,date_format)
                    if self.env.user.company_id.country_id.id == obj.partner_id.country_id.id:
                        worksheet_cdnur.write_rich_string('G%s' %(new_row), obj.partner_id.state_id.state_code + "-" + obj.partner_id.state_id.name)
                    else:
                        worksheet_cdnur.write_rich_string('G%s' %(new_row), '')
                    worksheet_cdnur.write('H%s' %(new_row), obj.total)
                    if obj.applied_tax_rate == '65':
                        worksheet_cdnur.write('I%s' %(new_row), 65.0)
                    else:
                        worksheet_cdnur.write('I%s' %(new_row), 100.0)

                    Rate = 0
                    if obj.tax.children_tax_ids:
                        Rate = sum(obj.tax.children_tax_ids.mapped('amount'))
                    else:
                        Rate = obj.tax.amount
                    worksheet_cdnur.write('J%s' %(new_row), Rate)

                    worksheet_cdnur.write('K%s' %(new_row), obj.amount)
                    worksheet_cdnur.write('L%s' %(new_row), '')
                    worksheet_cdnur.write('M%s' %(new_row), 'Y')

                    new_row+=1



        
