from odoo import models, fields, api
from odoo.tools.translate import _
from odoo.exceptions import UserError

class AccountMoveRetention(models.TransientModel):
    _name = 'account.move.retention'
    _description = 'Account Move Retention'

    retention_id = fields.Many2one(string="Retención", comodel_name="account.retention", required=1)
    percentage = fields.Float(string="Porcentaje", related="retention_id.percentage")
    amount_retention = fields.Float(string="Monto de retención", compute="_get_amount_retention")

    @api.onchange('retention_id','amount_untaxed')
    def _get_amount_retention(self):
        move_id = self.env.context.get('active_id', [])
        move_id_rec = self.env['account.move'].browse(move_id)
        for record in self:
            if record.retention_id:
                record.amount_retention = (move_id_rec.amount_untaxed * record.percentage)
            else:
                record.amount_retention = 0

    #Funcion para crear el comprobante de Retencion
    def retention_moves(self):
        #captura el id de la factura actual con el active_id
        move_id = self.env.context.get('active_id', [])
        #se busca en el modelo account.move con el id actual capturado en la variable anterior
        move_id_rec = self.env['account.move'].browse(move_id)
        
        #Se declara un arreglo
        lineas = []
        #se declara un diccionario con los campos un solo registro
        vals = {
            'name': self.retention_id.name,
            'account_id': self.retention_id.account_id.id,
            'quantity': 1,
            'price_unit': self.amount_retention,
        }
        # 0,0 es el codigo para crear
        lineas.append((0, 0, vals))
        
        #tiene todo el contenido de la factura
        invoice_vals = {
            'ref': 'Retención de ' + move_id_rec.name,
            'move_type': 'in_refund',
            'narration': move_id_rec.narration,
            'currency_id': move_id_rec.currency_id.id,
            'user_id': move_id_rec.user_id.id,
            'invoice_user_id': move_id_rec.invoice_user_id.id,
            'partner_id': move_id_rec.partner_id.id,
            'is_retention': True,
            'factura_id': move_id_rec.id,
            'retention_id': self.retention_id.id,
            'journal_id': move_id_rec.journal_id.id,  # company comes from the journal
            'invoice_payment_term_id': move_id_rec.invoice_payment_term_id.id,
            'payment_reference': move_id_rec.payment_reference,
            'invoice_line_ids': lineas,
            'company_id': move_id_rec.company_id.id,
        }
        
        #recuperar el id del movimiento y se crea el nuevo registro
        new_moves = self.env['account.move'].create(invoice_vals)
        
        #redireccionar al movimiento creado
        action = {
            'name': _('Reverse Moves'),
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
        }
        if len(new_moves) == 1:
            action.update({
                'view_mode': 'form',
                'res_id': new_moves.id,
                'context': {'default_move_type':  new_moves.move_type},
            })

        return action
