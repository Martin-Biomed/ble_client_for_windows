
# We use a GET/SET approach for the result str due to how the Python namespaces between the GUI and func files are set up
# To use the GET/SET approach for the result string, it was necessary to create an additional object.
class Result_String(object):

	def __init__(self):
		self.updated_result_str = ""

	def set_result_str(self, result_str: str):
		self.updated_result_str = result_str

	def get_result_str(self):
		return self.updated_result_str
