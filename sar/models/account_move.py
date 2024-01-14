# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import timedelta, datetime
from num2words import num2words
from decimal import Decimal, ROUND_HALF_UP, ROUND_HALF_EVEN


class AccountMove(models.Model):
    _inherit = "account.move"
   
    amount_total_text = fields.Char(string="Total en letras", compute='get_totalt', default='Cero')
    # Unique number of the invoice, computed automatically when the invoice is created
    internal_number = fields.Char(string='Número interno', readonly=True)

    #CAI DE FACTURAS DE CLIENTES
    cai_shot = fields.Char(string="CAI")
    cai_expires_shot = fields.Date(string="Fecha de expiración")
    min_number_shot = fields.Char(string="Número minímo ", readonly=True)
    max_number_shot = fields.Char(string="Número máximo", readonly=True)
    cai_create = fields.Boolean(string="Cai creado")
      
    # Campos necesarios para la retencion
    is_retention = fields.Boolean(string="Es retención")
    retention_id = fields.Many2one(string="Retención", comodel_name="account.retention")
    factura_id = fields.Many2one(string="Factura", comodel_name="account.move")


    numero_orden_excenta = fields.Char("No. Orden de compra excenta")
    numero_constancia_exoneracion = fields.Char("No. Constancia de registro de exoneración")
    numero_sag = fields.Char("No. Identificación del registro de la SAG")

    # campo agregado para factura de proveedor
    cai_proveedor = fields.Char("CAI de Factura Proveedor")
    
    def _post(self, soft=True):
        res = super(AccountMove, self)._post(soft=True)
        for inv in self:
            if inv.move_type in ('out_invoice', 'in_invoice', 'out_refund', 'in_refund'):
                factura_proveedor = False
                if inv.move_type == 'out_invoice':
                    # si la factura tiene este debit_origin_id es por que es una nota de debito
                    if inv.debit_origin_id:
                        cai = inv.journal_id.cai_nota_debito
                        # establezco cai_create en None por que odoo lo trae de la factura anterior por defecto y jala el cai que no es
                        inv.cai_create = None
                    else: 
                        cai = inv.journal_id.cai_ventas

                elif inv.move_type == "in_invoice":
                    if inv.debit_origin_id:
                        cai = inv.journal_id.cai_nota_debito
                    else:
                        factura_proveedor = True

                else:
                    if inv.is_retention == True:
                        cai = inv.journal_id.cai_retencion
                    elif inv.move_type == "out_refund":
                        cai = inv.journal_id.cai_nota_credito

                        # establezco cai_create en None por que odoo lo trae de la factura anterior por defecto y jala el cai que no es
                        inv.cai_create = None
                    else:
                        factura_proveedor = True

                if not factura_proveedor:
                   
                    if cai:

                        if  inv.invoice_date > cai.expiration_date:
                            raise ValidationError(_('La fecha de factura es mayor que la fecha de expiración del CAI'))
                        
                        if (cai.sequence_id.number_next_actual - 1) > (cai.valor_final - 1):
                            raise ValidationError(_('Ya llego al valor final de su rango de facturación, solicite uno nuevo'))

                        # Cambio de estado de a terminado
                        if (cai.sequence_id.number_next_actual + 1) > cai.valor_final:
                            cai.write({'state':'done'})
                        
                        if not inv.cai_create:
                            new_name = cai.sequence_id.with_context(ir_sequence_date=inv.invoice_date).next_by_id()

                            inv.write({'name': new_name})
                            inv.write({'internal_number': new_name})
                            inv.write({'payment_reference': new_name})
                            inv.cai_expires_shot = cai.expiration_date
                            inv.min_number_shot = cai.min_number
                            inv.max_number_shot = cai.max_number
                            inv.cai_shot = cai.name
                            inv.cai_create = True

                            # modifico el label del asiento contable al nuevo valor de la secuencia del CAI
                            to_write = {
                            'payment_reference': new_name,
                            'line_ids': []
                            }
                            for line in inv.line_ids.filtered(lambda line: line.account_id.user_type_id.type in ('receivable', 'payable')):
                                to_write['line_ids'].append((1, line.id, {'name': to_write['payment_reference']}))
                            inv.write(to_write)
                    
                    else:
                        raise ValidationError(_('No existe ningún CAI en proceso'))
                
        return res
    
    @api.depends('amount_total')
    def get_totalt(self):
        for rec in self: 
            rec.amount_total_text= rec.decimal_a_letras(rec.amount_total)
            return True
    
    def decimal_a_letras(self, numero):
        for rec in self:
            numero_entero = int(numero)
            numero_decimal = int(Decimal(numero - numero_entero).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP) * 100)
            return str(str(num2words(numero_entero, lang='es')) + ' con ' + str(numero_decimal) + '/100')

    def action_retention(self):
        return {
            'type':'ir.actions.act_window',
            'name':'Elegir retencion a aplicar',
            'res_model':'account.move.retention',
            'view_mode': 'form',
            'view_type': 'form',
            'target': 'new',
            'context': {
                'active_model': 'account.move',
                'active_id': self.id,
            } 
        }


class SequenceMixinInherit(models.AbstractModel):
    _inherit  = 'sequence.mixin'

    def _constrains_date_sequence(self):
        return
                    
