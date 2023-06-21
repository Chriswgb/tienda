# -*- coding: utf-8 -*- #

from odoo import models, fields

class dev_pos_config(models.Model):
	_inherit = 'pos.config'
	
	print_invoice_no_receipt = fields.Boolean(string="Imprimir Número de Factura")
	default_customer_id = fields.Many2one('res.partner', string='Cliente Por Defecto')


class dev_pos_order(models.Model):
	_inherit = 'pos.order'
	
	def fetch_invoice_number(self):
		self.ensure_one ()
		return self.account_move.name
	
	def fetch_cai_number(self):
		self.ensure_one ()
		return self.account_move.cai_shot
	
	def fetch_expiration_cai(self):
		self.ensure_one ()
		return self.account_move.cai_expires_shot
	
	def fetch_min_cai(self):
		self.ensure_one ()
		return self.account_move.min_number_shot
	
	def fetch_max_cai(self):
		self.ensure_one ()
		return self.account_move.max_number_shot
	
	def fetch_amount_untaxed(self):
		self.ensure_one ()
		return self.account_move.amount_untaxed
	
	def fetch_amount_tax(self):
		self.ensure_one ()
		return self.account_move.impuesto
	
	def fetch_amount_total_text(self):
		self.ensure_one ()
		return self.account_move.amount_total_text

	def fetch_excento(self):
		self.ensure_one ()
		return self.account_move.excento

	def fetch_exonerado(self):
		self.ensure_one ()
		return self.account_move.exonerado
	
	def fetch_gravado(self):
		self.ensure_one ()
		return self.account_move.gravado
	
	def fetch_street(self):
		self.ensure_one ()
		return self.company_id.street
	
	def fetch_street2(self):
		self.ensure_one ()
		return self.company_id.street2
	
	def fetch_city(self):
		self.ensure_one ()
		return self.company_id.city
	
	def fetch_state_id(self):
		self.ensure_one ()
		return self.company_id.state_id.name
	
	def fetch_rtn(self):
		self.ensure_one ()
		return self.company_id.rtn
	
	def fetch_nombre_comercial(self):
		self.ensure_one ()
		return self.company_id.nombre_comercial	
	
	def fetch_phone(self):
		self.ensure_one ()
		return self.company_id.phone

	def fetch_whatsapp(self):
		self.ensure_one ()
		return self.company_id.whatsapp
	
	def fetch_gravado18(self):
		self.ensure_one ()
		return self.account_move.gravado_18
	
	def fetch_impuesto18(self):
		self.ensure_one ()
		return self.account_move.impuesto_18

	def fetch_rtn2(self):
		self.ensure_one ()
		return self.account_move.partner_id.rtn

	def fetch_customer_name(self):
		self.ensure_one ()
		return self.account_move.partner_id.customer_name
	
	def fetch_customer_rtn(self):
		self.ensure_one ()
		return self.account_move.partner_id.customer_rtn

	def fetch_final_consumer(self):
		self.ensure_one ()
		return self.account_move.partner_id.final_consumer
	