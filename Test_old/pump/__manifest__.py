# -*- coding: utf-8 -*-

{
    'name': 'pump Record',
    'summary': """This module will add a record to store pump details""",
    'version': '1.0',
    'description': """This module will add a record to store pump details""",
    'author': 'Merlin_Techsol',
    'company': 'Merlin',
    'website': 'http://www.merlinTechsol.com',
    'category': 'Tools',
    'depends': ['base','report_xlsx'],
    'license': 'GPL-3',
    'data': [
        'wizard/wizard.xml',
        'views/pump_views.xml',
        'wizard/msg.xml',
        'report/invoicexlsx.xml',
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
}
