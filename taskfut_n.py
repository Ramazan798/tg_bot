import requests
import json
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Замените <YOUR_API_KEY> на ваш API ключ с сайта https://www.alphavantage.co/
API_KEY = "<6322698332:AAFTGAaqaygm6il9DAWeLA1HYmZlMAof7t0>"

# Обработчик команды /start
def start(update, context):
    update.message.reply_text("Привет! Я финансовый бот. Я могу предоставить информацию о курсах валют и индексах фондовых рынков.")

# Обработчик команды /help
def help(update, context):
    update.message.reply_text("Я могу выполнить следующие команды:\n"
                              "/start - начать диалог с ботом\n"
                              "/help - получить список доступных команд\n"
                              "/currency - получить информацию о курсе конкретной валюты\n"
                              "/index - получить информацию о конкретном индексе фондового рынка")

# Обработчик команды /currency
def currency(update, context):
    if len(context.args) == 0:
        update.message.reply_text("Использование команды: /currency <код валюты>")
        return

    currency_code = context.args[0].upper()
    response = requests.get(f"https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={currency_code}&to_currency=RUB&apikey={API_KEY}")
    data = json.loads(response.text)

    if "Realtime Currency Exchange Rate" not in data:
        update.message.reply_text("Не удалось получить информацию о курсе валюты")
        return

    exchange_rate = data["Realtime Currency Exchange Rate"]["5. Exchange Rate"]
    update.message.reply_text(f"Курс {currency_code} к RUB: {exchange_rate}")

# Обработчик команды /index
def index(update, context):
    if len(context.args) == 0:
        update.message.reply_text("Использование команды: /index <код индекса>")
        return

    index_code = context.args[0].upper()
    response = requests.get(f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={index_code}&apikey={API_KEY}")
    data = json.loads(response.text)

    if "Global Quote" not in data:
        update.message.reply_text("Не удалось получить информацию об индексе")
        return

    index_price = data["Global Quote"]["05. price"]
    index_change = data["Global Quote"]["09. change"]
    update.message.reply_text(f"Индекс {index_code}: Цена: {index_price}, Изменение: {index_change}")

# Обработчик текстовых сообщений
def echo(update, context):
    update.message.reply_text("Я не понимаю эту команду. Пожалуйста, используйте /help для получения списка доступных команд.")

# Создание и запуск бота
def main():
    updater = Updater("<YOUR_TELEGRAM_BOT_TOKEN>", use_context=True)

    updater.dispatcher.add_handler(CommandHandler("start", start))
    updater.dispatcher.add_handler(CommandHandler("help", help))
    updater.dispatcher.add_handler(CommandHandler("currency", currency))
    updater.dispatcher.add_handler(CommandHandler("index", index))

    updater.dispatcher.add_handler(MessageHandler(Filters.text, echo))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()