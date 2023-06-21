# -*- coding: utf-8 -*-
from odoo.http import request
from odoo import models, fields, api, _
from odoo.exceptions import Warning, ValidationError
from datetime import timedelta, datetime

class PurchasingInventory(models.TransientModel):
    _name = "hn.purchasing.inventory"
    _description = "Reporte de inventario compras"

    line_ids = fields.One2many(string="Lineas", comodel_name="hn.purchasing.inventory.line", inverse_name="report_id")

    def get_data(self):
        obj_delete = self.env["hn.purchasing.inventory.line"].search([('report_id','=',self.id)]).unlink()
        obj_create = self.env["hn.purchasing.inventory.line"]

        products = self.env['product.product'].search([('detailed_type','=','product')])
        

        for product in products:
            stock_qty = product.qty_available
            purchases = self.env['purchase.order.line'].search([('state','=','purchase'),('product_id','=',product.id)])
            purchases_total = sum(purchases.mapped('qty_received'))
            last_purchase = self.env['purchase.order.line'].search([('state','=','purchase'),('product_id','=',product.id)], order='id desc', limit=1)
            vals={
                'product_id':product.id,
                'stock_actual':stock_qty,
                'qty_purchase':purchases_total,
                'qty_sale':(purchases_total - stock_qty),
                'partner_id':last_purchase.partner_id.id,
                'price':last_purchase.price_unit,
                'categ_id':product.categ_id.id,
                'report_id':self.id
            }
            obj_create.create(vals)


class PurchasingInventoryLine(models.TransientModel):
    _name = "hn.purchasing.inventory.line"
    _description = "Lineas de reporte de inventario compras"

    company_id = fields.Many2one(string='Company', comodel_name='res.company', default=lambda self: self.env.user.company_id.id, index=1)
    currency_id = fields.Many2one(string='Currency', comodel_name='res.currency', default=lambda self:self.env.user.company_id.currency_id.id, required=True)
    product_id = fields.Many2one(string="Producto", comodel_name="product.product")
    stock_actual = fields.Float(string="Cantidad actual en existencia")
    qty_purchase = fields.Float(string="Cantidad comprada")
    qty_sale = fields.Float(string="Cantidad vendida")
    partner_id = fields.Many2one(string="Proveedor del que ingreso la ultima vez el producto", comodel_name="res.partner")
    price = fields.Float(string="Ultimo Precio de Compra al que ingreso con Impuesto incluido")
    categ_id = fields.Many2one(string="Categoria de producto", comodel_name="product.category")
    report_id = fields.Many2one(string="Reporte", comodel_name="hn.purchasing.inventory")