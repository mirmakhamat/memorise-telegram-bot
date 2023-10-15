import logging
from telegram.ext import Updater, CommandHandler, ConversationHandler
from bot import config
from bot.handlers import user
# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(config.TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', user.start)],
        states={
            # GENDER: [MessageHandler(Filters.regex('^(Boy|Girl|Other)$'), gender)],
            # PHOTO: [MessageHandler(Filters.photo, photo), CommandHandler('skip', skip_photo)],
            # LOCATION: [
            #     MessageHandler(Filters.location, location),
            #     CommandHandler('skip', skip_location),
            # ],
            # BIO: [MessageHandler(Filters.text & ~Filters.command, bio)],
        },
        fallbacks=[CommandHandler('start', user.start)],
    )

    dispatcher.add_handler(conv_handler)
    # on different commands - answer in Telegram

    # Start the Bot
    updater.start_polling()
    updater.idle()
