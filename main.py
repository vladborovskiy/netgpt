from datetime import datetime, timedelta
from io import BytesIO
from time import sleep, time

import PIL.Image
import requests
import telebot
from telebot import types

import data
import deepmind
import fusionbrain

bot = telebot.TeleBot('6701320890:AAEikVAmXiNgfoLYaeK01VSJ3bghoGYKeTY')
consolebot = telebot.TeleBot('6863223235:AAGaQ7RdJuW4NlNn5k-tvFTBm7HwX-bdoD0')
data = data.Database()
last_command_time = {}
last_message = {}
ai = deepmind.DeepMind('AIzaSyCQyNOv4RcZF8os4wRUuRBNqabcROdIQKI')


# Command /start
@bot.message_handler(commands=['start'])
def start_message(message):
  start_param = message.text.split(' ')[1] if len(
      message.text.split(' ')) > 1 else None

  if start_param == "premium":
    bot.send_message(message.chat.id, 'Теперь вам доступен премиум!')
    bot.send_message(message.chat.id, '🥳', disable_notification=True)
    bot.send_message(message.chat.id,
                     'Привет! Я ваш чат-помощник. Чем могу помочь?')
    #premium_users[user_id] = True
  #elif user_id in premium_users:
  #bot.send_message(message.chat.id, '👋')
  #bot.send_message(message.chat.id, 'Привет! Я ваш чат-помощник. Чем могу помочь?')
  else:
    bot.send_chat_action(message.chat.id, 'typing')
    bot.send_message(message.chat.id, '👋', disable_notification=True)
    bot.send_message(message.chat.id,
                     'Привет! Я бот-помощник. Напиши что-нибудь.')


# Command /img
@bot.message_handler(commands=['img'])
def img_command(message):
  bot.send_message(message.chat.id, '✨', disable_notification=True)
  msg = bot.send_message(
      message.chat.id,
      'Подробно опишите, что вы хотите увидеть на картинке \n\n/cansel - для отмены'
  )
  bot.register_next_step_handler(msg, ask_description)


def ask_description(message):
  chat_id = message.chat.id
  if len(message.text) < 5:
    bot.send_chat_action(message.chat.id, 'typing')
    bot.send_message(message.chat.id,
                     'Минимальный размер запроса - 5 символов.')
    bot.send_message(chat_id, "Введите /img, чтобы сгенерировать изображение.")
    return
  if len(message.text) > 1000:
    bot.send_chat_action(message.chat.id, 'typing')
    bot.send_message(message.chat.id,
                     'Максимальный размер запроса - 1000 символов.')
    bot.send_message(chat_id, "Введите /img, чтобы сгенерировать изображение.")
    return
  elif message.text == '/cansel':
    bot.send_message(chat_id,
                     "Введите /img, если хотите сгенерировать изображение.")
    return
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
def handle_callback_query(call):
  if call.message and call.message.text.startswith("Выберите стиль:"):
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
                              show_alert=False,
                              text="Изображение придет, когда будет готово!")

    bot.send_message(chat_id, "Ожидайте, генерируется изображение...")
    description_text = call.message.reply_to_message.text

    bot.send_chat_action(chat_id, 'upload_photo')
    image = fusionbrain.draw_image(description_text, int(style))

    if image:
      bot.send_photo(
          chat_id,
          photo=image,
          caption='Ваше изображение готово\nВведите /img, чтобы сгенерировать новое изображение.',
          reply_to_message_id=call.message.reply_to_message.message_id)
      user_id = call.message.reply_to_message.from_user.id
      data.add_img(user_id)
    else:
      bot.send_message(chat_id, '😔', disable_notification=True)
      bot.send_message(
          chat_id, 'Не удалось сгенерировать изображение. Попробуйте еще раз.\nВведите /img, чтобы сгенерировать новое изображение.')
  else:
    answer = call.data
    text = "***Выберите режим:***\n\n***Chat*** - бот будет работать в режиме диалога, т.е запоминать разговор\n***Content*** - вы сможете одновременно спрашивать разные вопросы и получать на них ответ"
    if answer == 'content':
      keyboard = types.InlineKeyboardMarkup()
      chat_button = types.InlineKeyboardButton(text="Chat", callback_data="chat")
      content_button = types.InlineKeyboardButton(text="✨Content",
                                                  callback_data="content")
      keyboard.add(chat_button, content_button)
      bot.answer_callback_query(callback_query_id=call.id,
      show_alert=False,
      text="Режим переключен на content!")
      bot.edit_message_text(chat_id=call.message.chat.id,
        message_id=call.message.message_id, text = text,
        reply_markup=keyboard, parse_mode='markdown')
    if answer == 'chat':
      keyboard = types.InlineKeyboardMarkup()
      chat_button = types.InlineKeyboardButton(text="✨Chat", callback_data="chat")
      content_button = types.InlineKeyboardButton(text="Content",
                                                  callback_data="content")
      keyboard.add(chat_button, content_button)
      bot.answer_callback_query(callback_query_id=call.id,
      show_alert=False,
      text="Режим переключен на chat!")
      bot.edit_message_text(chat_id=call.message.chat.id,
        message_id=call.message.message_id, text = text,
        reply_markup=keyboard, parse_mode='markdown')

