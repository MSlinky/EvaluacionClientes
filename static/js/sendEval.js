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

        for( var i = 0; i < 15; i++ ){
          if($(event.target)[0][i].type === 'radio'){
            if($(event.target)[0][i].checked){
              data[ $($(event.target)[0][i]).attr('name') ] = $(event.target)[0][i].value;
            }
          }else {
            data[ $($(event.target)[0][i]).attr('name') ] = $(event.target)[0][i].value;
          }
        }

        console.log(data)

        //console.log($('#sendEval').serialize());

        ajax.jsonRpc("/updateEvaluacion", 'call', {
          'data': data
        }).then(function (data) {
          console.log(data)
          if (data.status === "200") {
            //location.href ="https://www.mrplumber.com.mx/";
          }
        });
      });
  });
}
