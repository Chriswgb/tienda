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
    sequence_id = fields.Many2one(string="Secuencia", comodel_name="ir.sequence")
    porcentaje = fields.Float(string='Porcentaje', compute='compute_percentage')
    usados= fields.Integer(string="Usados", compute='compute_percentage')
    alerta_porcentaje_enviada = fields.Boolean("Alerta Porcentaje Enviada", default=False)
    alerta_fecha_enviada = fields.Boolean("Alerta Fecha Enviada", default=False)

    #agregar selection con tipo de Cai
    tipo = fields.Selection(
        string="Tipo",
        selection=[
            ('ventas', 'Factura'),
            ('nota_credito', 'Nota de Crédito'),
            ('nota_debito', 'Nota de Débito'),
            ('retencion', 'Retención'),
            ('guia_remision', 'Guía de Remisión'),
        ]
    )

    state = fields.Selection(
        string="Estado",
        selection=[
            ('draft', 'Borrador'), 
            ('progress', 'En proceso'), 
            ('done', 'Finalizado')
        ],
        default="draft"
    )

    def name_get(self):
        result = []
    
        for rec in self:
            result.append((rec.id, '%s - %s' % (rec.description, rec.name)))
             
        return result


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


    def enviar_correo_alerta(self, cai, tipo_alerta):
        
        if self.env.company.email:
            subject = 'Alerta CAI'
            recipients = self.env.company.email

            base_url = request.env['ir.config_parameter'].get_param('web.base.url')
            base_url += '/web#id=%d&view_type=form&model=%s' % (cai.id, cai._name)

            if tipo_alerta == "porcentaje":
                message_body = f"""    
                                Se le notifica que el número de CAI ({cai.name}), está por llegar a su totalidad.

                                {base_url}
                                """
            else:
                message_body = f"""
                                Se le notifica que el número de CAI ({cai.name}), vencerá el {cai.expiration_date}.

                                {base_url}
                                """

            template_obj = self.env['mail.mail'].sudo()

            template_data = {
            'subject': subject,
            'body_html': message_body,
            'email_to': recipients
            }

            template_id = template_obj.create(template_data)
            template_obj.send(template_id)

            try:
                template_id.send()
                if tipo_alerta=="porcentaje":
                    cai.write({'alerta_porcentaje_enviada': 1})
                else:
                    cai.write({'alerta_fecha_enviada': 1})
            except:
                raise ValidationError("Ocurrio un error durante el proceso, por favor intentelo mas tarde")


    def unlink(self):
        for r in self:
            if r.state != "draft":
                raise Warning(('No puede borrar este registro'))

        return super(Cai, self).unlink()

    def setProcess(self):

        if self.sequence_id:
            self.sequence_id.unlink()
        
        #pasar a finalizado todos los registros en estado proceso
        '''query = """UPDATE
                        cai
                    SET
                        state="done"
                    WHERE
                        state="progress";"""

        self.env.cr.execute(query)'''
        
        obj_create = self.env["ir.sequence"]

        vals = {
            "name":"CAI "+self.name,
            "implementation":"standard",
            "prefix": self.prefijo,
            "padding": self.size_secuencia,
            "number_next_actual": self.valor_inicial
        }

        obj_id = obj_create.create(vals)
        obj_id.number_next_actual = self.valor_inicial
        self.sequence_id = obj_id.id

        self.write({'state':'progress'})
    
    def setDraft(self):

        self.write({'state':'draft'})
        