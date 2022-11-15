import telebot, os, requests, validators, math, re, collections
from telebot import types
bot = telebot.TeleBot('5604918525:AAEGJil1o2cwvx6AlVobkb51d362wkleztc')
predlogs = ["без","за","близ","в","ввиду","вне","для","до","за",
"из","из-за","к","ко","кроме","на","над","от","перед","по","под",
"при","пред","с","кто","как", "когда","который","какой","где","куда",
"откуда","и", "ни-ни", "тоже", "также", "а", "но", "однако", "зато", "же", "или", "либо", "то-то", "у", "о", "об"]
status = ''
start_message = str('Введите команду:' + '\n'
+ '/site - проверить доступность сайта' + '\n' 
+ '/text - анализ текста' + '\n' 
+ '/calc - калькулятор' + '\n' 
+ '/exit - выход из бота')

value = ""
old_value = ""
keyboard = telebot.types.InlineKeyboardMarkup()
keyboard.row(   telebot.types.InlineKeyboardButton("sqrt", callback_data="sqrt"),
                telebot.types.InlineKeyboardButton("C", callback_data="C"),
                telebot.types.InlineKeyboardButton("<=", callback_data="<="),
                telebot.types.InlineKeyboardButton("/", callback_data="/") )

keyboard.row(   telebot.types.InlineKeyboardButton("log", callback_data="log"),
                telebot.types.InlineKeyboardButton("7", callback_data="7"),
                telebot.types.InlineKeyboardButton("8", callback_data="8"),
                telebot.types.InlineKeyboardButton("9", callback_data="9"),
                telebot.types.InlineKeyboardButton("*", callback_data="*") )

keyboard.row(   telebot.types.InlineKeyboardButton("sin", callback_data="sin"),
                telebot.types.InlineKeyboardButton("4", callback_data="4"),
                telebot.types.InlineKeyboardButton("5", callback_data="5"),
                telebot.types.InlineKeyboardButton("6", callback_data="6"),
                telebot.types.InlineKeyboardButton("-", callback_data="-") )

keyboard.row(   telebot.types.InlineKeyboardButton("cos", callback_data="cos"),
                telebot.types.InlineKeyboardButton("1", callback_data="1"),
                telebot.types.InlineKeyboardButton("2", callback_data="2"),
                telebot.types.InlineKeyboardButton("3", callback_data="3"),
                telebot.types.InlineKeyboardButton("+", callback_data="+") )

keyboard.row(   telebot.types.InlineKeyboardButton("tan", callback_data="tan"),
                telebot.types.InlineKeyboardButton("+/- ", callback_data="+/-"),
                telebot.types.InlineKeyboardButton("0", callback_data="0"),
                telebot.types.InlineKeyboardButton(",", callback_data="."),
                telebot.types.InlineKeyboardButton("=", callback_data="=") )

@bot.message_handler(commands=["start"])
def start(message, res=False):
    bot.send_message(message.chat.id, start_message)

# Получение сообщений
@bot.message_handler(content_types=["text"])
def handle_text(message):
    global status
    text = message.text
    if text == '/exit' and status != '':
        status = ''
        bot.send_message(message.chat.id, start_message)
        return
    if status == '':
        if text == '/site':
            status = text
            bot.send_message(message.chat.id, "Введите URL сайта:")
            bot.register_next_step_handler(message, get_site)#запуск проверки сайта
        elif text == '/text':
            status = text
            bot.send_message(message.chat.id, "Введите текст:")
            bot.register_next_step_handler(message, start_textAnalyst)#запуск проверки текста
        elif text == '/calc':
            status = text
            start_calculator(message)#запуск калькулятора
        else:
            bot.send_message(message.chat.id, "Некорректная команда!")
            bot.send_message(message.chat.id, start_message)
    elif status == '/site':
        get_site(message)#запуск проверки сайта
    elif status == '/text':
        start_textAnalyst(message)#запуск проверки текста
    elif text == '/calc':
        start_calculator(message)#запуск калькулятора

#Проверка сайта
def get_site(message):
    if validators.url(message.text):
        bot.send_message(message.chat.id, 'Выполняется проверка, ожидайте...')
        try:
            requests.get(message.text)
            bot.send_message(message.chat.id, 'Сайт доступен!')
        except:
            bot.send_message(message.chat.id, 'Сайт недоступен!')    
    else:
        bot.send_message(message.chat.id, 'Введен некорректный URL, попробуйте снова')

    bot.send_message(message.chat.id, 'Введите URL сайта:')

#Анализ текста
def start_textAnalyst(message):
    text = message.text
    try:
        sentences = text.split(".")
        if sentences[-1] == "":
            sentences.pop()
        sentences_length = len(sentences)

        text = re.sub(r'[^\w\s]','', text.lower())
        words = text.split()

        clear_words = []
        for word in words:
            if word not in predlogs:
                clear_words.append(word)

        counter_words = collections.Counter(clear_words)
        common_words = counter_words.most_common()[:3]
        longest_word = max(clear_words, key=len)
        
        bot.send_message(message.chat.id, 
        'Количество предложений: ' + str(sentences_length) + '\n' +
        'Количество уникальных слов: ' + str(len(counter_words)) + '\n' +
        'Самые популярные слова: '+ '\n' +
        str(common_words[0]) + ", "+ '\n' +
        str(common_words[1]) + ", " + '\n' +
        str(common_words[2]) + '\n' +
        'Самое длинное: ' + str(longest_word)
        )
        bot.send_message(message.chat.id, "Введите текст:")
    except:
        bot.send_message(message.chat.id, "Ошибка анализа текста! Введите другой.")

def start_calculator(message):
    global value, keyboard
    if value == "":
        bot.send_message(message.from_user.id, "0", reply_markup=keyboard)
    else:
        bot.send_message(message.from_user.id, value, reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def callback_func(call):
    global value, old_value
    data = call.data
    message_error = "Ошибка вычисления"
    try:
        if data == "C" :
            value = ""
        elif data == "log":
            result = eval(value)
            if result > 0:
                value = str(math.log(eval(value)))
            else:
                value = "log error!"
        elif data == "sqrt":
            result = eval(value)
            if result > 0:
                value = str(math.sqrt(eval(value)))
            else:
                value = "sqrt error!"
        elif data == "sin":
            value = str(math.sin(eval(value)))
        elif data == "cos":
            value = str(math.cos(eval(value)))
        elif data == "tan":
            value = str(math.tan(eval(value)))
        elif data == "+/-":
            value = str(eval(value)*(-1))
        elif data == "=" :
            value = str(eval(value))
        else:
            value += data
    except:
        value = message_error

    if value != old_value:
        if value == "":
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="0", reply_markup=keyboard)
        else:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=value, reply_markup=keyboard)

    old_value = value
    if value == message_error: value = ""  

bot.polling(none_stop=True, interval=0)

