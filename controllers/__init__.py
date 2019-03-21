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

		if ('tiempoLlegada' in vars['data']):
			tiempoLlegada = vars['data']['tiempoLlegada']
		else :
			tiempoLlegada = ''

		if ('atencion' in vars['data']):
			atencion = vars['data']['atencion']
		else :
			atencion = ''

		if ('arreglo' in vars['data']):
			arreglo = vars['data']['arreglo']
		else :
			arreglo = ''

		if ('cuidado' in vars['data']):
			cuidado = vars['data']['cuidado']
		else :
			cuidado = ''

		if ('consideraciones' in vars['data']):
			consideraciones = vars['data']['consideraciones']
		else :
			consideraciones = ''

		if ('consideracionesPorque' in vars['data']):
			consideracionesPorque = vars['data']['consideracionesPorque']
		else :
			consideracionesPorque = ''

		if ('herramientas' in vars['data']):
			herramientas = vars['data']['herramientas']
		else :
			herramientas = ''

		if ('herramientasPorque' in vars['data']):
			herramientasPorque = vars['data']['herramientasPorque']
		else :
			herramientasPorque = ''

		if ('volver' in vars['data']):
			volver = vars['data']['volver']
		else :
			volver = ''

		if ('volverPorque' in vars['data']):
			volverPorque = vars['data']['volverPorque']
		else :
			volverPorque = ''

		if ('observaciones' in vars['data']):
			observaciones = vars['data']['observaciones']
		else :
			observaciones = ''
		
		if ('estrellas' in vars['data']):
			estrellas = vars['data']['estrellas']
		else :
			estrellas = ''

		save = MealType.create({ 
			'tiempoLlegada' : tiempoLlegada,
			'atencionTecnico' : atencion,
			'arregloTecnico' : arreglo,
			'cuidadoTecnico' : cuidado,
			'refacciones' : consideraciones,
			'whyRefacciones' : consideracionesPorque,
			'herramientas' : herramientas,
			'whyherramientas' : herramientasPorque,
			'volver' : volver,
			'whyvolver' : volverPorque,
			'observaciones' : observaciones,
			'estrellas' : estrellas,
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

		reference = vars['data']['pedido'].split(" ")

		http.request.env.cr.execute("SELECT id, partner_id, user_id FROM pos_order WHERE pos_reference LIKE '%"+reference[len(reference)-1]+"'")

		result = http.request.cr.fetchall()

		save = MealType.create({ 
				'cliente_id' : result[0][1],
				'socio_id' : result[0][2],
				'puntoVenta_id' : result[0][0]
			})

		last_id = save and max(save)

		http.request.env.cr.execute("SELECT email FROM res_partner WHERE id = "+str(result[0][1]) )

		result = http.request.cr.fetchall()

		import os
		import smtplib
		from email.mime.multipart import MIMEMultipart
		from email.mime.text import MIMEText
		from email.mime.image import MIMEImage
	
		path = os.path.join(os.path.dirname(os.path.abspath(__file__)))

		print(path)

		fromaddr = "wwwmario1515@gmail.com"
		toaddr = result[0][0]
		msg = MIMEMultipart('alternative')
		
		msg['From'] = fromaddr
		msg['To'] = toaddr
		msg['Subject'] = "MrPlumber"

		http.request.env.cr.execute("SELECT MAX(id) FROM evaluacion_model")

		result = http.request.cr.fetchall()

		body = """\
				<html>
				  <head></head>
				  <body>
				    <a style="text-decoration: none;" href='"""+http.request.env['ir.config_parameter'].sudo().get_param('web.base.url')+"""/evaluacion/"""+str(result[0][0])+"""'><center><div class="btn" style="background-color: #e66231;color: white;font-size: 3em;font-weight: bold;    -webkit-box-shadow: 0 16px 24px 2px rgba(0,0,0,0.14), 0 6px 30px 5px rgba(0,0,0,0.12), 0 8px 10px -7px rgba(0,0,0,0.2);box-shadow: 0 16px 24px 2px rgba(0,0,0,0.14), 0 6px 30px 5px rgba(0,0,0,0.12), 0 8px 10px -7px rgba(0,0,0,0.2)">Contestar encuesta</div></center></a>
				  </body>
				</html>
				"""

		import base64
		aaa = bytes(vars['data']['canvas'].split(',')[1], 'utf-8')
		with open(path+"/tickets/"+reference[len(reference)-1]+".png", "wb") as fh:
			fh.write(base64.decodebytes(aaa))

		fp = open(path+"/tickets/"+reference[len(reference)-1]+".png", 'rb')                                                    
		img = MIMEImage(fp.read())
		fp.close()
		msg.add_header('Content-Disposition', 'attachment', filename=reference[len(reference)-1]+'.png')
		msg.attach(img)

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