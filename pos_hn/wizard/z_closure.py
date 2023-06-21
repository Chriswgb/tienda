from odoo import models, fields, api


class ZClosure(models.TransientModel):
    _name="z.closure"
    _description="Wizard para crear reporte de ciere z"
    _rec_name="date"

    date = fields.Date("Fecha")

    user_id = fields.Many2one(
        string="Creado por",
        comodel_name="res.users",
        default=lambda self: self.env.user.id
    )

    company_id = fields.Many2one(
        string='Company',
        comodel_name='res.company',
        default=lambda self: self.env.company.id, 
        index=1
    )


    def get_data(self):
        inv_ref = self.get_invoices_and_refunds()
        payments = self.get_payments()
        methods = self.get_methods_amount()
        points = self.get_points()

        data = {
            'user_name': self.user_id.name,
            'company': self.company_id.read(['logo'])[0],
            'date': self.date,
            'invoices': inv_ref,
            'payments': payments,
            'methods': methods,
            'points': points
        }

        return self.env.ref('pos_hn.z_closure_report').report_action(self, data=data)


    def get_invoices_and_refunds(self):
        query = """SELECT 
                    am.name as invoice_no,
                    am.invoice_date,
                    rp.vat as client_rtn, 
                    rp.name as client_name,
                    am.move_type,
                    o.amount_total
                FROM pos_order o
                JOIN res_partner rp on o.partner_id = rp.id
                JOIN account_move am on o.account_move = am.id
                WHERE (o.date_order at time zone 'utc' at time zone 'CST')::text like %s
                AND am.move_type in ('out_invoice', 'out_refund')
        """
        params = [f'{self.date}%']

        self.env.cr.execute(query, params) 

        result = self.env.cr.dictfetchall()

        return result

    def get_payments(self):
        query = """SELECT 
                    pp.payment_date,
                    po.name as order,
                    ppm.name as method,
                    pp.amount
                FROM pos_payment pp
                JOIN pos_order po on pp.pos_order_id = po.id
                JOIN pos_payment_method ppm on pp.payment_method_id = ppm.id
                WHERE (po.date_order at time zone 'utc' at time zone 'CST')::text like %s
            """
        params = [f'{self.date}%']

        self.env.cr.execute(query, params) 

        result = self.env.cr.dictfetchall()

        return result


    def get_methods_amount(self):
        query = """SELECT 
                    sum(pp.amount) as amount, 
                    ppm.name as method
                FROM pos_order po
                JOIN pos_payment pp on pp.pos_order_id = po.id
                JOIN pos_payment_method AS ppm ON ppm.id = pp.payment_method_id
                WHERE (po.date_order at time zone 'utc' at time zone 'CST')::text like %s
                group by ppm.name
            """

        params = [f'{self.date}%']

        self.env.cr.execute(query, params) 

        result = self.env.cr.dictfetchall()

        return result

    
    def get_points(self):
        query = """SELECT 
                    pc.name as point,
                    sum(po.amount_total) as total
                FROM pos_order po
                JOIN pos_session ps on po.session_id = ps.id
                JOIN pos_config pc on ps.config_id = pc.id
                WHERE (date_order at time zone 'utc' at time zone 'CST')::text like %s
                GROUP BY pc.name;
        """

        params = [f'{self.date}%']

        self.env.cr.execute(query, params) 

        result = self.env.cr.dictfetchall()

        return result
