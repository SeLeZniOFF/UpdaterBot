import os
import re
import telebot
from dotenv import load_dotenv
from urllib.request import urlretrieve

# Load environment variables
load_dotenv()

# Initialize the bot
bot = telebot.TeleBot(os.getenv("BOT_TOKEN"))

# Define the categories
categories = ["1.Чат стрингеров", "2.Поддержка 360", "3.Терминал доработки", "4.МА ПодмСегодня муниципалы", "5.Тезисы к созвонам" , "6.Конспект созвонов"]

def create_main_menu():
    markup = telebot.types.InlineKeyboardMarkup()
    for category in categories:
        save_button = telebot.types.InlineKeyboardButton("💾 " + category.split(".")[1], callback_data="save_" + category)
        view_button = telebot.types.InlineKeyboardButton("👁 " + category.split(".")[1], callback_data="view_" + category)
        clear_button = telebot.types.InlineKeyboardButton("🗑 " + category.split(".")[1], callback_data="clear_" + category)
        markup.row(save_button, view_button, clear_button)
    return markup

# Handler for /start command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = create_main_menu()
    bot.reply_to(message, "Привет! Этот бот поможет тебе сохранять заметки в разных категориях. Выбери категорию, в которую хочешь добавить заметку или просмотреть заметки:", reply_markup=markup)

@bot.message_handler(commands=['help'])
def send_welcome(message):
    markup = create_main_menu()
    bot.reply_to(message, "Для того чтобы добавить заметку, выберите категорию и напиши сообщение. \n"
    "Для того чтобы просмотреть готовое сообщение выберите кнопку с глазом напротив категории.\n",
    reply_markup=markup)

# Handler for inline keyboard button presses
@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    action, category = call.data.split("_", 1)
    if action == "save":
        save_note_callback(call, category)
    elif action == "view":
        view_notes_callback(call, category)
    elif action == "clear":
        clear_notes_callback(call, category)

def save_note_callback(call, category):
    message = call.message
    bot.answer_callback_query(call.id, "Заметка будет сохранена в категории {}".format(category.split(".")[1]))
    bot.edit_message_text("Отправь сообщение, которое нужно сохранить:", message.chat.id, message.message_id)
    bot.register_next_step_handler(message, save_note, category)



def clear_notes_callback(call, category):
    message = call.message
    filename = category.split(".")[1].replace(" ", "_") + ".md"
    filepath = os.path.join(os.getcwd(), filename)
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write("")
        bot.answer_callback_query(call.id, "Заметки в категории {} успешно очищены.".format(category.split(".")[1]))
    except FileNotFoundError:
        bot.answer_callback_query(call.id, "Ошибка. Файл не найден.")
def view_notes_callback(call, category):
    message = call.message
    filename = category.split(".")[1].replace(" ", "_") + ".md"
    filepath = os.path.join(os.getcwd(), filename)
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            file_content = f.read()
        bot.answer_callback_query(call.id)
        bot.send_message(message.chat.id, file_content)
    except FileNotFoundError:
        bot.answer_callback_query(call.id, "Ошибка. Файл не найден.")

def save_note(message, category):
    clean_message = re.sub(r'\\d+', '', message.text).strip()
    filename = category.split(".")[1].replace(" ", "_") + ".md"
    filepath = os.path.join(os.getcwd(), filename)
    with open(filepath, "a", encoding="utf-8") as f:
        f.write("📌 " + clean_message + "\n\n")
    bot.reply_to(message, f"Заметка сохранена в категории: {category.split('.')[1]}")
    markup = create_main_menu()
    bot.send_message(message.chat.id, "Выбери категорию, в которую хочешь добавить заметку или просмотреть заметки:", reply_markup=markup)

# Start the bot
bot.polling()