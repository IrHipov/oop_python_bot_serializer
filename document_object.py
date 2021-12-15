# -*- coding: utf-8 -*-

class DObject:
	# dtype (string) - document type
	# content (turple) - document content 
	#{
	#	PublishDate: Date
	#	ContentLen: Int
	#	ArticlesCount: Int  
	#}
	# author (string) - document creator
	def __init__(self, dtype, content, author):
		self.type = dtype
		self.content = content
		self.author = author

	def get_doc_info(self):
		return "Document type: {}, content:\n" \
				"PublishDate: {}; ContentLen: {}; ArticlesCount: {};\n" \
				"author: {}".format(self.type, 
										self.content['PublishDate'],
										self.content['ContentLen'], 
										self.content['ArticlesCount'],
										self.author)

	
	def send_file(self, message):
		pass
