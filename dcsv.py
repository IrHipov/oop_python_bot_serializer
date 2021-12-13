from document_object import *
import csv


class DCsv(DObject):
	def __init__(self, content, author):
		DObject.__init__(self, "JSON", content, author)

	def send_file(self):
		with open('file.csv', 'w', newline="") as doc:
			columns = ['PublishDate', 'ContentLen', 'ArticlesCount']
			writer = csv.DictWriter(doc, fieldnames=columns)
			writer.writeheader()
			writer.writerow(self.content)
		return open('file.csv', 'rb')

	def file_to_object(file):
		with open('file.csv', 'wb') as doc:
			doc.write(file)
		with open('file.csv', 'r', newline="") as doc:
			reader = csv.DictReader(doc)
			for row in reader:
				return {
					'PublishDate': row['PublishDate'],
					'ContentLen': row['ContentLen'],
					'ArticlesCount': row['ArticlesCount']
				}
		return {}