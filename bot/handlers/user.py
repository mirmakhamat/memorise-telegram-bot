from telegram import Update
from telegram.ext import CallbackContext
from db.functions.user import register
from bot.keyboards.user import main_keyboard_markup


def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    register(user.id, user.first_name, user.last_name)

    update.message.reply_text(
        "You are in main menu",
        reply_markup=main_keyboard_markup()
    )

def back_to_main(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer
    query.edit_message_text(
        "You are in main menu",
        reply_markup=main_keyboard_markup()
    )

def settings(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer("Soon")