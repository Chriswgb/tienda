# -*- coding: utf-8 -*-
{
    'name': "Reportes",
    "author": "Christopher Gonzalez",
    'summary': '', 
    'description': """
        Reportes
    """,          
    'version': '1.0',
    'license': 'AGPL-3',
    'depends': ['base', 'account','stock','purchase'],
    'data': [
        # 'security/groups.xml',
        'security/ir.model.access.csv',
        'views/hn_profit_per_sale_views.xml',
        'views/purchase_order_views.xml',
        'views/hn_purchasing_inventory_views.xml',
        'views/menus.xml'
    ],
   
    'application': False,
}