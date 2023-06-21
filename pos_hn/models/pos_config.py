from odoo import models, fields


class PosConfigInherit(models.Model):
    _inherit="pos.config"
    _description="POS Config Inherit"

    default_customer_id = fields.Many2one('res.partner', string='Cliente Por Defecto')

    card_information = fields.Boolean(string="Agregar información de tarjetas")
    cheque_information = fields.Boolean(string="Agregar información de cheques")

    specific_address = fields.Char("Dirección Especifica")
    general_address = fields.Char("Dirección General")
