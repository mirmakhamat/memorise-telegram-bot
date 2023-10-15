
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from db.functions.user import register
from bot.keyboards.user import main_keyboard_markup
from db.functions.word import get_user_word


def new_words(update: Update, context: CallbackContext) -> None:
    query = update.callback_query

    query.answer()
    word = get_user_word(query.from_user.id)
    if word:
        query.edit_message_text(text=f"Edited message {word.word}")
    else:
        query.edit_message_text(text="No words")
