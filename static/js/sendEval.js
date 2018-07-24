function sendEval(){
  odoo.define('EvaluacionClientes.evaluacion', function(require) {
    "use strict";

      var base = require('web_editor.base');
      var ajax = require('web.ajax');
      var core = require('web.core');
      var _t = core._t;

      $('#sendEval').submit(function(event){
        event.preventDefault();

        var data = {};

        data[ 'encuesta' ] = window.location.pathname;

        for( var i = 0; i < 11; i++ ){
          data[ $($(event.target)[0][i]).attr('name') ] = $(event.target)[0][i].value;
        }

        //console.log($('#sendEval').serialize());

        ajax.jsonRpc("/updateEvaluacion", 'call', {
          'data': data
        }).then(function (data) {
          console.log(data);
        });
      });
  });
}
