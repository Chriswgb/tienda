from itertools import groupby
from datetime import datetime, timedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_is_zero, float_compare, DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tools.misc import formatLang
from odoo.tools import html2plaintext
import odoo.addons.decimal_precision as dp

class PosPaymentMethodInherit(models.Model):
    _inherit="pos.payment.method"
    _description="POS Payment Method Inherit"

    card_information = fields.Boolean(string="Agregar información de tarjeta")
    cheque_information = fields.Boolean(string="Agregar información de cheque")

    @api.onchange('card_information')
    def change_cheque(self):
        if self.card_information:
            self.cheque_information = False

    @api.onchange('cheque_information')
    def change_card(self):
        if self.cheque_information:
            self.card_information = False