from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class SaleOrderLineInherit(models.Model):
    _inherit = "sale.order.line"

    @api.constrains("product_id", "price_unit")
    def _check_product_price(self):
        for line in self:
            if line.product_id and line.price_unit < line.product_id.lst_price:
                if not line.order_id.allow_sale_low_price:
                    raise ValidationError("El precio de venta del producto no puede ser inferior al precio de venta mínimo establecido en la ficha del producto.")

            if line.product_id and line.price_unit < line.product_id.standard_price:
                if not line.order_id.allow_sale_low_price:
                    raise ValidationError("El precio de venta del producto no puede ser inferior al costo.")
            
class SaleOrderInherit(models.Model):
    _inherit = "sale.order"

    #agregamos un campo boolean para permitir crear facturas al credito
    allow_sale_low_price = fields.Boolean("Permitir facturar con precios por debajo del de la ficha de producto", tracking=True)
