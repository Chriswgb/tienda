from odoo import fields, api, models


class ResPartnerInherit(models.Model):
    _inherit="res.partner"

    customer_name = fields.Char(string="Nombre de cliente")
    customer_rtn = fields.Char(string="RTN de cliente")