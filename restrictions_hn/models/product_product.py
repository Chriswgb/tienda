from odoo import models, fields, api, _
from odoo.exceptions import *
from odoo.tools import format_amount

class ProductProductInherit(models.Model):
    _inherit = "product.product"

    @api.depends('lst_price','standard_price')
    def _get_ganancia(self):
        for rec in self:
            diferencia = rec.lst_price - rec.standard_price
            rec.ganancia = diferencia / rec.standard_price

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

    #sobreecribimos la funcion create
    @api.model
    def create(self, vals):

        vals["default_code"] = ""
        #verificamos si el campo del codigo del producto esta vacio
        if not vals["default_code"]:
            
            #consultamos el objeto que contiene las configuraciones del modulo de inventario
            product_sequence_id = int(self.env['ir.config_parameter'].sudo().get_param('res_config_settings.product_sequence_id'))

            #verificacmos que se haya establecido una secuencia para los productos
            if product_sequence_id:
                # asignamos el codido del producto desde la secuencia configurada
                vals["default_code"] = self.env["ir.sequence"].sudo().search([('id', '=', product_sequence_id)]).next_by_id()
            else:
                raise UserError(("Debe establecer la secuencia de códigos de producto en el apartado de ajustes en el módulo de inventario."))

        res = super(ProductProductInherit, self).create(vals)

        return res
