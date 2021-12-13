import telebot
import config
import requests
import json
from djson import *
from dcsv import *

from telebot import types

bot = telebot.TeleBot(config.TOKEN)

# Constants
COMMANDS = [
	"JsonFileToObj",
	"JsonObjToFile",
	"CsvFileToObj",
	"CsvObjToFile"
]


# On Start
@bot.message_handler(commands=['start'])
def welcome(message):
	global markup
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

	markup.add(types.KeyboardButton(COMMANDS[0]),
				types.KeyboardButton(COMMANDS[1]),
				types.KeyboardButton(COMMANDS[2]),
				types.KeyboardButton(COMMANDS[3]))


	bot.send_message(message.chat.id, "Hi, choose what I will be do", 
						reply_markup=markup)


@bot.message_handler(func=lambda m: m.text == COMMANDS[0])
def json_file_to_obj(message):
	send = bot.send_message(message.chat.id, "OK. Send me JSON file",
							reply_markup=types.ReplyKeyboardRemove())
	bot.register_next_step_handler(send, get_json_file)


@bot.message_handler(func=lambda m: m.text == COMMANDS[1])
def json_obj_to_file(message):
	send = bot.send_message(message.chat.id, 
							'Enter: \n\
							\tPublish Date\n\
							\tContent Length\n\
							\tArticles Count\n',
							reply_markup=types.ReplyKeyboardRemove())
	bot.register_next_step_handler(send, gen_json_object)


@bot.message_handler(func=lambda m: m.text == COMMANDS[2])
def csv_file_to_obj(message):
	send = bot.send_message(message.chat.id, "OK. Send me CSV file",
							reply_markup=types.ReplyKeyboardRemove())
	bot.register_next_step_handler(send, get_csv_file)


@bot.message_handler(func=lambda m: m.text == COMMANDS[3])
def csv_obj_to_file(message):
	send = bot.send_message(message.chat.id, 
							'Enter: \n\
							\tPublish Date\n\
							\tContent Length\n\
							\tArticles Count\n',
							reply_markup=types.ReplyKeyboardRemove())
	bot.register_next_step_handler(send, gen_csv_object)




def gen_json_object(message):
	split_array = message.text.split('\n')
	obj = {
		'PublishDate': split_array[0],
		'ContentLen': int(split_array[1]),
		'ArticlesCount': int(split_array[2])
	}
	
	gen_file(message, DJson(obj, message.from_user.username))


def gen_csv_object(message):
	split_array = message.text.split('\n')
	obj = {
		'PublishDate': split_array[0],
		'ContentLen': int(split_array[1]),
		'ArticlesCount': int(split_array[2])
	}
	
	gen_file(message, DCsv(obj, message.from_user.username))


def gen_file(message, obj):
	global markup
	
	if isinstance(obj, DJson):
		bot.send_message(message.chat.id, "JSON object serlialized to file.json:")
	elif isinstance(obj, DCsv):
		bot.send_message(message.chat.id, "CSV object serlialized to file.csv:")
	
	bot.send_document(message.chat.id, obj.send_file(),
						reply_markup=markup)


def get_json_file(message):
	global markup

	file_info = bot.get_file(message.document.file_id)
	downloaded_file = bot.download_file(file_info.file_path)

	djson = DJson(DJson.file_to_object(downloaded_file), message.from_user.username)
	bot.send_message(message.chat.id, "File success deserialized:")
	bot.send_message(message.chat.id, djson.get_doc_info(),
						reply_markup=markup)


def get_csv_file(message):
	global markup

	file_info = bot.get_file(message.document.file_id)
	downloaded_file = bot.download_file(file_info.file_path)

	dcsv = DCsv(DCsv.file_to_object(downloaded_file), message.from_user.username)
	bot.send_message(message.chat.id, "File success deserialized:")
	bot.send_message(message.chat.id, dcsv.get_doc_info(),
						reply_markup=markup)
	




# Bot start
bot.polling(none_stop=True)



# EMPTY_OBJECT = {
# 	'PublishDate': None,
#  	'ContentLen': None,
#  	'ArticlesCount': None
# }

# TEST_STR_OBJECT = '{"PublishDate": "01.12.2021","ContentLen": 10002,"ArticlesCount": 8}'

# # On User send message
# @bot.message_handler(content_types=['text'])
# def on_message(message):
# 	global bot_state
# 	global markup

# 	if message.chat.type == 'private':
# 		command = message.text

# 		if bot_state == 'None':
# 			bot_state = command 

# 			if command == BUTTON_NAME_JSON_TO_OBJ or command == BUTTON_NAME_CSV_TO_OBJ:
# 				bot.send_message(message.chat.id, "Send me string from file", 
# 									reply_markup=types.ReplyKeyboardRemove())
# 			elif command == BUTTON_NAME_JSON_FROM_OBJ or command == BUTTON_NAME_CSV_FROM_OBJ:
# 				send = bot.send_message(message.chat.id, "Ok. Let's go to create Object", 
# 									reply_markup=types.ReplyKeyboardRemove())

# 				if command == BUTTON_NAME_JSON_FROM_OBJ:
# 					next_task = json_from_object(message)
# 				else:
# 					next_task = csv_from_object(message)
				
# 				bot.register_next_step_handler(send, next_task)
# 			else:
# 				bot.send_message(message.chat.id, "Unknown command 😢")
# 				bot_state = 'None'
# 			return
# 		elif bot_state == BUTTON_NAME_JSON_TO_OBJ:
# 			json_to_object(message)
# 		elif bot_state == BUTTON_NAME_CSV_TO_OBJ:
# 			csv_to_object(message)

# 		bot.send_message(message.chat.id, "OK. Go to start", reply_markup=markup)
# 		bot_state = 'None'


# # Functions 
# def json_to_object(message):
# 	djson = DJson(message.text, message.from_user.username)

# 	bot.send_message(message.chat.id, "JSON object created:\n")
# 	bot.send_message(message.chat.id, djson.get_doc_info())

# def json_from_object(message):
# 	get_object(message)

# def csv_to_object(message):
# 	bot.send_message(message.chat.id, "55")

# def csv_from_object(message):
# 	bot.send_message(message.chat.id, "66")

# def get_object(message):
# 	global obj
# 	obj = EMPTY_OBJECT

# 	send = bot.send_message(message.chat.id, 'Enter Publish Date')
# 	bot.register_next_step_handler(send, set_publish_date)

# def set_publish_date(message):
# 	global obj
# 	obj['PublishDate'] = message.text
	
# 	send = bot.send_message(message.chat.id, 'Enter Content Length')
# 	bot.register_next_step_handler(send, set_content_len)
	
# def set_content_len(message):
# 	global obj
# 	obj['ContentLen'] = message.text

# 	send = bot.send_message(message.chat.id, 'Enter Articles Count number')
# 	bot.register_next_step_handler(send, set_articles_count)

# def set_articles_count(message): 
# 	global obj
# 	obj['ArticlesCount'] = message.text

# 	send = bot.send_message(message.chat.id, 'OK')
# 	print(obj)

# # Bot start
# bot.polling(none_stop=True)