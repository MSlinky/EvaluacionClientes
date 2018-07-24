from odoo import models, fields

class EncuestaClientes(models.Model):
	_name = 'encuesta.model'

	tiempoLlegada = fields.Selection([('excelente','Excelente'),('bueno','Bueno'), ('regular','Regular'), ('malo','Malo')],'El tiempo de arribo fué: ')
	atencionTecnico = fields.Selection([('excelente','Excelente'),('bueno','Bueno'), ('regular','Regular'), ('malo','Malo')],'La atención del técnico fué: ')
	arregloTecnico = fields.Selection([('excelente','Excelente'),('bueno','Bueno'), ('regular','Regular'), ('malo','Malo')],'El arreglo del técnico fué: ')
	cuidadoTecnico = fields.Selection([('excelente','Excelente'),('bueno','Bueno'), ('regular','Regular'), ('malo','Malo')],'El cuidado con el que se realizo el servicio fué: ')

	refacciones = fields.Selection([('excelente','Excelente'),('bueno','Bueno'), ('regular','Regular'), ('malo','Malo')],'Considera que las refacciones y materiales utilizados son: ')
	whyRefacciones = fields.Text('¿Porque?')

	herramientas = fields.Selection([('si','Si'),('no','No')],'Considera que el técnico contaba con las herramientas necesarias: ')
	whyherramientas = fields.Text('¿Porque?')

	volver = fields.Selection([('si','Si'),('no','No')],'De llegar a requerir un servicio semejante a este, volvería a llamarnos: ')
	whyvolver = fields.Text('¿Porque?')

	observaciones = fields.Text('Observaciones y/o comentarios')

class EvaluacionClientes(models.Model):
	_name = 'evaluacion.model'

	cliente_id = fields.Many2one('res.partner', string="Cliente", required=True)
	socio_id = fields.Many2one('res.users', string="Socio", required=True)
	puntoVenta_id = fields.Many2one('pos.order', string="Venta", required=True)
	encuesta_id = fields.Many2one('encuesta.model', string="Encuesta", required=False)
	status = fields.Boolean('Finalizada', required=False)