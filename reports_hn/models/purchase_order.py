# -*- coding: utf-8 -*-
from odoo import api, models, fields, _
from odoo.exceptions import UserError


class PurchaseOrderLineInherit(models.Model):
    _inherit = "purchase.order.line"

    total_isv = fields.Float(string="Total con ISV", store=True)

    @api.onchange('product_id','product_qty','price_unit')
    def _get_total(self):
        for rec in self:
            rec.total_isv = rec.product_qty * rec.price_unit