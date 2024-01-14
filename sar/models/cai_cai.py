# -*- coding: utf-8 -*-
from odoo.http import request
from odoo import models, fields, api, _
from odoo.exceptions import Warning, ValidationError
from datetime import timedelta, datetime

class Cai(models.Model):
    _name = "cai.cai"
    _description = "Números proporcionados por la SAR"
    _inherit = ['mail.thread']

    # Datos generales
    name = fields.Char(string="CAI", tracking=True)
    min_number = fields.Char(string="Rango autorizado desde", tracking=True)
    max_number = fields.Char(string="Rango autorizado hasta", tracking=True)
    expiration_date = fields.Date(string="Fecha limite de emisión", tracking=True)
    description = fields.Char(string="Descripción", tracking=True)
    
    #secuencia
    prefijo = fields.Char(string="Prefijo")
    size_secuencia = fields.Integer(string="Tamaño de secuencia")
    valor_inicial = fields.Integer(string="Valor inicial")
    valor_final = fields.Integer(string="Valor final")
    sequence_id = fields.Many2one(string="Secuencia", comodel_name="ir.sequence", copy=False)
    porcentaje = fields.Float(string='Porcentaje', compute='compute_percentage')
    usados= fields.Integer(string="Usados", compute='compute_percentage')
    alerta_porcentaje_enviada = fields.Boolean("Alerta Porcentaje Enviada", default=False)
    alerta_fecha_enviada = fields.Boolean("Alerta Fecha Enviada", default=False)

    #agregar selection con tipo de Cai
    tipo = fields.Selection(string="Tipo", selection=[('ventas', 'Factura'),('nota_credito', 'Nota de Crédito'),('nota_debito', 'Nota de Débito'),('retencion', 'Retención'),('guia_remision', 'Guía de Remisión'),])
    state = fields.Selection(string="Estado", selection=[('draft', 'Borrador'),('progress', 'En proceso'),('done', 'Finalizado')], default="draft")

    def name_get(self):
        result = []
    
        for rec in self:
            result.append((rec.id, '%s - %s' % (rec.description, rec.name)))
             
        return result


    def cai_notifications(self):
        emails = False
        cai_ids = self.search([('state','=','progress')])
        notification_group_id = self.env.ref('sar.group_send_notification_cai')
        if notification_group_id and notification_group_id.users:
            emails = ','.join(x.login for x in notification_group_id.users)

        today = datetime.now() - timedelta(hours=6)
        if emails:        
            for cai in cai_ids:
                diff_dates = cai.expiration_date - today.date()
                diff = cai.valor_final - cai.sequence_id.number_next_actual
                
                if diff <= 50:
                    self.send_email(emails, diff, cai.name, 'sequence')

                if diff_dates.days < 3:
                    self.send_email(emails, abs(diff_dates.days), cai.name, 'dates')

                
    def send_email(self, emails, diff, cai, type_sequence):
        if emails:
            mail_mail = self.env['mail.mail']
            if type_sequence == 'sequence':
                mail_message = {
                    'subject': 'Notificacion de CAI',
                    'body_html': "Quedan %s numeros disponibles del cai %s"%(diff, cai),
                    'email_to': emails,
                    'state': 'outgoing',
                    'auto_delete': True,
                }
            else:
                mail_message = {
                    'subject': 'Notificacion de CAI',
                    'body_html': "La fecha del CAI %s esta a punto de expirar, quedan %s dias."%(cai, diff),
                    'email_to': emails,
                    'state': 'outgoing',
                    'auto_delete': True,
                }
            mail_id = mail_mail.create(mail_message)
            mail_id.send()


    @api.depends('sequence_id.number_next_actual')
    def compute_percentage(self):

        for record in self:
            # recupero y calculo el valor actual en el que va la secuencia
            numerador = record.sequence_id.number_next_actual - record.valor_inicial
            denominador = (record.valor_final - record.valor_inicial) + 1

            if record.valor_inicial == record.sequence_id.number_next_actual:
                record.porcentaje = 0
            elif (record.sequence_id.number_next_actual) -1 == record.valor_final:
                record.porcentaje = 100
                record.state = 'done'
            else:
                if denominador > 0:
                    record.porcentaje = (numerador / denominador) * 100
                else:
                    record.porcentaje = 0

            # numero de secuencias usadas del CAI
            record.usados = numerador


    def unlink(self):
        for r in self:
            if r.state != "draft":
                raise Warning(('No puede borrar este registro'))

        return super(Cai, self).unlink()

    def setProcess(self):
        if self.sequence_id:
            self.sequence_id.sudo().write({'number_next_actual':self.valor_inicial})
        else:
            obj_create = self.env["ir.sequence"]

            vals = {
                "name":"CAI "+self.name,
                "implementation":"standard",
                "prefix": self.prefijo,
                "padding": self.size_secuencia,
                "number_next_actual": self.valor_inicial
            }

            obj_id = obj_create.sudo().create(vals)
            obj_id.sudo().number_next_actual = self.valor_inicial
            self.sequence_id = obj_id.id

        self.write({'state':'progress'})
    
    def setDraft(self):

        self.write({'state':'draft'})
        