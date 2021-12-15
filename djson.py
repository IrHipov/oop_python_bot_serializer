# -*- coding: utf-8 -*-

from document_object import *
import json


class DJson(DObject):
	def __init__(self, content, author):
		DObject.__init__(self, "JSON", content, author)

	def send_file(self):
		with open('file.json', 'w') as doc:
			doc.write(json.dumps(self.content, indent = 4))
		return open('file.json', 'rb')

	def file_to_object(file):
		with open('file.json', 'wb') as doc:
			doc.write(file)
		with open('file.json', 'r') as doc:
			return json.load(doc)
		return {}
