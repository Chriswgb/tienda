from odoo import models, fields, api

class ResCompanyInherit(models.Model):
    _inherit="res.company"

    rtn = fields.Char("RTN")