from itertools import groupby
from datetime import datetime, timedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_is_zero, float_compare, DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tools.misc import formatLang
from odoo.tools import html2plaintext
import odoo.addons.decimal_precision as dp

class PosOrderInherit(models.Model):
    _inherit="pos.order"
    _description="POS Order Inherit"

    account_move_name= fields.Char("Factura", related="account_move.name") 

    def _process_payment_lines(self, pos_order, order, pos_session, draft):
        """Create account.bank.statement.lines from the dictionary given to the parent function.

        If the payment_line is an updated version of an existing one, the existing payment_line will first be
        removed before making a new one.
        :param pos_order: dictionary representing the order.
        :type pos_order: dict.
        :param order: Order object the payment lines should belong to.
        :type order: pos.order
        :param pos_session: PoS session the order was created in.
        :type pos_session: pos.session
        :param draft: Indicate that the pos_order is not validated yet.
        :type draft: bool.
        """
        prec_acc = order.pricelist_id.currency_id.decimal_places
        order_bank_statement_lines= self.env['pos.payment'].search([('pos_order_id', '=', order.id)])
        order_bank_statement_lines.unlink()
        for payments in pos_order['statement_ids']:
            if not float_is_zero(payments[2]['amount'], precision_digits=prec_acc):
                order.add_payment(self._payment_fields(order, payments[2], pos_order))

        order.amount_paid = sum(order.payment_ids.mapped('amount'))

        if not draft and not float_is_zero(pos_order['amount_return'], prec_acc):
            cash_payment_method = pos_session.payment_method_ids.filtered('is_cash_count')[:1]
            if not cash_payment_method:
                raise UserError(_("No cash statement found for this session. Unable to record returned cash."))
            return_payment_vals = {
                'name': _('return'),
                'pos_order_id': order.id,
                'amount': -pos_order['amount_return'],
                'payment_date': fields.Date.context_today(self),
                'payment_method_id': cash_payment_method.id,
                'card_number' : pos_order.get('card_number'),
                'expiration_date' : pos_order.get('expiration_date'),
                'security_code' : pos_order.get('security_code'),
                'cheque_number' : pos_order.get('cheque_number'),
            }
            order.add_payment(return_payment_vals)
        
    def _payment_fields(self, order, ui_paymentline, pos_order):
        payment_date = ui_paymentline['name']
        payment_date = fields.Date.context_today(self, fields.Datetime.from_string(payment_date))
        payment_method = self.env['pos.payment.method'].browse(ui_paymentline['payment_method_id'])
        if payment_method.card_information == True:
            return {
                'amount': ui_paymentline['amount'] or 0.0,
                'payment_date': payment_date,
                'payment_method_id': ui_paymentline['payment_method_id'],
                'card_type': ui_paymentline.get('card_type'),
                'transaction_id': ui_paymentline.get('transaction_id'),
                'pos_order_id': order.id,
                'card_number' : pos_order.get('card_number'),
                'expiration_date' : pos_order.get('expiration_date'),
                'security_code' : pos_order.get('security_code')
            }
        elif payment_method.cheque_information == True:
            return {
                'amount': ui_paymentline['amount'] or 0.0,
                'payment_date': payment_date,
                'payment_method_id': ui_paymentline['payment_method_id'],
                'card_type': ui_paymentline.get('card_type'),
                'transaction_id': ui_paymentline.get('transaction_id'),
                'pos_order_id': order.id,
                'cheque_number' : pos_order.get('cheque_number'),
            }
        else:
            return {
                'amount': ui_paymentline['amount'] or 0.0,
                'payment_date': payment_date,
                'payment_method_id': ui_paymentline['payment_method_id'],
                'card_type': ui_paymentline.get('card_type'),
                'transaction_id': ui_paymentline.get('transaction_id'),
                'pos_order_id': order.id,
            }

    # esta funcion se utiliza en ReceiptScreen.js
    def set_note(self, note):
        self.write({'note': note}) 