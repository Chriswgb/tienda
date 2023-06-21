odoo.define('.ClientDetailsEdit', function(require) {
    'use strict';

    var models = require('point_of_sale.models')
    var _super_posmodel = models.PosModel.prototype;
    
    models.PosModel = models.PosModel.extend({
    initialize: function (session, attributes) {
        // Add field to model
        var partner_model = _.find(this.models, function(model){
            return model.model === 'res.partner';
        });
        partner_model.fields.push('street');
        partner_model.fields.push('customer_name');
        partner_model.fields.push('customer_rtn');
        partner_model.fields.push('rtn');
        // run Super
        return _super_posmodel.initialize.call(this, session, attributes)
        },
    });

});