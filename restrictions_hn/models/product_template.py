from odoo import models, fields, api, _
from odoo.exceptions import *
from odoo.tools import format_amount

class ProductTemplateInherit(models.Model):
    _inherit = "product.template"

    @api.depends('list_price','standard_price')
    def _get_ganancia(self):
        for rec in self:
            diferencia = rec.list_price - rec.standard_price
            rec.ganancia = diferencia / rec.list_price

    ganancia = fields.Float(string="Ganancia(%)", compute="_get_ganancia")
    tax_cost_string = fields.Char(compute='_compute_tax_cost_string')

    @api.depends('taxes_id', 'standard_price')
    def _compute_tax_cost_string(self):
        for record in self:
            record.tax_cost_string = record._construct_tax_cost_string(record.standard_price)

    def _construct_tax_cost_string(self, price):
        currency = self.currency_id
        res = self.taxes_id.compute_all(price, product=self, partner=self.env['res.partner'])
        joined = []
        included = res['total_included']
        if currency.compare_amounts(included, price):
            joined.append(_('%s Incl. Taxes', format_amount(self.env, included, currency)))
        excluded = res['total_excluded']
        if currency.compare_amounts(excluded, price):
            joined.append(_('%s Excl. Taxes', format_amount(self.env, excluded, currency)))
        if joined:
            tax_cost_string = f"(= {', '.join(joined)})"
        else:
            tax_cost_string = " "
        return tax_cost_string