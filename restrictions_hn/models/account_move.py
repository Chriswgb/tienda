from odoo import models, fields, api
from odoo.exceptions import *

class AccountMoveLineInherit(models.Model):
	_inherit = "account.move.line"

	@api.constrains("product_id", "price_unit")
	def _check_product_price(self):
		for line in self:
			if line.move_id.move_type == 'out_invoice':
				if line.product_id and line.price_unit < line.product_id.lst_price:
					if not line.move_id.allow_sale_low_price:
						raise ValidationError("El precio de venta del producto no puede ser inferior al precio de venta mínimo establecido en la ficha del producto.")


class AccountMoveInherit(models.Model):
	#heredamos el modelo account.move
	_inherit = "account.move"

	#agregamos un campo boolean para permitir crear facturas al credito
	allow_credit_invoices = fields.Boolean("Permitir facturas al crédito", tracking=True)
	#agregamos un campo boolean para permitir crear facturas al credito
	allow_sale_low_price = fields.Boolean("Permitir facturar con precios por debajo del de la ficha de producto", tracking=True)

	#sobreecribimos la funcion action_post
	def action_post(self):

		r = super(AccountMoveInherit,self).action_post()

		if self.move_type == 'out_invoice':

			if self.invoice_payment_term_id:

				if self.invoice_payment_term_id.id != 1:
					
					#consultamos el objeto que contiene las configuraciones del modulo de inventario
					if not self.allow_credit_invoices:
						raise UserError(("No tiene permisos para crear facturas al crédito"))
			
		return r
		