from itertools import groupby
from datetime import datetime, timedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_is_zero, float_compare, DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tools.misc import formatLang
from odoo.tools import html2plaintext
import odoo.addons.decimal_precision as dp

class PosPaymentInherit(models.Model):
    _inherit="pos.payment"
    _description="POS Payment Inherit"

    # Datos de tarjeta
    card_number = fields.Char(string="Número de tarjeta")
    expiration_date= fields.Char(string="Fecha de vencimiento")
    security_code = fields.Char(string="Código de seguridad")
    # Datos de cheque
    cheque_number = fields.Char(string="Número de cheque")
