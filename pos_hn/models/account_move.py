# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
#from itertools import ifilter
# mapping invoice type to journal type

class AccountInvoiceBIM(models.Model):
    _inherit = "account.move"
   
    @api.depends("invoice_line_ids.price_subtotal")
    def sar(self):
        for move in self:
            exento = 0
            exonerado = 0
            gravado = 0 
            impuesto = 0
            impuesto_18 = 0 
            gravado_18 = 0 
            
            for line in move.invoice_line_ids:
                for tax in line.tax_ids:
                    if tax.description == "Exento":
                        exento += line.price_subtotal
                    if tax.description == "Exonerado":
                        exonerado += line.price_subtotal
                    if tax.amount == 15:
                        impuesto += (line.price_total - line.price_subtotal)
                        gravado += line.price_subtotal
                    if tax.amount == 18:
                        impuesto_18 += (line.price_total - line.price_subtotal)
                        gravado_18 += line.price_subtotal
            
            move.excento = exento
            move.exonerado = exonerado
            move.gravado = gravado 
            move.impuesto = impuesto
            move.impuesto_18 = impuesto_18 
            move.gravado_18 = gravado_18 
    
    excento = fields.Float(string="Exento", compute="sar", store=True)
    exonerado = fields.Float(string="Exonerado", compute="sar", store=True)
    gravado =fields.Float(string="Gravado", compute="sar", store=True)
    impuesto =fields.Float(string="Impuesto 15", compute="sar", store=True)
    gravado_18 =fields.Float(string="Gravado 18", compute="sar", store=True)
    impuesto_18 =fields.Float(string="Impuesto 15", compute="sar", store=True)