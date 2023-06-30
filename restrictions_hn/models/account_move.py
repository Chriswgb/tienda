from odoo import models, fields, api
from odoo.exceptions import *

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
		