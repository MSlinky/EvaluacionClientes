odoo.define('EvaluacionClientes.form', function(require) {
	"use strict";
	console.log(7465564856686573);

	setTimeout(function(){
		$('.o_main_content').ready(function(){
			$('html').on('click', '.receipt-screen.screen .button.next.highlight', function(){

		        var base = require('web_editor.base');
				var ajax = require('web.ajax');
				var core = require('web.core');
				var _t = core._t;

				
				var data = {
					ticket : $('.pos-receipt-container').html(),
					pedido : $('.pos-sale-ticket').find('.pos-center-align').html()
				};

				setTimeout(function(){

					console.log(data);

					ajax.jsonRpc("/saveEvaluacion", 'call', {
						'data': data
					}).then(function (data) {
						console.log(data);
					});

					console.log($('.pos-sale-ticket').html());
		      	}, 5000);
			});
		})
	}, 5000);

});
	
	
//});