# Command /help
@bot.message_handler(commands=['help'])
def help_message(message):
  help_text = '''
***О боте***
Бот работает через официальный API Gemini от Google AI и API Kandisky от Fusionbrain AI.
Бот работает на бета версии ***V1.3.3*** Просьба ***ошибки*** отправлять @F5key

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

***Генерация изображений***
Вы можете сгенерировать изображение на основе вашего запроса. Для этого просто напишите в чат /img. Но для максимально-крутой картинки нужен хороший запрос. Для этого почитайте [нашу статью](http://telegra.ph/Horoshie-prompty-dlya-generacii-kartinok-01-26)

***Поддержка пользователей***
Написать в поддержку — @F5key.
    '''
  bot.send_chat_action(message.chat.id, 'typing')
  bot.send_message(message.chat.id, help_text, parse_mode='Markdown', disable_web_page_preview = True)


# Command /reset
@bot.message_handler(commands=['reset'])
def reset_message(message):
  bot.send_chat_action(message.chat.id, 'typing')
  ai.clear_history()
  bot.send_message(message.chat.id, 'Контекст успешно сброшен!')


# Command /profile
@bot.message_handler(commands=['profile'])
def profile(message):
  try:
    user_id = message.from_user.id
    subscribe = str(data.get_subscribe(user_id))
    text_res = str(data.get_text(user_id))
    img_gen = str(data.get_img(user_id))
    bot.send_chat_action(message.chat.id, 'typing')
    bot.send_message(
        message.chat.id,
        f'***Ваш профиль***\n\nID: {user_id}\nПодписка: {subscribe}\n\n***Статистика***\nТекстовые запросы: {text_res}\nГенерация изображений: {img_gen}',
        parse_mode='Markdown')
  except Exception as e:
    bot.send_message(message.chat.id, 'Профиль не найден.')
    print(f'!Error: {e}')


# Command /mode
@bot.message_handler(commands=['mode'])
def mode(message):
  bot.send_chat_action(message.chat.id, 'typing')
  bot.send_message(message.chat.id, 'Comming soon!')


# Command /settings
@bot.message_handler(commands=['settings'])
def settings_command(message):
  keyboard = types.InlineKeyboardMarkup()
  chat_button = types.InlineKeyboardButton(text="Chat", callback_data="chat")
  content_button = types.InlineKeyboardButton(text="Content",
                                              callback_data="content")
  keyboard.add(chat_button, content_button)
  bot.send_message(message.chat.id, "***Выберите режим:***\n\n***Chat*** - бот будет работать в режиме диалога, т.е запоминать разговор\n***Content*** - вы сможете одновременно спрашивать разные вопросы и получать на них ответ", reply_markup=keyboard, parse_mode='markdown')

# Text message
@bot.message_handler(func=lambda message: True)
def echo_message(message):
  if message.text.startswith('/'):
    if message.text in [
        '/settings', '/help', '/start', '/img', '/profile', '/mode', '/reset'
    ]:
      pass
    else:
      bot.send_chat_action(message.chat.id, 'typing')
      bot.send_message(message.chat.id, 'Нет такой команды! Помощь - /help')
  else:
    user_id = message.from_user.id
    if len(message.text) < 5:
      bot.send_chat_action(message.chat.id, 'typing')
      bot.send_message(message.chat.id,
                       'Минимальный размер запроса - 5 символов.')
      return
    if user_id in last_message and last_message[user_id] == message.text:
      bot.send_chat_action(message.chat.id, 'typing')
      bot.send_message(message.chat.id,
                       'Повторное сообщение. Пожалуйста, уточните запрос.')
      return
    if user_id in last_command_time:
      last_time = last_command_time[user_id]
      elapsed_time = datetime.now() - last_time
      if elapsed_time < timedelta(seconds=1):
        bot.send_chat_action(message.chat.id, 'typing')
        bot.send_message(
            message.chat.id,
            'Слишком много команд. Пожалуйста, подождите некоторое время.')
        chat_id = message.chat.id
        until_date = int(time.time()) + 5
        bot.restrict_chat_member(chat_id, user_id, until_date=until_date)
        return

    user_id = message.from_user.id
    data.add_text(user_id)
    bot.send_chat_action(message.chat.id, 'typing')
    promt = message.text
    answer = ai.generate(promt)
    bot.send_message(message.chat.id, answer, parse_mode='markdown')
    last_command_time[user_id] = datetime.now()
    last_message[user_id] = message.text


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
    response = str(message.caption)
    bot.send_message(message.chat.id,
                     ai.generate_content([response, img]),
                     parse_mode='markdown')
  else:
    user_id = message.from_user.id
    data.add_text(user_id)
    bot.send_chat_action(message.chat.id, 'typing')
    response = 'Реши задачу на картинке'
    bot.send_message(message.chat.id,
                     ai.generate_content([response, img]),
                     parse_mode='markdown')


def send_message_console(message):
  consolebot.send_message(6441643574, message, parse_mode='markdown')


# Start the bot
if __name__ == "__main__":
  while True:
    try:
      print(" * Serving Telegram bot 'main.py'")
      dt = datetime.now()
      dt = dt.replace(microsecond=0)
      send_message_console(
          f"***Serving Telegram bot*** 'main.py' at\n ___{str(dt)}___")
      bot.polling()
    except Exception as e:
      print('!Fatal error: ' + str(e))
      dt = datetime.now()
      dt = dt.replace(microsecond=0)
      send_message_console(f'***!Fatal error:*** `{str(e)}` at\n ___{str(dt)}___')
      sleep(5)
