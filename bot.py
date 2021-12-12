import telebot
import config
from djson import *

from telebot import types

# Constants
BUTTON_NAME_JSON_TO_OBJ = "To JSON"
BUTTON_NAME_CSV_TO_OBJ = "To CSV"

BUTTON_NAME_JSON_FROM_OBJ = "From JSON Object"
BUTTON_NAME_CSV_FROM_OBJ = "From CSV Object"

EMPTY_OBJECT = {
	'PublishDate': None,
 	'ContentLen': None,
 	'ArticlesCount': None
}

TEST_STR_OBJECT = '{"PublishDate": "01.12.2021","ContentLen": 10002,"ArticlesCount": 8}'

markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

markup.add(types.KeyboardButton(BUTTON_NAME_JSON_TO_OBJ))
markup.add(types.KeyboardButton(BUTTON_NAME_CSV_TO_OBJ))
markup.add(types.KeyboardButton(BUTTON_NAME_JSON_FROM_OBJ))
markup.add(types.KeyboardButton(BUTTON_NAME_CSV_FROM_OBJ))


bot = telebot.TeleBot(config.TOKEN)
bot_state = "None"
global obj;

# On Start
@bot.message_handler(commands=['start'])
def welcome(message):
	# regular keyboard
	global markup
	global bot_state

	bot_state = 'None'

	bot.send_message(message.chat.id, "Hi, choose what I will be do", 
		reply_markup=markup)

# On User send message
@bot.message_handler(content_types=['text'])
def on_message(message):
	global bot_state
	global markup

	if message.chat.type == 'private':
		command = message.text

		if bot_state == 'None':
			bot_state = command 

			if command == BUTTON_NAME_JSON_TO_OBJ or command == BUTTON_NAME_CSV_TO_OBJ:
				bot.send_message(message.chat.id, "Send me string from file", 
									reply_markup=types.ReplyKeyboardRemove())
			elif command == BUTTON_NAME_JSON_FROM_OBJ or command == BUTTON_NAME_CSV_FROM_OBJ:
				send = bot.send_message(message.chat.id, "Ok. Let's go to create Object", 
									reply_markup=types.ReplyKeyboardRemove())

				if command == BUTTON_NAME_JSON_FROM_OBJ:
					next_task = json_from_object(message)
				else:
					next_task = csv_from_object(message)
				
				bot.register_next_step_handler(send, next_task)
			else:
				bot.send_message(message.chat.id, "Unknown command 😢")
				bot_state = 'None'
			return
		elif bot_state == BUTTON_NAME_JSON_TO_OBJ:
			json_to_object(message)
		elif bot_state == BUTTON_NAME_CSV_TO_OBJ:
			csv_to_object(message)

		bot.send_message(message.chat.id, "OK. Go to start", reply_markup=markup)
		bot_state = 'None'


# Functions 
def json_to_object(message):
	djson = DJson(message.text, message.from_user.username)

	bot.send_message(message.chat.id, "JSON object created:\n")
	bot.send_message(message.chat.id, djson.get_doc_info())

def json_from_object(message):
	get_object(message)

def csv_to_object(message):
	bot.send_message(message.chat.id, "55")

def csv_from_object(message):
	bot.send_message(message.chat.id, "66")

def get_object(message):
	global obj
	obj = EMPTY_OBJECT

	send = bot.send_message(message.chat.id, 'Enter Publish Date')
	bot.register_next_step_handler(send, set_publish_date)

def set_publish_date(message):
	global obj
	obj['PublishDate'] = message.text
	
	send = bot.send_message(message.chat.id, 'Enter Content Length')
	bot.register_next_step_handler(send, set_content_len)
	
def set_content_len(message):
	global obj
	obj['ContentLen'] = message.text

	send = bot.send_message(message.chat.id, 'Enter Articles Count number')
	bot.register_next_step_handler(send, set_articles_count)

def set_articles_count(message): 
	global obj
	obj['ArticlesCount'] = message.text

	send = bot.send_message(message.chat.id, 'OK')
	print(obj)

# Bot start
bot.polling(none_stop=True)