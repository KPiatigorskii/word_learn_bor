import logging
import os
import pymongo
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, Poll
from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv

from dictionary import Dictionary

from easygoogletranslate import EasyGoogleTranslate

load_dotenv()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

translate_en_to_iw = EasyGoogleTranslate(
    source_language='en',
    target_language='iw',
    timeout=10
)

dictionary_class = Dictionary()

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)


async def create_dictionary(update: Update, context: ContextTypes.DEFAULT_TYPE):
    new_dictionary_name = ' '.join(context.args)
    dictionary_class.create_dictionary(new_dictionary_name)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"dictionary successfully created")

async def select_dictionary(update: Update, context: ContextTypes.DEFAULT_TYPE):
    current_dictionary = ' '.join(context.args)
    dictionary_class.set_name(current_dictionary)
    word_amount = dictionary_class.get_words_amount()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"You choose dictionary \"{current_dictionary}\" with {word_amount} words")

async def get_select_dictionary(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Your current dictionary is \"{dictionary_class.get_name()}\"")


async def add_word(update: Update, context: ContextTypes.DEFAULT_TYPE):
    word = ' '.join(context.args)
    inserted_id = dictionary_class.insert_word(word)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"word was added with id {inserted_id}")

async def confirm_word(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pass

async def start_victorine(update: Update, context: ContextTypes.DEFAULT_TYPE):
    dictionary_class.get_random_words(4)
    q = 'What is the capital of Italy?'
    answers = ['Rome', 'London', 'Amsterdam']
    await context.bot.send_poll(chat_id=update.effective_chat.id, question=q, options=answers, type=Poll.QUIZ,
                                correct_option_id=0)
    await context.bot.send_poll(chat_id=update.effective_chat.id, question=q, options=answers, type=Poll.QUIZ,
                                correct_option_id=0)
    await context.bot.send_poll(chat_id=update.effective_chat.id, question=q, options=answers, type=Poll.QUIZ,
                                correct_option_id=0)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


async def new_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pass

if __name__ == '__main__':
    application = ApplicationBuilder().token(os.getenv('TG_BOT_TOKEN')).build()

    start_victorine_handler = CommandHandler('start_victorine', start_victorine)
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    start_handler = CommandHandler('start', start)
    add_word_handler = CommandHandler('add_word', add_word)
    select_dictionary_handler = CommandHandler("select_dictionary", select_dictionary)
    create_dictionary_handler = CommandHandler("create_dictionary", create_dictionary)
    get_select_dictionary_handler = CommandHandler("get_select_dictionary", get_select_dictionary)

    application.add_handler(start_victorine_handler)
    application.add_handler(start_handler)
    application.add_handler(add_word_handler)
    application.add_handler(select_dictionary_handler)
    application.add_handler(create_dictionary_handler)
    application.add_handler(get_select_dictionary_handler)

    application.run_polling()