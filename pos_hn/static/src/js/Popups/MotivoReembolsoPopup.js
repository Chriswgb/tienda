odoo.define('pos_hn.MotivoReembolsoPopup', function(require) {
	"use strict";

	const Registries = require('point_of_sale.Registries');
	const AbstractAwaitablePopup = require('point_of_sale.AbstractAwaitablePopup');
    const { _t } = require('web.core');



	class MotivoReembolsoPopup extends AbstractAwaitablePopup {
        // creo los estados y referencias de los attributos
        setup() {
            this.state = owl.hooks.useState({
                inputMotivo: '',
                inputHasError: false,
            });
            this.inputMotivo = owl.hooks.useRef('input-motivo');
        }
        
        // hago focus en el input al momento de montar la vista
        // para eso sirve la referencia de arriba
		mounted() {
            this.inputMotivo.el.focus();
        }

        // funcion del boton Aceptar
        // encargada de obtener los valores de los inputs, de mostrar errores en caso de ser
        // necesario y de hacer el action confirm
        getValue() {
            if (this.state.inputMotivo.trim() === ''){
                this.state.inputHasError = true;
                this.errorMessage = this.env._t('Debe escribir el motivo');
                return;
            }
            
            return super.confirm();
        }

        // esta funcion se dispara cuando se confirma el dialogo con el 'super.confirm()'
        // y se recibe el payload en donde se llama el dialogo
        getPayload() {
            return {
                motivo: this.state.inputMotivo.trim(),
            };
        }
	}

	MotivoReembolsoPopup.template = 'MotivoReembolsoPopup';
	MotivoReembolsoPopup.defaultProps = {
        confirmText: _t('Aceptar'),
        cancelText: _t('Cancelar'),
        title: '',
        body: '',
        list: [],
        startingValue: '',
    };

	Registries.Component.add(MotivoReembolsoPopup);

	return MotivoReembolsoPopup;
});