# -*- coding: utf-8 -*-
{
    'name': "SAR Honduras",
    "author": "Christopher Gonzalez",
    'summary': '', 
    'description': """
        Régimen de facturación SAR Honduras
    """,          
    'version': '1.0',
    'license': 'AGPL-3',
    'depends': ['base', 'account', 'account_debit_note','l10n_hn','contacts'],
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'views/cai_cai_views.xml',
        'views/res_partner_views.xml',
        'views/res_company_views.xml',
        'views/account_move_views.xml',
        'views/account_journal_views.xml',
        'views/account_retention_views.xml',
        'views/res_company.xml',
        'widzard/account_move_retention_views.xml',
        'reports/invoice_report.xml',
        # 'reports/report_invoice_document.xml',
        'views/menus.xml'
    ],
   
    'application': False,
}