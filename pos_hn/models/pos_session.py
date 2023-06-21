from odoo import models, fields, api, _
from odoo.osv.expression import AND

class PosSessionInherit(models.Model):
    _inherit="pos.session"
    _description="POS Session Inherit"

    total_ventas= fields.Float("Total de Ventas",compute="get_totales")
    total_pagos = fields.Float("Total de pagos", compute="get_totales_pagados")
    total_devolucion = fields.Float("Total de Devolucion", compute="get_totales")


    is_listo = fields.Boolean()

    corte_caja_detail_wizard_ids=fields.One2many("corte.caja.detail.wizard","corte_caja_wizard_2_id","corte_caja_detail_wizard_ids")
    corte_caja_diario_cuenta_ids = fields.One2many("corte.caja.diario.cuenta","corte_caja_diario_cuenta_2_id", "corte_caja_diario_cuenta_ids")
    corte_caja_pagos_ids=fields.One2many("corte.caja.pagos","corte_caja_pago_id","corte_caja_pagos_ids")

    @api.depends("corte_caja_diario_cuenta_ids.monto")
    def get_totales_pagados(self):
            for record in self:
                record.total_pagos = sum(r.monto for r in record.corte_caja_diario_cuenta_ids)

    @api.depends('corte_caja_detail_wizard_ids.montototal')
    def get_totales(self):
        for record in self:
            record.total_ventas=sum(r.montototal for r in record.corte_caja_detail_wizard_ids if r.tipo_doc == "out_invoice")
            record.total_devolucion=sum(r.montototal for r in record.corte_caja_detail_wizard_ids if r.tipo_doc == "out_refund")

    def obtener_datos(self):
        obj_delete=self.env["corte.caja.detail.wizard"].search([('corte_caja_wizard_2_id','=',self.id)]).unlink()
        obj_create=self.env["corte.caja.detail.wizard"]

        query=  """
                select mo.name as no_documento,mo.date as fecha_doc,pa.vat as rtn,
                pa.name as cliente,mo.move_type as tipo_doc,
                ord.amount_total as montototal
                from public.pos_order as ord
                join public.res_partner as pa on pa.id = ord.partner_id
                join public.pos_session as se on se.id = ord.session_id
                join public.account_move as mo on mo.id = ord.account_move
                where se.id=%s
                """
        self.env.cr.execute(query,(self.id,))
        result=self.env.cr.fetchall()
        
        for r in result:
            vals={
                'no_documento':r[0],
                'fecha_doc':r[1],
                'rtn':r[2],
                'cliente':r[3],
                'tipo_doc':r[4],
                'montototal':r[5],
                
                'corte_caja_wizard_2_id':self.id

            }
            obj_create.create(vals)

        obj_delete=self.env["corte.caja.diario.cuenta"].search([('corte_caja_diario_cuenta_2_id','=',self.id)]).unlink()
        obj_create=self.env["corte.caja.diario.cuenta"]

        query2= """
                SELECT sum(pp.amount) as monto, ppm.name
                FROM public.pos_payment as pp
                JOIN public.pos_payment_method AS ppm ON ppm.id = pp.payment_method_id
                JOIN public.pos_session as ps on ps.id= pp.session_id
                where ps.id=%s
                group by ppm.name
                """
        self.env.cr.execute(query2,(self.id,))
        result=self.env.cr.fetchall()

        for r2 in result:
            vals={
                'monto':r2[0],
                'cuenta':r2[1],
                
                
                'corte_caja_diario_cuenta_2_id':self.id

            }
            obj_create.create(vals)
        obj_delete=self.env["corte.caja.pagos"].search([('corte_caja_pago_id','=',self.id)]).unlink()
        obj_create=self.env["corte.caja.pagos"]

        query3= """
                SELECT pp.payment_date as fecha_pago,po.name as orden, pp.amount as importe,ppm.name as metodo_pago,ps.name as sesion
                FROM public.pos_payment as pp
                join public.pos_session as ps on ps.id= pp.session_id
                join public.pos_order as po on po.id=pp.pos_order_id
                join public.pos_payment_method as ppm on ppm.id=pp.payment_method_id
                where ps.id=%s
                """
        self.env.cr.execute(query3,(self.id,))
        result=self.env.cr.fetchall()
        for r3 in result:
            vals={
                'fecha_pago':r3[0],
                'orden':r3[1],
                'importe':r3[2],
                'metodo_pago':r3[3],
                
                
                'corte_caja_pago_id':self.id

            }
            obj_create.create(vals)

        for record in self:
            if record.state == "closed":
                record.is_listo = True

class CorteCajaDetailWizard(models.Model):
    _name="corte.caja.detail.wizard"
    _description="Corte de caja"

    no_documento=fields.Char("Número de Documento")
    fecha_doc=fields.Char("Fecha de Documento")
    rtn=fields.Char("RTN")
    cliente=fields.Char("Cliente")
    tipo_doc=fields.Char("Tipo de Documento")
    montototal=fields.Float("Total")
    monto_devolucion=fields.Float("Monto Devolución")

    corte_caja_wizard_2_id=fields.Many2one("pos.session","corte_caja_wizard_2_id")


class CorteCajaDiarioCuenta(models.Model):
    _name = "corte.caja.diario.cuenta"
    _description="Corte de caja cuenta"

    cuenta = fields.Char("Cuenta")
    monto = fields.Float("Monto")

    corte_caja_diario_cuenta_2_id = fields.Many2one("pos.session", "corte_caja_diario_cuenta_2_id")

class CorteCajaPagos(models.Model):
    _name='corte.caja.pagos'
    _description="Corte de caja pagos"

    fecha_pago=fields.Datetime("Fecha de Pago")
    orden=fields.Char('Orden')
    importe=fields.Float('importe')
    metodo_pago=fields.Char('Metodo de Pago')  

    corte_caja_pago_id=fields.Many2one("pos.session","corte_caja_pago_id")
