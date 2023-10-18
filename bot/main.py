import logging
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, ConversationHandler, MessageHandler, Filters
from bot import config
from bot.handlers import user
from bot.handlers import word
from bot.keyboards import user as user_keyboard
from bot.keyboards import word as word_keyboard
from bot import states


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def main() -> None:
    """Start the bot."""
    updater = Updater(config.TOKEN)

    dispatcher = updater.dispatcher
    
    handlers = [
        CommandHandler('start', user.start),
        CallbackQueryHandler(word.update_words, pattern=user_keyboard.NEW_WORDS_KEY),
        CallbackQueryHandler(word.review_words, pattern=user_keyboard.REVIEW_KEY),
        CallbackQueryHandler(word.update_words, pattern=word_keyboard.WORD_KEY),
        CallbackQueryHandler(word.review_words, pattern=word_keyboard.REVIEW_KEY),
        CallbackQueryHandler(word.check, pattern=word_keyboard.CHECK_KEY),
        CallbackQueryHandler(word.audio, pattern=word_keyboard.AUDIO_KEY),
        CallbackQueryHandler(user.back_to_main, pattern=word_keyboard.BACK_KEY),
        CallbackQueryHandler(user.settings, pattern=user_keyboard.SETTINGS_KEY),
        CallbackQueryHandler(word.example, pattern=word_keyboard.EXAMPLE_KEY),
        ConversationHandler(
            entry_points=[
                CommandHandler('add', user.add),
            ],
            states={
                states.NEW: [
                    CallbackQueryHandler(user.back_to_main, pattern=word_keyboard.BACK_KEY),
                    MessageHandler(Filters.photo | Filters.text, word.add_word),
                ],
                states.AUDIO: [
                    CommandHandler('skip', user.start),
                    MessageHandler(Filters.audio, word.add_audio),
                ]
            },
            fallbacks=[]
        )
    ]

    for handler in handlers:
        dispatcher.add_handler(handler)
    
    updater.start_polling()
    updater.idle()
