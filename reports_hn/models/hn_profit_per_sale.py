# -*- coding: utf-8 -*-
from odoo.http import request
from odoo import models, fields, api, _
from odoo.exceptions import Warning, ValidationError
from datetime import timedelta, datetime

class ProfitPerSale(models.TransientModel):
    _name = "hn.profit.per.sale"
    _description = "Reporte de ganancias por venta"
    _rec_name = "date_from"

    date_from = fields.Date(string="Fecha desde")
    date_to = fields.Date(string="Fecha hasta")
    ganancia_percentage = fields.Float(string="Ganancia total %")
    line_ids = fields.One2many(string="Lineas", comodel_name="hn.profit.per.sale.line", inverse_name="report_id")

    def get_data(self):
        obj_delete = self.env["hn.profit.per.sale.line"].search([('report_id','=',self.id)]).unlink()
        obj_create = self.env["hn.profit.per.sale.line"]
        # Querys de las facturas
        select_query_invoices=  """
            SELECT am.invoice_date AS fecha_documento, am.name AS num_documento, am.cai_shot AS cai, am.cai_expires_shot AS fecha_limite,
            rp.id AS cliente, am.amount_total AS monto_total, am.id AS id_factura
            FROM public.account_move AS am
        """
        join_query_invoices = """
             JOIN public.res_partner AS rp ON rp.id=am.partner_id
        """
        where_query_invoices = """
             WHERE am.invoice_date >= %s AND am.invoice_date <= %s AND am.state='posted' AND  am.move_type='out_invoice'
        """
        query_invoices = select_query_invoices + join_query_invoices + where_query_invoices
        self.env.cr.execute(query_invoices,(self.date_from, self.date_to))
        invoices = self.env.cr.dictfetchall()

        # Querys de las lineas de factura
        select_query_invoice_lines = """
            SELECT aml.move_id, at.description, aml.price_subtotal, aml.price_total, aml.discount, aml.price_unit, aml.quantity, aml.product_id
            FROM public.account_move_line AS aml
        """
        join_query_invoice_lines = """
             JOIN public.account_move_line_account_tax_rel AS amlatr ON amlatr.account_move_line_id = aml.id
            JOIN public.account_tax AS at ON at.id = amlatr.account_tax_id
        """
        where_query_invoice_lines = """
             WHERE aml.date >= %s AND aml.date <= %s AND aml.parent_state='posted' 
        """
        query_invoice_lines = select_query_invoice_lines + join_query_invoice_lines + where_query_invoice_lines
        self.env.cr.execute(query_invoice_lines,(self.date_from, self.date_to))
        invoice_lines = self.env.cr.dictfetchall()

        total_costo = 0
        total_ganancia = 0
        # Recorro las facturas
        for invoice in invoices:
            # Variables para acumular
            exento=0
            exonerado=0
            grabado_quince=0
            impuesto=0
            subtotal = 0
            descuento = 0
            costo = 0
            ganancia = 0
            ganancia_porcentaje = 0
            # Recorro las lineas de factura
            for line in invoice_lines:
                # si el move_id sea igual a id_factura va a comparar  la etiqueta del tipo de impuesto y hacer los calculos correspondientes
                if line['move_id'] ==invoice['id_factura']:
                    if line['description']=='Exento':
                        exento= exento+line['price_subtotal']
                    if line['description']=='Exonerado':
                        exonerado=exonerado+line['price_subtotal']
                    if line['description']=='ISV por Pagar':
                        grabado_quince=grabado_quince+line['price_subtotal']
                        impuesto=impuesto+(line['price_total'] - line['price_subtotal'])
                    if line['discount'] > 0:
                        descuento = descuento + (line['quantity'] * (line['price_unit'] * (line['discount']/100)))
                    if line['product_id']:
                        product = self.env['product.product'].browse(int(line['product_id']))
                        costo += (line['quantity'] * product.standard_price)
                
            subtotal = exento + exonerado + grabado_quince
            ganancia = subtotal - costo
            total_costo += costo
            total_ganancia += ganancia
            ganancia_porcentaje = ganancia / costo
            vals={
                'date':invoice['fecha_documento'],
                'invoice':invoice['num_documento'],
                'cai':invoice['cai'],
                'end_date':invoice['fecha_limite'],
                'partner_id':invoice['cliente'],
                'amount_total':invoice['monto_total'],
                'exento':exento,
                'exonerado':exonerado,
                'gravado':grabado_quince,
                'impuesto':impuesto,
                'descuento':descuento,
                'sub_total':subtotal,
                'cost_total':costo,
                'ganancia_total':ganancia,
                'ganancia_percentage':ganancia_porcentaje,
                'report_id':self.id
            }
            obj_create.create(vals)
        
        if total_costo > 0 and total_ganancia > 0:
            self.ganancia_percentage = total_ganancia / total_costo
        else:
            self.ganancia_percentage = 0

class ProfitPerSale(models.TransientModel):
    _name = "hn.profit.per.sale.line"
    _description = "Lineas de reporte de ganancias por venta"

    company_id = fields.Many2one(string='Company', comodel_name='res.company', default=lambda self: self.env.user.company_id.id, index=1)
    currency_id = fields.Many2one(string='Currency', comodel_name='res.currency', default=lambda self:self.env.user.company_id.currency_id.id, required=True)
    date = fields.Date(string="Fecha")
    invoice = fields.Char(string="Factura")
    cai = fields.Char(string="CAI")
    end_date =  fields.Date(string="Fecha limite")
    partner_id = fields.Many2one(string="Cliente", comodel_name="res.partner")
    exento = fields.Float(string="Monto Exento")
    exonerado = fields.Float(string="Monto Exonerado")
    gravado = fields.Float(string="Monto Gravado 15%")
    sub_total = fields.Float(string="Sub Total")
    impuesto = fields.Float(string="Impuesto (15%)")
    descuento = fields.Float(string="Monto Descuento")
    amount_total = fields.Float(string="Monto Total")
    cost_total = fields.Float(string="Costo de Venta Total sin ISV")
    ganancia_total = fields.Float(string="Ganancia Total sin ISV")
    ganancia_percentage = fields.Float(string="Ganancia %")
    report_id = fields.Many2one(string="Reporte", comodel_name="hn.profit.per.sale")