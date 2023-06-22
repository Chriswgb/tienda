# -*- coding: utf-8 -*-
{
    'name': "POS Honduras",

    'summary': """""",

    'description': """""",

    'author': "Christopher Gonzalez",

    'category': 'Sales/Point of Sale',
    'version': '1.0',
    'license': 'AGPL-3',
    # any module necessary for this one to work correctly
    'depends': ['base', 'point_of_sale', 'sar'],
    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'reports/corte_caja_report.xml',
        'reports/corte_caja_session_report.xml',
        'reports/z_closure_report.xml',
        'reports/z_closure_report_view.xml',
        'wizard/z_closure.xml',
        'views/pos_config_view.xml',
        'views/res_company.xml',
        'views/pos_order.xml',
        'views/pos_session.xml',
        'views/pos_payment_method.xml',
    ],
    'assets': {
        'web.assets_qweb':[
            'pos_hn/static/src/xml/Screens/ReceiptScreen/OrderReceipt.xml',
            'pos_hn/static/src/xml/Screens/PaymentScreen/PaymentScreen.xml',
            'pos_hn/static/src/xml/Screens/ClientListScreen/ClientDetailsEdit.xml',
            'pos_hn/static/src/xml/Screens/ClientListScreen/ClientLineCustom.xml',
            'pos_hn/static/src/xml/Screens/ClientListScreen/ClientListScreen.xml',
            'pos_hn/static/src/xml/Popups/CardInformationPopup.xml',
            'pos_hn/static/src/xml/Popups/ChequeInformationPopup.xml',
            'pos_hn/static/src/xml/Popups/MotivoReembolsoPopup.xml',
            'pos_hn/static/src/xml/Screens/ProductScreen/NumpadWidget.xml',
            'pos_hn/static/src/xml/Screens/ProductScreen/ActionpadWidget.xml',
            'pos_hn/static/src/xml/Screens/ProductScreen/ControlButtons/EstadoCajaButton.xml',
        ],
        'point_of_sale.assets': [
            'pos_hn/static/src/js/models.js',
            'pos_hn/static/src/js/Screens/TicketScreen/ControlButtons/ReprintReceiptButton.js',
            'pos_hn/static/src/js/Screens/ClientListScreen/ClientDetailsEdit.js',
            'pos_hn/static/src/js/Popups/CardPopUp.js',
            'pos_hn/static/src/js/Popups/ChequePopUp.js',
            'pos_hn/static/src/js/Popups/MotivoReembolsoPopup.js',
            'pos_hn/static/src/js/Screens/PaymentScreen/PaymentScreen.js',
            'pos_hn/static/src/js/Screens/ProductScreen/ControlButtons/EstadoCajaButton.js',
        ]
    },
    'application': False
}
