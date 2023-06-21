from odoo import models, fields, api

class ResCompanyInherit(models.Model):
    _inherit="res.company"

    nombre_comercial = fields.Char("Nombre Comercial")
    rtn = fields.Char("RTN")
    whatsapp = fields.Char("Whatsapp")