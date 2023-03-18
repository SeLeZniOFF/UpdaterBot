import telebot
import os

bot = telebot.TeleBot("6093967066:AAFrAi3LwxYZ0vj8PDJXce7RIY9OZt84jpA")

# List of categories
categories = ["1.Для_чата_стрингеров", "2.Для_поддержки_360", "3.Для_чата_Терминал_доработки", "4.Для_чата_Мультиадминка_Подм_Сегодня+муниципалы"]

# Create files for each category, if they don't already exist
for category in categories:
    filename = category.split(".")[1] + ".md"
    filepath = os.path.join(os.getcwd(), filename)
    if not os.path.exists(filepath):
        with open(filepath, "w", encoding="utf-8") as f:
            f.write("# Заметки для категории {}\\\\n\\\\n".format(category))

# Handler for /start command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Этот бот поможет тебе сохранять заметки в разных категориях. Напиши /help, чтобы узнать как им пользоваться.")

# Handler for /help command
@bot.message_handler(commands=['help'])
def send_help(message):
    text = "Чтобы сохранить заметку, выбери категорию и напиши сообщение. Например, '1 Привет, чат стрингеров!'\\\\n\\\\n"
    text += "Чтобы посмотреть заметки в категории, напиши '/view название_файла'.\\\\n"
    text += "Категории:\\\\n"
    for category in categories:
        text += category + "\\\\n"
    bot.reply_to(message, text)

# Handler for /view command
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
@bot.message_handler(func=lambda message: True)
def save_note_multiple_categories(message):
    categories_to_save = []
    for word in message.text.split():
        if word.isdigit() and int(word) in range(1, 5):
            categories_to_save.append(categories[int(word)-1])
    if categories_to_save:
        for category in categories_to_save:
            filename = category.split(".")[1] + ".md"
            filepath = os.path.join(os.getcwd(), filename)
            with open(filepath, "a", encoding="utf-8") as f:
                f.write("📌 " + message.text.strip() + "\n\n")
        bot.reply_to(message, "Заметка сохранена в {} категориях.".format(len(categories_to_save)))
    else:
        bot.reply_to(message, "Ошибка. Некорректные категории.")

bot.polling()

