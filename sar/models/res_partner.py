from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import timedelta, datetime

class ResPartner(models.Model):
    _inherit = "res.partner"

    id_number = fields.Char(string="Número de identidad")
    rtn = fields.Char(string="RTN")
    exclude_rtn = fields.Char(string="Excluir rtn")