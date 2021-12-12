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

	def as_dobject_content(dct):
		publish_date = ""
		content_len = 0
		articles_count = 0

		if 'PublishDate' in dct:
			publish_date = dct['PublishDate']
		if 'ContentLen' in dct:
			publish_date = dct['ContentLen']
		if 'ArticlesCount' in dct:
			publish_date = dct['ArticlesCount']

		return {
				'PublishDate': publish_date, 
				'ContentLen': content_len, 
				'ArticlesCount': articles_count
				}