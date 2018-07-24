# -*- coding: utf-8 -*-
from odoo import http
from odoo import models
import sys

class EvaluacionClientes(http.Controller):
	@http.route('/evaluacion/<id>', type='http', auth='public', website=True)
	def index(self, id):
		http.request.env.cr.execute("SELECT status FROM evaluacion_model WHERE id = "+str(id))

		result = http.request.cr.fetchall()

		print(result[0][0]);

		if result[0][0] == True:
			return "Encuesta contestada"
		else:
			return http.request.render('EvaluacionClientes.evaluacion', {})

	@http.route(['/updateEvaluacion'], type='json', auth="public", website=True)
	def updateEvaluacion(self,  **vars):
		print (vars['data'])

		MealType = http.request.env['encuesta.model']

		print (vars['data']['consideraciones'])

		save = MealType.create({ 
				'tiempoLlegada' : vars['data']['tiempoLlegada'],
				'atencionTecnico' : vars['data']['atencion'],
				'arregloTecnico' : vars['data']['arreglo'],
				'cuidadoTecnico' : vars['data']['cuidado'],
				'refacciones' : vars['data']['consideraciones'],
				'whyRefacciones' : vars['data']['consideracionesPorque'],
				'herramientas' : vars['data']['herramientas'],
				'whyherramientas' : vars['data']['herramientasPorque'],
				'volver' : vars['data']['volver'],
				'whyvolver' : vars['data']['volverPorque'],
				'observaciones' : vars['data']['observaciones'],
			})

		http.request.env.cr.execute("SELECT MAX(id) FROM encuesta_model")

		result = http.request.cr.fetchall()

		print (result)

		http.request.env.cr.execute("UPDATE evaluacion_model SET status = 'True', encuesta_id= "+str(result[0][0])+" WHERE id = "+str(vars['data']['encuesta'].split("/")[2])+";")


		return {
			'message': 'Formulario guardado',
			'status': '200',
		}

	@http.route(['/saveEvaluacion'], type='json', auth="public", website=True)
	def save(self,  **vars):
		data = {}
		print (sys.path)

		MealType = http.request.env['evaluacion.model']
		
		'''save = MealType.create({ 
				'tiempoLlegada' : '',
				'atencionTecnico' : '',
				'arregloTecnico' : '',
				'cuidadoTecnico' : '',
				'refacciones' : '',
				'whyRefacciones' : '',
				'herramientas' : '',
				'whyherramientas' : '',
				'volver' : '',
				'whyvolver' : '',
				'observaciones' : '', 
			})

		print (save)'''

		print (vars)

		reference = vars['data']['pedido'].split(" ")

		print(reference)

		print(reference[len(reference)-1])

		http.request.env.cr.execute("SELECT id, partner_id, user_id FROM pos_order WHERE pos_reference LIKE '%"+reference[len(reference)-1]+"'")

		result = http.request.cr.fetchall()

		print(result[0][0])

		save = MealType.create({ 
				'cliente_id' : result[0][1],
				'socio_id' : result[0][2],
				'puntoVenta_id' : result[0][0]
			})

		last_id = save and max(save)

		print(last_id)


		print('idCliente'+str(result[0][1]));


		http.request.env.cr.execute("SELECT email FROM res_partner WHERE id = "+str(result[0][1]) )

		result = http.request.cr.fetchall()

		print('correo: '+str(result[0][0]))

		import os
		import smtplib
		from email.mime.multipart import MIMEMultipart
		from email.mime.text import MIMEText
		from email.mime.base import MIMEBase
		from email import encoders

		fromaddr = "wwwmario1515@gmail.com"
		toaddr = result[0][0]
		msg = MIMEMultipart('alternative')
		
		msg['From'] = fromaddr
		msg['To'] = toaddr
		msg['Subject'] = "MrPlumber"


		http.request.env.cr.execute("SELECT MAX(id) FROM evaluacion_model")

		result = http.request.cr.fetchall()

		print('ultimo id')

		print(result[0][0])
		
		body = """\
				<html>
				  <head><style type="text/css">.pos-sale-ticket {text-align: left;width: 300px;background-color: white;margin: 20px; padding: 15px;font-size: 14px;padding-bottom: 30px;display: inline-block;font-family: "Inconsolata";border: solid 1px rgb(220,220,220);border-radius: 3px;overflow: hidden;} .btn="-moz-box-shadow: 0px 10px 14px -7px #276873;-webkit-box-shadow: 0px 10px 14px -7px #276873;box-shadow: 0px 10px 14px -7px #276873;background:-webkit-gradient(linear, left top, left bottom, color-stop(0.05, #599bb3), color-stop(1, #408c99));background:-moz-linear-gradient(top, #599bb3 5%, #408c99 100%);background:-webkit-linear-gradient(top, #599bb3 5%, #408c99 100%);background:-o-linear-gradient(top, #599bb3 5%, #408c99 100%);background:-ms-linear-gradient(top, #599bb3 5%, #408c99 100%);background:linear-gradient(to bottom, #599bb3 5%, #408c99 100%);filter:progid:DXImageTransform.Microsoft.gradient(startColorstr="#599bb3", endColorstr="#408c99",GradientType=0);background-color:#599bb3;-moz-border-radius:8px;-webkit-border-radius:8px;border-radius:8px;display:inline-block;cursor:pointer;color:#ffffff;font-family:Arial;font-size:20px;font-weight:bold;padding:13px 32px;text-decoration:none;text-shadow:0px 1px 0px #3d768a;"</style></head>
				  <body>
				    """+vars['data']['ticket']+"""\
				    <a href='"""+http.request.env['ir.config_parameter'].sudo().get_param('web.base.url')+"""/evaluacion/"""+str(result[0][0])+"""'><center><div class="btn">Contestar encuesta</div></center></a>
				  </body>
				</html>
				"""

		
		msg.attach(MIMEText(body, 'html'))
		
		text = msg.as_string()

		server = smtplib.SMTP('smtp.gmail.com', 587)
		server.starttls()
		server.login(fromaddr, "36602317m")
		server.sendmail(fromaddr, toaddr, text)

		'''http.request.env.cr.execute("UPDATE evaluacion_model SET status='False' WHERE id="+id)

		http.request.env.cr.execute("SELECT id, cliente_id, socio_id, encuesta_id, status FROM evaluacion_model")

		print (http.request.cr.fetchall())'''

		return {
			'message': 'Formulario guardado',
			'status': '200',
		}