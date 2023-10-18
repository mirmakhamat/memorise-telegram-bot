from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler
from db.functions.user import register
from bot.keyboards.user import main_keyboard_markup
from bot.keyboards.word import back_keyboard_markup
from bot import states


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
    return ConversationHandler.END

def settings(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer("Soon")

def add(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        "Yangi so'zni kiriting\n\n<b>so'z</b>\n<i>tarjima</i>\n\nSo'zni rasm orqali yoki rasm kiritimsadan kiritish mumkin.",
        parse_mode="HTML",
        reply_markup=back_keyboard_markup()
    )

    return states.NEW