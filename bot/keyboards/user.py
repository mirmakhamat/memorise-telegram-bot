# inline keyboard
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

NEW_WORDS_KEY = "new_words"
REVIEW_KEY = "review_words"
SETTINGS_KEY = "settings"


def main_keyboard_markup():
    main_keyboard = [
        [
            InlineKeyboardButton("📚 Learning new words",
                                 callback_data=NEW_WORDS_KEY),
        ],
        [InlineKeyboardButton("📖 Review words", callback_data=REVIEW_KEY)],
        [InlineKeyboardButton("⚙️ Settings", callback_data=SETTINGS_KEY)],
    ]

    return InlineKeyboardMarkup(main_keyboard)
