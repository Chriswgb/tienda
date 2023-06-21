odoo.define('.ReprintReceiptButton', function (require) {
    'use strict';

    const ReprintReceiptButton = require('point_of_sale.ReprintReceiptButton');
    const Registries = require('point_of_sale.Registries');
    const models = require('point_of_sale.models')


    var _super_order = models.Order.prototype;
    models.Order = models.Order.extend({
        export_for_printing: function () {
            var result = _super_order.export_for_printing.apply(this, arguments);
            result.invoice_number = this.getInvoiceNumber();
            result.cai_number = this.getCaiNumber();
            result.cai_expires_shot = this.getCaiExpiresShot();
            result.min_cai = this.getMinCai();
            result.max_cai = this.getMaxCai();
            result.amount_untaxed = this.getAmountUntaxed();
            result.amount_tax = this.getAmountTax();
            result.amount_total_text = this.getAmountTotalText();
            result.excento = this.getExcento();
            result.exonerado = this.getExonerado();
            result.gravado = this.getGravado();
            result.street = this.getStreet();
            result.street2 = this.getStreet2();
            result.city = this.getCity();
            result.state_id = this.getStateId();
            result.rtn = this.getRtn();
            result.nombre_comercial = this.getNombreComercial();
            result.phone = this.getPhone();
            result.whatsapp = this.getWhatsapp();
            result.gravado18 = this.getGravado18();
            result.impuesto18 = this.getImpuesto18();
            result.rtn2 = this.getRtn2();
            result.customer_name = this.getCustomerName();
            result.customer_rtn = this.getCustomerRtn();
            result.final_consumer = this.getFinalConsumer();

            return result;
        },

        setInvoiceNumber: function (invoice_number) {
            this.invoice_number = invoice_number;
        },
        getInvoiceNumber: function () {
            return this.invoice_number;
        },

        setCaiNumber: function (cai_number) {
            this.cai_number = cai_number;
        },
        getCaiNumber: function () {
            return this.cai_number;
        },

        setCaiExpiresShot: function (cai_expires_shot) {
            this.cai_expires_shot = cai_expires_shot;
        },

        getCaiExpiresShot: function () {
            return this.cai_expires_shot;
        },

        setMinCai: function (min_cai) {
            this.min_cai = min_cai;
        },

        getMinCai: function () {
            return this.min_cai;
        },

        setMaxCai: function (max_cai) {
            this.max_cai = max_cai;
        },

        getMaxCai: function () {
            return this.max_cai;
        },

        setAmountUntaxed: function (amount_untaxed) {
            this.amount_untaxed = amount_untaxed;
        },

        getAmountUntaxed: function () {
            return this.amount_untaxed;
        },

        setAmountTax: function (amount_tax) {
            this.amount_tax = amount_tax;
        },

        getAmountTax: function () {
            return this.amount_tax;
        },

        setAmountTotalText: function (amount_total_text) {
            this.amount_total_text = amount_total_text;
        },

        getAmountTotalText: function () {
            return this.amount_total_text;
        },

        setExcento: function (excento) {
            this.excento = excento;
        },

        getExcento: function () {
            return this.excento;
        },

        setExonerado: function (exonerado) {
            this.exonerado = exonerado;
        },

        getExonerado: function () {
            return this.exonerado;
        },

        setGravado: function (gravado) {
            this.gravado = gravado;
        },

        getGravado: function () {
            return this.gravado;
        },

        setStreet: function (street) {
            this.street = street;
        },

        getStreet: function () {
            return this.street;
        },

        setStreet2: function (street2) {
            this.street2 = street2;
        },

        getStreet2: function () {
            return this.street2;
        },

        setCity: function (city) {
            this.city = city;
        },

        getCity: function () {
            return this.city;
        },

        setStateId: function (state_id) {
            this.state_id = state_id;
        },

        getStateId: function () {
            return this.state_id;
        },

        setRtn: function (rtn) {
            this.rtn = rtn;
        },

        getRtn: function () {
            return this.rtn;
        },

        setRtn2: function (rtn2) {
            this.rtn2 = rtn2;
        },

        getRtn2: function () {
            return this.rtn2;
        },


        setCustomerName: function (customer_name) {
            this.customer_name = customer_name;
        },

        getCustomerName: function () {
            return this.customer_name;
        },

        setCustomerRtn: function (customer_rtn) {
            this.customer_rtn = customer_rtn;
        },

        getCustomerRtn: function () {
            return this.customer_rtn;
        },

        setFinalConsumer: function (final_consumer) {
            this.final_consumer = final_consumer;
        },

        getFinalConsumer: function () {
            return this.final_consumer;
        },

        setNombreComercial: function (nombre_comercial) {
            this.nombre_comercial = nombre_comercial;
        },

        getNombreComercial: function () {
            return this.nombre_comercial;
        },

        setPhone: function (phone) {
            this.phone = phone;
        },

        getPhone: function () {
            return this.phone;
        },

        setWhatsapp: function (whatsapp) {
            this.whatsapp = whatsapp;
        },

        getWhatsapp: function () {
            return this.whatsapp;
        },

        setGravado18: function (gravado18) {
            this.gravado18 = gravado18;
        },

        getGravado18: function () {
            return this.gravado18;
        },

        setImpuesto18: function (impuesto18) {
            this.impuesto18 = impuesto18;
        },

        getImpuesto18: function () {
            return this.impuesto18;
        },

    });

    const ReprintReceiptButtonInherit = ReprintReceiptButton =>
    class extends ReprintReceiptButton {

        async _onClick() {
            console.log(this.props.order)
            if (!this.props.order) return;
            var self = this;
            await self.rpc({
                model: 'pos.order',
                method: 'fetch_invoice_number',
                args: [self.props.order.backendId],
            }).then(function (invoice_number) {
                if (invoice_number) {
                    self.props.order.setInvoiceNumber(invoice_number);
                }
            });

            await self.rpc({
                model: 'pos.order',
                method: 'fetch_cai_number',
                args: [self.props.order.backendId],
            }).then(function (cai_number) {
                if (cai_number) {
                    self.props.order.setCaiNumber(cai_number);
                }
            });

            await self.rpc({
                model: 'pos.order',
                method: 'fetch_expiration_cai',
                args: [self.props.order.backendId],
            }).then(function (cai_expires_shot) {
                if (cai_expires_shot) {
                    self.props.order.setCaiExpiresShot(cai_expires_shot);
                }
            });

            await self.rpc({
                model: 'pos.order',
                method: 'fetch_min_cai',
                args: [self.props.order.backendId],
            }).then(function (min_cai) {
                if (min_cai) {
                    self.props.order.setMinCai(min_cai);
                }
            });

            await self.rpc({
                model: 'pos.order',
                method: 'fetch_max_cai',
                args: [self.props.order.backendId],
            }).then(function (max_cai) {
                if (max_cai) {
                    self.props.order.setMaxCai(max_cai);
                }
            });

            await self.rpc({
                model: 'pos.order',
                method: 'fetch_amount_untaxed',
                args: [self.props.order.backendId],
            }).then(function (amount_untaxed) {
                if (amount_untaxed) {
                    self.props.order.setAmountUntaxed(amount_untaxed);
                }
            });

            await self.rpc({
                model: 'pos.order',
                method: 'fetch_amount_tax',
                args: [self.props.order.backendId],
            }).then(function (amount_tax) {
                if (amount_tax) {
                    self.props.order.setAmountTax(amount_tax);
                }
            });

            await self.rpc({
                model: 'pos.order',
                method: 'fetch_amount_total_text',
                args: [self.props.order.backendId],
            }).then(function (amount_total_text) {
                if (amount_total_text) {
                    self.props.order.setAmountTotalText(amount_total_text);
                }
            });

            await self.rpc({
                model: 'pos.order',
                method: 'fetch_excento',
                args: [self.props.order.backendId],
            }).then(function (excento) {
                if (excento) {
                    self.props.order.setExcento(excento);
                }
            });

            await self.rpc({
                model: 'pos.order',
                method: 'fetch_exonerado',
                args: [self.props.order.backendId],
            }).then(function (exonerado) {
                if (exonerado) {
                    self.props.order.setExonerado(exonerado);
                }
            });

            await self.rpc({
                model: 'pos.order',
                method: 'fetch_gravado',
                args: [self.props.order.backendId],
            }).then(function (gravado) {
                if (gravado) {
                    self.props.order.setGravado(gravado);
                }
            });

            await self.rpc({
                model: 'pos.order',
                method: 'fetch_street',
                args: [self.props.order.backendId],
            }).then(function (street) {
                if (street) {
                    self.props.order.setStreet(street);
                }
            });

            await self.rpc({
                model: 'pos.order',
                method: 'fetch_street2',
                args: [self.props.order.backendId],
            }).then(function (street2) {
                if (street2) {
                    self.props.order.setStreet2(street2);
                }
            });

            await self.rpc({
                model: 'pos.order',
                method: 'fetch_city',
                args: [self.props.order.backendId],
            }).then(function (city) {
                if (city) {
                    self.props.order.setCity(city);
                }
            });

            await self.rpc({
                model: 'pos.order',
                method: 'fetch_state_id',
                args: [self.props.order.backendId],
            }).then(function (state_id) {
                if (state_id) {
                    self.props.order.setStateId(state_id);
                }
            });

            await self.rpc({
                model: 'pos.order',
                method: 'fetch_rtn',
                args: [self.props.order.backendId],
            }).then(function (rtn) {
                if (rtn) {
                    self.props.order.setRtn(rtn);
                }
            });

            await self.rpc({
                model: 'pos.order',
                method: 'fetch_rtn2',
                args: [self.props.order.backendId],
            }).then(function (rtn2) {
                if (rtn2) {
                    self.props.order.setRtn2(rtn2);
                }
            });

            await self.rpc({
                model: 'pos.order',
                method: 'fetch_customer_name',
                args: [self.props.order.backendId],
            }).then(function (customer_name) {
                if (customer_name) {
                    self.props.order.setCustomerName(customer_name);
                }
            });

            await self.rpc({
                model: 'pos.order',
                method: 'fetch_customer_rtn',
                args: [self.props.order.backendId],
            }).then(function (customer_rtn) {
                if (customer_rtn) {
                    self.props.order.setCustomerRtn(customer_rtn);
                }
            });

            await self.rpc({
                model: 'pos.order',
                method: 'fetch_final_consumer',
                args: [self.props.order.backendId],
            }).then(function (final_consumer) {
                if (final_consumer) {
                    self.props.order.setFinalConsumer(final_consumer);
                }
            });

            await self.rpc({
                model: 'pos.order',
                method: 'fetch_nombre_comercial',
                args: [self.props.order.backendId],
            }).then(function (nombre_comercial) {
                if (nombre_comercial) {
                    self.props.order.setNombreComercial(nombre_comercial);
                }
            });

            await self.rpc({
                model: 'pos.order',
                method: 'fetch_whatsapp',
                args: [self.props.order.backendId],
            }).then(function (whatsapp) {
                if (whatsapp) {
                    self.props.order.setWhatsapp(whatsapp);
                }
            });

            await self.rpc({
                model: 'pos.order',
                method: 'fetch_gravado18',
                args: [self.props.order.backendId],
            }).then(function (gravado18) {
                if (gravado18) {
                    self.props.order.setGravado18(gravado18);
                }
            });

            await self.rpc({
                model: 'pos.order',
                method: 'fetch_impuesto18',
                args: [self.props.order.backendId],
            }).then(function (impuesto18) {
                if (impuesto18) {
                    self.props.order.setImpuesto18(impuesto18);
                }
            });

            self.showScreen('ReprintReceiptScreen', { order: self.props.order });
        }
    };

    Registries.Component.extend(ReprintReceiptButton, ReprintReceiptButtonInherit);

    return ReprintReceiptButton;
});
