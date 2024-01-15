# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class AccountJournal(models.Model):
    _inherit = "account.journal"

    street = fields.Char(string="Dirección de la tienda")
    cai_ventas = fields.Many2one(string="CAI Ventas", comodel_name="cai.cai", domain=[('tipo', '=', 'ventas'),('state', '=', 'progress')])
    cai_nota_credito = fields.Many2one(string="CAI Notas de Crédito", comodel_name="cai.cai", domain=[('tipo', '=', 'nota_credito'),('state', '=', 'progress')])
    cai_nota_debito = fields.Many2one(string="CAI Notas de Débito", comodel_name="cai.cai", domain=[('tipo', '=', 'nota_debito'),('state', '=', 'progress')])
    cai_retencion = fields.Many2one(string="CAI Retención", comodel_name="cai.cai", domain=[('tipo', '=', 'retencion'),('state', '=', 'progress')])
