# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.

{
    'name': "Remise Globale sur Devis et Factures",
    'summary': """ Vous permet d’appliquer une remise globale sur le montant de vos devis et factures.  """,
    "contributors": [
        "1 <Nassim REFES>",
        "2 <Kamel BENCHEHIDA>",
    ],
    'version': '12.0.0.1',
    "license": "OPL-1",
    'author': 'Elosys',
    'website': 'http://igpro-online.net/',
    "price": 00.0,
    "currency": 'EUR',
    'depends': [
        'account',
        'sale',
        'sale_management',
    ],
    'data': [
        "security/security.xml",

        "views/account_invoice.xml",
        "views/sale_order.xml",

        "reports/account_invoice_report.xml",
        "reports/sale_report.xml",
    ],
    'images': ['images/main_screenshot.gif'],

    'installable': True,
    'auto_install': False,
    "application":False,
}
