from document_object import *
import json

class DJson(DObject):
	json_content = ""

	def __init__(self, strContent, author):
		DObject.__init__(self, "JSON", self.from_string(strContent), author)
		json_content = strContent


	def from_string(self, strContent):
		return json.loads(strContent, object_hook=DObject.as_dobject_content)

	
