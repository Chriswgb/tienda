odoo.define('.PaymentScreenWidget', function(require){
	'use strict';

	const PaymentScreen = require('point_of_sale.PaymentScreen');
	const PosComponent = require('point_of_sale.PosComponent');
	const Registries = require('point_of_sale.Registries');
	const { useListener } = require('web.custom_hooks');
    var models = require('point_of_sale.models');

	models.load_models({
		model:  'pos.payment.method',
		fields: ['name', 'is_cash_count', 'use_payment_terminal', 'card_information', 'cheque_information'],
		domain: function(self, tmp) {
			return [['id', 'in', tmp.payment_method_ids]];
		},
		loaded: function(self, payment_methods) {
			self.payment_methods = payment_methods.sort(function(a,b){
				// prefer cash payment_method to be first in the list
				if (a.is_cash_count && !b.is_cash_count) {
					return -1;
				} else if (!a.is_cash_count && b.is_cash_count) {
					return 1;
				} else {
					return a.id - b.id;
				}
			});
			self.payment_methods_by_id = {};
			_.each(self.payment_methods, function(payment_method) {
				self.payment_methods_by_id[payment_method.id] = payment_method;

				var PaymentInterface = self.electronic_payment_interfaces[payment_method.use_payment_terminal];
				if (PaymentInterface) {
					payment_method.payment_terminal = new PaymentInterface(self, payment_method);
				}
			});
		}
	});

	var posorder_super = models.Order.prototype;
	models.Order = models.Order.extend({
		initialize: function(attr, options) {
			posorder_super.initialize.apply(this,arguments);
			this.card_number = this.card_number || false;
			this.expiration_date = this.expiration_date || false;
			this.security_code = this.security_code || false;
			this.cheque_number = this.cheque_number || false;
			this.note = this.note || false;
		},

		export_as_JSON: function() {
			var json = posorder_super.export_as_JSON.apply(this,arguments);
			json.card_number = this.card_number;
			json.expiration_date = this.expiration_date;
			json.security_code = this.security_code;
			json.cheque_number = this.cheque_number;
			json.note = this.note;

			return json;
		},
		init_from_JSON: function(json) {
			posorder_super.init_from_JSON.apply(this,arguments);
			this.card_number = json.card_number;
			this.expiration_date = json.expiration_date;
			this.security_code = json.security_code;
			this.cheque_number = json.cheque_number;
			this.note = json.note;
		},

		get_card_number: function() {
			return this.card_number
		},
		set_card_number:function(card_number) {
			this.card_number = card_number;
			this.trigger('change');
		},

		get_expiration_date:function() {
			return this.expiration_date
		},
		set_expiration_date:function(expiration_date) {
			this.expiration_date = expiration_date
			this.trigger('change');
		},

		get_security_code:function() {
			return this.security_code
		},
		set_security_code:function(security_code) {
			this.security_code = security_code
			this.trigger('change');
		},

		get_cheque_number: function() {
			return this.cheque_number
		},
		set_cheque_number:function(cheque_number) {
			this.cheque_number = cheque_number;
			this.trigger('change');
		},
		get_note: function() {
			return this.note
		},
		set_note:function(note) {
			this.note = note;
			this.trigger('change');
		},
		export_for_printing: function () {
            var result = posorder_super.export_for_printing.apply(this, arguments);
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


	const PaymentScreenWidget = (PaymentScreen) =>
		class extends PaymentScreen {
			constructor() {
				super(...arguments);
                useListener('card-info', this.cardInfo);
				useListener('cheque-info', this.chequeInfo);
			}

            async cardInfo(event) {
                var self = this;
                const { cid } = event.detail;
                const line = this.paymentLines.find((line) => line.cid === cid);
                await this.showPopup('CardInformationPopup', {
					body: 'Tarjeta',
					startingValue: self,
					list: self.env.pos.bank,
                    title: this.env._t('Información de tarjeta'),
                });

            }

			async chequeInfo(event) {
                var self = this;
                const { cid } = event.detail;
                const line = this.paymentLines.find((line) => line.cid === cid);
                await this.showPopup('ChequeInformationPopup', {
					body: 'Cheque',
					startingValue: self,
					list: self.env.pos.bank,
                    title: this.env._t('Información de cheque'),
                });

            }

			// funcion sobre escrita de la clase original
			async validateOrder(isForceValidate) {

				if(this.env.pos.config.cash_rounding) {
					if(!this.env.pos.get_order().check_paymentlines_rounding()) {
						this.showPopup('ErrorPopup', {
							title: this.env._t('Rounding error in payment lines'),
							body: this.env._t("The amount of your payment lines must be rounded to validate the transaction."),
						});
						return;
					}
				}
				if (await this._isOrderValid(isForceValidate)) {
					// remove pending payments before finalizing the validation
					for (let line of this.paymentLines) {
						if (!line.is_done()) this.currentOrder.remove_paymentline(line);
					}

					
					/*si la orden es valida mando a traer el total a pagar y si es negativo,
					tomo como que es un reembolso, entonces pido el motivo de reembolso por medio 
					de un Popup y asigno el valor que me devuelve en el payload al atributo note,
					para posteriormente en el  metodo "_finalizeValidation()" pueda enviar ese atributo 
					en las props y guardarlo en la base de datos y poderlo mostrar en el recibo de cobro*/

					const total_paid =	this.currentOrder.get_total_with_tax() + this.currentOrder.get_rounding_applied()
				
					if (total_paid < 0){
						const { confirmed, payload } = await this.showPopup('MotivoReembolsoPopup');
						
						if (confirmed){

							this.currentOrder.set_note(payload.motivo)
							await this._finalizeValidation();

						}

					}
					// si la orden no es una devolucion se sigue el funcionamiento normal
					else {
						await this._finalizeValidation();
					}
					
				}
			}

			// funcion sobre escrita de la clase original
			async _finalizeValidation() {
                console.log(this.currentOrder)
                var self = this;
                if (this.currentOrder.is_paid_with_cash() && this.env.pos.config.iface_cashdrawer) {
                    this.env.pos.proxy.printer.open_cashbox();
                }

                this.currentOrder.initialize_validation_date();
                this.currentOrder.finalized = true;

                let syncedOrderBackendIds = [];

                try {
                    if (this.currentOrder.is_to_invoice()) {
                        syncedOrderBackendIds = await this.env.pos.push_and_invoice_order(
                            this.currentOrder
                        );
                    } else {
                        syncedOrderBackendIds = await this.env.pos.push_single_order(this.currentOrder);
                    }
                } catch (error) {
                    if (error instanceof Error) {
                        throw error;
                    } else {
                        await this._handlePushOrderError(error);
                    }
                }

                if (syncedOrderBackendIds.length && this.currentOrder.wait_for_push_order()) {
                    const result = await this._postPushOrderResolve(
                        this.currentOrder,
                        syncedOrderBackendIds
                    );
                    if (!result) {
                        await this.showPopup('ErrorPopup', {
                            title: 'Error: no internet connection.',
                            body: error,
                        });
                    }
                } else {
                    if (syncedOrderBackendIds && syncedOrderBackendIds.length && self.env.pos.config.print_invoice_no_receipt) {
                        await self.rpc({
                            model: 'pos.order',
                            method: 'fetch_invoice_number',
                            args: [syncedOrderBackendIds[0]],
                        }).then(function (invoice_number) {
                            if (invoice_number) {
                                self.currentOrder.setInvoiceNumber(invoice_number);
                            }
                        });

                        await self.rpc({
                            model: 'pos.order',
                            method: 'fetch_cai_number',
                            args: [syncedOrderBackendIds[0]],
                        }).then(function (cai_number) {
                            if (cai_number) {
                                self.currentOrder.setCaiNumber(cai_number);
                            }
                        });

                        await self.rpc({
                            model: 'pos.order',
                            method: 'fetch_expiration_cai',
                            args: [syncedOrderBackendIds[0]],
                        }).then(function (cai_expires_shot) {
                            if (cai_expires_shot) {
                                self.currentOrder.setCaiExpiresShot(cai_expires_shot);
                            }
                        });

                        await self.rpc({
                            model: 'pos.order',
                            method: 'fetch_min_cai',
                            args: [syncedOrderBackendIds[0]],
                        }).then(function (min_cai) {
                            if (min_cai) {
                                self.currentOrder.setMinCai(min_cai);
                            }
                        });

                        await self.rpc({
                            model: 'pos.order',
                            method: 'fetch_max_cai',
                            args: [syncedOrderBackendIds[0]],
                        }).then(function (max_cai) {
                            if (max_cai) {
                                self.currentOrder.setMaxCai(max_cai);
                            }
                        });

                        await self.rpc({
                            model: 'pos.order',
                            method: 'fetch_amount_untaxed',
                            args: [syncedOrderBackendIds[0]],
                        }).then(function (amount_untaxed) {
                            if (amount_untaxed) {
                                self.currentOrder.setAmountUntaxed(amount_untaxed);
                            }
                        });

                        await self.rpc({
                            model: 'pos.order',
                            method: 'fetch_amount_tax',
                            args: [syncedOrderBackendIds[0]],
                        }).then(function (amount_tax) {
                            if (amount_tax) {
                                self.currentOrder.setAmountTax(amount_tax);
                            }
                        });

                        await self.rpc({
                            model: 'pos.order',
                            method: 'fetch_amount_total_text',
                            args: [syncedOrderBackendIds[0]],
                        }).then(function (amount_total_text) {
                            if (amount_total_text) {
                                self.currentOrder.setAmountTotalText(amount_total_text);
                            }
                        });

                        await self.rpc({
                            model: 'pos.order',
                            method: 'fetch_excento',
                            args: [syncedOrderBackendIds[0]],
                        }).then(function (excento) {
                            if (excento) {
                                self.currentOrder.setExcento(excento);
                            }
                        });

                        await self.rpc({
                            model: 'pos.order',
                            method: 'fetch_exonerado',
                            args: [syncedOrderBackendIds[0]],
                        }).then(function (exonerado) {
                            if (exonerado) {
                                self.currentOrder.setExonerado(exonerado);
                            }
                        });

                        await self.rpc({
                            model: 'pos.order',
                            method: 'fetch_gravado',
                            args: [syncedOrderBackendIds[0]],
                        }).then(function (gravado) {
                            if (gravado) {
                                self.currentOrder.setGravado(gravado);
                            }
                        });

                        await self.rpc({
                            model: 'pos.order',
                            method: 'fetch_street',
                            args: [syncedOrderBackendIds[0]],
                        }).then(function (street) {
                            if (street) {
                                self.currentOrder.setStreet(street);
                            }
                        });

                        await self.rpc({
                            model: 'pos.order',
                            method: 'fetch_street2',
                            args: [syncedOrderBackendIds[0]],
                        }).then(function (street2) {
                            if (street2) {
                                self.currentOrder.setStreet2(street2);
                            }
                        });

                        await self.rpc({
                            model: 'pos.order',
                            method: 'fetch_city',
                            args: [syncedOrderBackendIds[0]],
                        }).then(function (city) {
                            if (city) {
                                self.currentOrder.setCity(city);
                            }
                        });

                        await self.rpc({
                            model: 'pos.order',
                            method: 'fetch_state_id',
                            args: [syncedOrderBackendIds[0]],
                        }).then(function (state_id) {
                            if (state_id) {
                                self.currentOrder.setStateId(state_id);
                            }
                        });

                        await self.rpc({
                            model: 'pos.order',
                            method: 'fetch_rtn',
                            args: [syncedOrderBackendIds[0]],
                        }).then(function (rtn) {
                            if (rtn) {
                                self.currentOrder.setRtn(rtn);
                            }
                        });

                        await self.rpc({
                            model: 'pos.order',
                            method: 'fetch_rtn2',
                            args: [syncedOrderBackendIds[0]],
                        }).then(function (rtn2) {
                            if (rtn2) {
                                self.currentOrder.setRtn2(rtn2);
                            }
                        });

                        await self.rpc({
                            model: 'pos.order',
                            method: 'fetch_nombre_comercial',
                            args: [syncedOrderBackendIds[0]],
                        }).then(function (nombre_comercial) {
                            if (nombre_comercial) {
                                self.currentOrder.setNombreComercial(nombre_comercial);
                            }
                        });

                        await self.rpc({
                            model: 'pos.order',
                            method: 'fetch_whatsapp',
                            args: [syncedOrderBackendIds[0]],
                        }).then(function (whatsapp) {
                            if (whatsapp) {
                                self.currentOrder.setWhatsapp(whatsapp);
                            }
                        });

                        await self.rpc({
                            model: 'pos.order',
                            method: 'fetch_gravado18',
                            args: [syncedOrderBackendIds[0]],
                        }).then(function (gravado18) {
                            if (gravado18) {
                                self.currentOrder.setGravado18(gravado18);
                            }
                        });

                        await self.rpc({
                            model: 'pos.order',
                            method: 'fetch_impuesto18',
                            args: [syncedOrderBackendIds[0]],
                        }).then(function (impuesto18) {
                            if (impuesto18) {
                                self.currentOrder.setImpuesto18(impuesto18);
                            }
                        });


                    }
                }
                this.showScreen(this.nextScreen);

                // If we succeeded in syncing the current order, and
                // there are still other orders that are left unsynced,
                // we ask the user if he is willing to wait and sync them.
                if (syncedOrderBackendIds.length && this.env.pos.db.get_orders().length) {
                    const { confirmed } = await this.showPopup('ConfirmPopup', {
                        title: this.env._t('Remaining unsynced orders'),
                        body: this.env._t(
                            'There are unsynced orders. Do you want to sync these orders?'
                        ),
                    });
                    if (confirmed) {
                        // NOTE: Not yet sure if this should be awaited or not.
                        // If awaited, some operations like changing screen
                        // might not work.
                        this.env.pos.push_orders();
                    }
                }
            }

	};

	Registries.Component.extend(PaymentScreen, PaymentScreenWidget);
	return PaymentScreen;

});
