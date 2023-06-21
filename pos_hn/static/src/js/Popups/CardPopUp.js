odoo.define('pos_card_information.CardPopup', function(require) {
	"use strict";

	var core = require('web.core');
	const { useState, useRef } = owl.hooks;
	const { useListener } = require('web.custom_hooks');
	const PosComponent = require('point_of_sale.PosComponent');
	const Registries = require('point_of_sale.Registries');
	const AbstractAwaitablePopup = require('point_of_sale.AbstractAwaitablePopup');
	var QWeb = core.qweb;

	var _t = core._t;

	class CardInformationPopup extends AbstractAwaitablePopup {
		constructor() {
			super(...arguments);
			this.inputCardNumberRef = useRef('input-card_number');
			this.inputExpirationDateRef = useRef('input-expiration_date');
			this.inputSecurityCodeRef = useRef('input-security_code');
			
		}
		mounted() {
            this.inputCardNumberRef.el.focus();
        }

        getValue() {
        	var order = this.env.pos.get_order()
			order.set_card_number(this.inputCardNumberRef.el.value);
			order.set_expiration_date(this.inputExpirationDateRef.el.value);
			order.set_security_code(this.inputSecurityCodeRef.el.value);
			this.trigger('close-popup');
        }
        cancel() {
        	this.trigger('close-popup');
        }
	}

	CardInformationPopup.template = 'CardInformationPopup';
	CardInformationPopup.defaultProps = {
        confirmText: 'Ok',
        cancelText: 'Cancel',
        title: '',
        body: '',
        list: [],
        startingValue: '',
    };

	Registries.Component.add(CardInformationPopup);

	return CardInformationPopup;
});