
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from db.functions.user import register


def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    register(user.id, user.first_name,
             user.last_name)
    update.message.reply_text(
        "Assalomu alayukum, {0} {1}!\n".format(
            user.first_name, user.last_name),
    )
