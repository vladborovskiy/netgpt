import telebot
import data
import PIL.Image
from io import BytesIO
import requests
from telebot import types
from time import sleep
import gemini, kandisky

bot = telebot.TeleBot('6701320890:AAEikVAmXiNgfoLYaeK01VSJ3bghoGYKeTY')
consolebot = telebot.TeleBot('6863223235:AAGaQ7RdJuW4NlNn5k-tvFTBm7HwX-bdoD0')
data = data.Database()
king_id = 644164357


# Command /start
@bot.message_handler(commands=['start'])
def start_message(message):
  start_param = message.text.split(' ')[1] if len(
      message.text.split(' ')) > 1 else None

  if start_param == "premium":
    bot.send_message(message.chat.id, 'Теперь вам доступен премиум!')
    bot.send_message(message.chat.id, '🥳')
    bot.send_message(message.chat.id,
                     'Привет! Я ваш чат-помощник. Чем могу помочь?')
    #premium_users[user_id] = True
  #elif user_id in premium_users:
  #bot.send_message(message.chat.id, '👋')
  #bot.send_message(message.chat.id, 'Привет! Я ваш чат-помощник. Чем могу помочь?')
  else:
    bot.send_chat_action(message.chat.id, 'typing')
    bot.send_message(message.chat.id, '👋')
    bot.send_message(message.chat.id,
                     'Привет! Я бот-помощник. Напиши что-нибудь.')
  print('Processed /start command!')


# Command /img
@bot.message_handler(commands=['img'])
def img_command(message):
  bot.send_message(message.chat.id, '✨')
  msg = bot.send_message(
      message.chat.id, 'Подробно опишите, что вы хотите увидеть на картинке')
  bot.register_next_step_handler(msg, ask_description)


def ask_description(message):
  chat_id = message.chat.id
  markup = types.InlineKeyboardMarkup(row_width=1)
  button1 = types.InlineKeyboardButton(text="Кандинский", callback_data="0")
  button2 = types.InlineKeyboardButton(text="Детальное фото",
                                       callback_data="1")
  button3 = types.InlineKeyboardButton(text="Аниме", callback_data="2")
  button4 = types.InlineKeyboardButton(text="Стандартный", callback_data="3")
  markup.add(button1, button2, button3, button4)
  bot.send_message(chat_id,
                   "Выберите стиль:",
                   reply_markup=markup,
                   reply_to_message_id=message.message_id)


@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query_img(call):
  if call.message:
    chat_id = call.message.chat.id
    text_style = ""
    style = call.data

    if style == '0':
      text_style = "Кандинский"
    elif style == '1':
      text_style = "Детальное фото"
    elif style == '2':
      text_style = "Аниме"
    elif style == '3':
      text_style = "Стандартный"
    bot.edit_message_text(chat_id=call.message.chat.id,
                          message_id=call.message.message_id,
                          text=str("Вы выбраль стиль: " + text_style),
                          reply_markup=None)
    bot.answer_callback_query(callback_query_id=call.id,
                              show_alert=True,
                              text="Изображение придет, когда будет готово!")

    bot.send_message(chat_id, "Ожидайте, генерируется изображение...")
    description_text = call.message.reply_to_message.text

    bot.send_chat_action(chat_id, 'upload_photo')
    image = kandisky.draw_image(description_text, int(style))

    if image:
      bot.send_photo(chat_id, photo=image, caption='Ваше изображение:')
    else:
      bot.send_message(chat_id, '😔')
      bot.send_message(
          chat_id, 'Не удалось сгенерировать изображение. Попробуйте еще раз.')
    bot.send_message(chat_id,
                     "Введите /img, чтобы сгенерировать новое изображение.")
  user_id = call.message.reply_to_message.from_user.id
  data.add_img(user_id)
  print('Processed /img command!')


