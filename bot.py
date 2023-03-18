import os
import re
import telebot
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize the bot
bot = telebot.TeleBot(os.getenv("BOT_TOKEN"))

# Define the categories
categories = ["1.Для чата стрингеров", "2.Для поддержки 360", "3.Для чата Терминал доработки", "4.МА ПодмСегодня муниципалы"]

# Handler for /start command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = telebot.types.InlineKeyboardMarkup()
    for category in categories:
        button = telebot.types.InlineKeyboardButton(category.split(".")[1], callback_data=category)
        markup.add(button)
    bot.reply_to(message, "Привет! Этот бот поможет тебе сохранять заметки в разных категориях. Выбери категорию, в которую хочешь добавить заметку:", reply_markup=markup)

# Handler for inline keyboard button presses
@bot.callback_query_handler(func=lambda call: True)
def save_note_callback(call):
    categories_to_save = [call.data]
    message = call.message
    bot.answer_callback_query(call.id, "Заметка будет сохранена в категории {}".format(call.data.split(".")[1]))
    bot.edit_message_text("Отправь сообщение, которое нужно сохранить:", message.chat.id, message.message_id)
    bot.register_next_step_handler(message, save_note_multiple_categories, categories_to_save)
@bot.message_handler(commands=['view'])
def view_file(message):
    try:
        # Get the file name from the command arguments
        file_name = message.text.split()[1]
        # Add the .md extension if it's not already included
        if not file_name.endswith('.md'):
            file_name += '.md'
        # Open the file and read its contents
        with open(file_name, "r", encoding="utf-8") as f:
            file_content = f.read()
        # Send the file's contents to the user as a message
        bot.reply_to(message, file_content)
    except IndexError:
        # If no file name is specified, display an error message
        bot.reply_to(message, "Ошибка. Не указано название файла.")
    except FileNotFoundError:
        # If the file is not found, display an error message
        bot.reply_to(message, "Ошибка. Файл не найден.")


# Handler for all other messages
def save_note_multiple_categories(message, categories_to_save):
    clean_message = re.sub(r'\\d+', '', message.text).strip()
    saved_categories = []
    for category in categories_to_save:
        filename = category.split(".")[1].replace(" ", "_") + ".md"
        filepath = os.path.join(os.getcwd(), filename)
        with open(filepath, "a", encoding="utf-8") as f:
            f.write("📌 " + clean_message + "\n\n")
        saved_categories.append(category.split(".")[1])
    categories_str = ', '.join(saved_categories)
    bot.reply_to(message, f"Заметка сохранена в категориях: {categories_str}")
    markup = telebot.types.InlineKeyboardMarkup()
    for category in categories:
        button = telebot.types.InlineKeyboardButton(category.split(".")[1], callback_data=category)
        markup.add(button)
    bot.send_message(message.chat.id, "Выбери категорию, в которую хочешь добавить заметку:", reply_markup=markup)


# Start the bot
bot.polling()
