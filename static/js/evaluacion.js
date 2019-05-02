odoo.define('EvaluacionClientes.form', function(require) {
	"use strict";

	$('body').ready(function(){
		$('body').append('<div id="ex1" class="modal" style="max-width: 100%;"><canvas id="sign" class="pad"></canvas><div class="clear" style="background: #6EC89B !important;border: solid 1px #64AF8A !important;color: white !important;padding: 0px;width: 100%;display: inline-block;text-align: center;font-size: 50px;">Clear</div></div><div style="display:hidden" id="ticket-hidden"></div>');
	});

	setTimeout(function(){
		$('.paymentlines').ready(function(){
			$('.receipt-screen .screen-content .top-content').append('<a style="color: white;" href="#ex1" rel="modal:open"><span class="button highlight" style="right: 0;width: 180px;top: 70PX;">Encuesta</span></a>');
		});
	}, 60000);

	setTimeout(function(){
		$('.o_main_content').ready(function(){

			$('body').append('<div id="div-carga" style="position: fixed;width: 100%;height: 100vh;background-color: #000000c9;z-index: 9;left: 0;top: 0;text-align: center;color: white;padding-top: 30vh;">Cargando</div>');
				html2canvas(document.querySelector('.pos-sale-ticket')).then(function(canvas) {
					$("#ticket-canvas-hidden").remove();
					canvas.id = 'ticket-canvas-hidden';
					$('#ticket-hidden').append(canvas);
					$('#div-carga').remove();
				});

			$('body').append('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/jquery-modal/0.9.1/jquery.modal.min.css" /><script src="https://cdnjs.cloudflare.com/ajax/libs/jquery-modal/0.9.1/jquery.modal.min.js"></script>');

			var $canvas,
        onResize = function(event) {
          $canvas.attr({
            height: window.innerHeight - 130,
            width: window.innerWidth - 240
          });
        };

			$(document).ready(function() {
				$canvas = $('canvas');
				window.addEventListener('orientationchange', onResize, false);
				window.addEventListener('resize', onResize, false);
				onResize();

				$('.modal').signaturePad({
					drawOnly: true,
					defaultAction: 'drawIt',
					validateFields: false,
					lineWidth: 0,
					output: null,
					sigNav: null,
					name: null,
					typed: null,
					clear: '.clear',
					typeIt: null,
					drawIt: null,
					typeItDesc: null,
					drawItDesc: null,
					onDrawEnd: function () {
						var canvas = document.getElementById("sign");
						var img    = canvas.toDataURL("image/png");
						$("#content-firma").remove();
						$('.pos-sale-ticket').append('<div id="content-firma"><img id="imgSign" style="width: 100%;" src="'+img+'"/><div style="text-align: center;border-top: solid black 1px;">Firma</div></div>');

						$('body').append('<div id="div-carga" style="position: fixed;width: 100%;height: 100vh;background-color: #000000c9;z-index: 9;left: 0;top: 0;text-align: center;color: white;padding-top: 30vh;">Cargando</div>');
						html2canvas(document.querySelector('.pos-sale-ticket')).then(function(canvas) {
							$("#ticket-canvas-hidden").remove();
							canvas.id = 'ticket-canvas-hidden';
							$('#ticket-hidden').append(canvas);
							$('#div-carga').remove();
						});
					}
				});
			});

			$('html').on('click', '.receipt-screen.screen .button.next.highlight', function(){

		    var base = require('web_editor.base');
				var ajax = require('web.ajax');
				var core = require('web.core');
				var _t = core._t;

				
				var data = {
					ticket : $('.pos-receipt-container').html(),
					pedido : $('.pos-sale-ticket').find('.pos-center-align').html(),
					canvas : document.getElementById("ticket-canvas-hidden").toDataURL("image/png")
				};

				setTimeout(function(){

					ajax.jsonRpc("/saveEvaluacion", 'call', {
						'data': data
					}).then(function (data) {
						console.log(data);
					});

				}, 5000);
				
			});
		})
	}, 5000);

});
