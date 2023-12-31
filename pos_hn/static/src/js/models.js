odoo.define('.pos_default_customer', function(require) {
    "use strict";

    var models = require('point_of_sale.models');

    var _super_order = models.Order.prototype;
    models.Order = models.Order.extend({
        initialize: function() {
            _super_order.initialize.apply(this, arguments);

            var customer = this.pos.config.default_customer_id;

            // establezco el cliente por defecto
            if (customer) {
                this.set_client(this.pos.db.get_partner_by_id(customer[0]));
            }

            // establezco verdadero a esta variable para que el boton de crear factura en el pos
            // siempre este presionado
            this.to_invoice = true
        },
    });
});