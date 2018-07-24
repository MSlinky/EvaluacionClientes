from odoo import models

class AModel(models.Model):
	_name = 'evaluacion.model'

	def __init__(self):
		print( '--- modelo ---' )

	def a_method(self):
		# self can be anywhere between 0 records and all records in the
		# database
		self.do_operation()

	def do_operation(self):
		print (self) # => a.model(1, 2, 3, 4, 5)
		for record in self:
			print (record) # => a.model(1), then a.model(2), then a.model(3), ...

	def get_all_meal_types(self):
        return self.search([])