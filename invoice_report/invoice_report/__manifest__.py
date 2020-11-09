# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'Invoice Report',
    'version' : '1.1',
    'summary': 'Generate report ',
    'description': """
Generate report in xlsx format.
    """,
    'category': 'Accounting',
    'website': 'https://www.merlintecsol.com',
    'data': [
        'report/invoice_report.xml',
        'wizard/wizard_report.xml',
    ],
    'depends': ['base','report_xlsx','account_invoicing'],
    'installable': True,
    'application': False,
    'auto_install': False,
}
