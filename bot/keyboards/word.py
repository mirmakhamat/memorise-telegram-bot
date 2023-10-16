# inline keyboard
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

BACK_KEY = "back"
CHECK_KEY = "check"
REVIEW_KEY = "review"
WORD_KEY = "word"
AUDIO_KEY = "audio"

def word_keyboard_markup(type, word_id, user_id, audio=None):
    word_keyboard = [
        [
            InlineKeyboardButton("✅ Known", callback_data=f"{type}-{word_id}-{user_id}-1"),
            InlineKeyboardButton("♻️ Learn", callback_data=f"{type}-{word_id}-{user_id}-2"),
        ],
        [
            InlineKeyboardButton("🧐 Check", callback_data=f"{CHECK_KEY}-{word_id}"),
        ],
        [
            InlineKeyboardButton("🔙 Back", callback_data=BACK_KEY),
        ]
    ]
    if audio:
        word_keyboard[0].insert(1, InlineKeyboardButton("🎙", callback_data=f"{AUDIO_KEY}-{word_id}"))
        
    return InlineKeyboardMarkup(word_keyboard)


def back_keyboard_markup():
    back_keyboard = [
        [
            InlineKeyboardButton("🔙 Back", callback_data=BACK_KEY),
        ]
    ]
    return InlineKeyboardMarkup(back_keyboard)