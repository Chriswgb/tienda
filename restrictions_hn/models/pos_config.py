from odoo import models, fields, api

class PosConfig(models.Model):
	_inherit = "pos.config"

	users_ids = fields.Many2many("res.users", "pos_users_rel", "pos_id", "user_id", string="Usuarios permitidos")

	@api.model
	def search(self, args, offset=0, limit=None, order=None, count=False):
		args += [('users_ids', 'in', self.env.user.id)]
		
		return super(PosConfig, self).search(args=args, offset=offset, limit=limit, order=order, count=count)
	