# -*- coding: utf-8 -*-
{
    'name': "Restricciones Honduras",

    'summary': """""",

    'description': """""",

    'author': "Christopher Gonzalez",

    'category': 'Sales/Point of Sale',
    'version': '1.0',
    'license': 'AGPL-3',
    # any module necessary for this one to work correctly
    'depends': ['stock','account','point_of_sale','purchase'],
    # always loaded
    'data': [
        'security/groups.xml',
        'views/sale_order_views.xml',
        'views/account_move_views.xml',
        'views/stock_picking_views.xml',
        'views/product_product_views.xml',
        'views/product_template_views.xml',
        'views/account_menus.xml',
        'views/stock_menus.xml'
    ],
    'assets': {
        'web.assets_qweb':[
            'restrictions_hn/static/src/xml/Screens/ProductScreen/NumpadWidget.xml',
            'restrictions_hn/static/src/xml/Screens/ProductScreen/ActionpadWidget.xml',
        ],
    },
    'application': False
}
