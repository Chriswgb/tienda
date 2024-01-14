from odoo import models, fields, api

class ResUsers(models.Model):
	_inherit = "res.users"

	pos_ids = fields.Many2many("pos.config", "pos_users_rel", "user_id", "pos_id", string="POS permitidos")