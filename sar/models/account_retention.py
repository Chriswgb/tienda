from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

class AccountRetentionInherit(models.Model):
    _name = "account.retention"
    _description = "Retenciones"
    _inherit = ['mail.thread']
   
    name = fields.Char(string="Nombre", tracking=True)
    code = fields.Char(string="Codigo", tracking=True)
    percentage = fields.Float(string="Porcentaje", tracking=True)
    account_id = fields.Many2one(string="Cuenta", comodel_name="account.account", tracking=True)
    leyenda1=fields.Char(string="Leyenda 1", tracking=True)
    leyenda2=fields.Text(string="Leyenda 2", tracking=True)

    def name_get(self):
        result = []
        for rec in self:
            result.append((rec.id, '%s - %s' % (rec.code,rec.name)))
             
        return result