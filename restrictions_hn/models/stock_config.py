# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class StockConfigInherit(models.TransientModel):
	#heredamos el modelo que contiene las configuraciones del modulo stock
	_inherit = "res.config.settings"
	
	#agregamos un campo que haga referencia al modelo de las secuencias
	product_sequence_id = fields.Many2one(comodel_name="ir.sequence", string="Secuencia para el código del producto", config_parameter='res_config_settings.product_sequence_id')