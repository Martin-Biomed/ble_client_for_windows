
# We use a Get/Set approach for the result str due to how the Python namespaces between the GUI and func files are set up
class Result_String(object):

	def __init__(self):
		self.updated_result_str = ""

	def set_result_str(self, result_str: str):
		self.updated_result_str = result_str

	def get_result_str(self):
		return self.updated_result_str
