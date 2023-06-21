odoo.define('point_of_sale.EstadoCajaButton', function(require) {
    'use strict';

    const PosComponent = require('point_of_sale.PosComponent');
    const ProductScreen = require('point_of_sale.ProductScreen');
    const { useListener } = require('web.custom_hooks');
    const Registries = require('point_of_sale.Registries');

    class EstadoCajaButton extends PosComponent {
        constructor() {
            super(...arguments);
            useListener('click', this.onClick);
        }
      
        async onClick() {
            try {
                
                // genero el reporte desde la funcion de python (obtener_datos) en el modelo pos.session
                await this.rpc({
                    model: 'pos.session',
                    method: 'obtener_datos',
                    args: [[this.env.pos.config.current_session_id[0]]],
                    context: this.env.session.user_context,
                });

                // luego imprimo el reporte pdf ya con los datos generedo en la funcion anterior
                await this.env.pos.do_action('point_of_sale_update_community.report_corte_caja_session2', {
                    additional_context: {
                        active_ids: [this.env.pos.config.current_session_id[0]],
                    },
                });

            // si ocurre un error devuelvo un mensaje al usuario
            } catch (error) {
                if (error instanceof Error) {
                    throw error;
                } else {
                    // NOTE: error here is most probably undefined
                    this.showPopup('ErrorPopup', {
                        title: this.env._t('Network Error'),
                        body: this.env._t('Unable to download invoice.'),
                    });
                }
            }
        }
    }
    EstadoCajaButton.template = 'EstadoCajaButton';

    ProductScreen.addControlButton({
        component: EstadoCajaButton,
        condition: () => true,
        position: ['after', 'ProductInfoButton'],
    });

    Registries.Component.add(EstadoCajaButton);

    return EstadoCajaButton;
});