# Command /help
@bot.message_handler(commands=['help'])
def help_message(message):
  help_text = '''
***О боте***
Бот работает через официальный API Gemini от Google AI и API Kandisky от Fusionbrain AI.
Бот работает на бета версии ***V1.2*** Просьба ***ошибки*** отправлять @F5key

***Команды бота***
/start - Перезапуск бота.
/mode - Позволяет выбрать нейросеть для генерации.
/img - Создать изображение на основе вашего запроса.
/reset - Сброс контекста для начала нового диалога.
/profile - Просмотр профиля пользователя с информацией о его предпочтениях.
/settings - Настройка различных параметров, таких как язык и дополнительные параметры генерации изображений.

***Что такое контекст?***
Бот работает в режиме контекста, то есть запоминает предыдущие сообщения. Это сделано для того, чтобы можно было уточнить дополнения или вести диалог. Команда /reset сбрасывает контекст.

***Распознавание изображений***
Вы можете сделать запрос прикрепив изображение. Бот распознает изображение и ответит на ваш запрос. Для этого просто прикрепите изображение к запросу. Работает только с Gemini-Pro-Vision.

***Поддержка пользователей***
Написать в поддержку — @F5key.
    '''
  bot.send_chat_action(message.chat.id, 'typing')
  bot.send_message(message.chat.id, help_text, parse_mode='Markdown')
  print('Processed /help command!')


# Command /reset
@bot.message_handler(commands=['reset'])
def reset_message(message):
  try:
    bot.send_chat_action(message.chat.id, 'typing')
    gemini.reset_context()
    bot.send_message(message.chat.id, 'Контекст успешно сброшен!')
  except:
    bot.send_message(message.chat.id, 'Ошибка сброса, попробуйте ещё раз')
  print('Processed /reset command!')


# Command /profile
@bot.message_handler(commands=['profile'])
def profile(message):
  user_id = message.from_user.id
  subscribe = 'premium'
  text_res = str(data.get_text(user_id))
  img_gen = str(data.get_img(user_id))
  bot.send_chat_action(message.chat.id, 'typing')
  bot.send_message(
      message.chat.id,
      f'***Ваш профиль***\n\nID: {user_id}\nПодписка: {subscribe}\n\n***Статистика***\nТекстовые запросы: {text_res}\nГенерация изображений: {img_gen}',
      parse_mode='Markdown')
  print('Processed /profile command!')


# Command /mode
@bot.message_handler(commands=['mode'])
def mode(message):
  bot.send_chat_action(message.chat.id, 'typing')
  bot.send_message(message.chat.id, 'soon')
  print('Processed /mode command!')


# Command /settings
@bot.message_handler(commands=['settings'])
def settings(message):
  bot.send_chat_action(message.chat.id, 'typing')
  bot.send_message(message.chat.id, 'soon')
  print('Processed /settings command!')


# Text message
@bot.message_handler(func=lambda message: True)
def echo_message(message):
  if message.text.startswith('/'):
    if message.text in [
        '/settings', '/help', '/start', '/img', '/cancel', '/profile', '/mode',
        '/reset'
    ]:
      # Handle commands that are allowed
      pass
    else:
      # Handle unknown commands
      bot.send_message(message.chat.id, 'Нет такой команды! Для помощи /help')
  else:
    user_id = message.from_user.id
    data.add_text(user_id)
    bot.send_chat_action(message.chat.id, 'typing')
    bot.send_message(message.chat.id,
                     gemini.generate('gemini-pro', str(message.text), False),
                     parse_mode='markdown')
    print('Processed text command!')


# Photo message
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
  file_id = message.photo[-1].file_id
  file_info = bot.get_file(file_id)
  img_url = f'https://api.telegram.org/file/bot{bot.token}/{file_info.file_path}'
  img_save = requests.get(img_url).content
  img = PIL.Image.open(BytesIO(img_save))

  if message.caption is not None:
    user_id = message.from_user.id
    data.add_text(user_id)
    bot.send_chat_action(message.chat.id, 'typing')
    response = message.caption
    bot.send_message(message.chat.id,
                     gemini.generate('gemini-pro-vision', [response, img],
                                     False),
                     parse_mode='markdown')
  else:
    user_id = message.from_user.id
    data.add_text(user_id)
    bot.send_chat_action(message.chat.id, 'typing')
    response = 'Реши задачу на картинке'
    bot.send_message(message.chat.id,
                     gemini.generate('gemini-pro-vision', [response, img],
                                     False),
                     parse_mode='markdown')
  print('Processed photo command!')


def send_message_console(message):
  consolebot.send_message(6441643574, message)


# Start the bot
while True:
  try:
    print('Bot is running!')
    send_message_console('Bot is running!')
    bot.polling()
  except Exception as e:
    print('Fatal error: ' + str(e))
    send_message_console(f'Fatal error: {str(e)}')
    sleep(5)

send_message_console('Bot is stopped!')
