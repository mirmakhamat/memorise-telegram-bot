from telegram import Update, InputMediaPhoto
from telegram.ext import CallbackContext
from bot.keyboards.word import word_keyboard_markup, back_keyboard_markup, REVIEW_KEY, WORD_KEY
from db.functions.word import get_user_word, users_words_create, get_user_review_word, get_word
from db.functions.user import get_user_data


def update_words(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    data = query.data.split('-')
    query.answer()

    if len(data) > 3:
        users_words_create(data[2], data[1], data[3])

    user = get_user_data(query.from_user.id)
    word = get_user_word(user.id)

    if word:
        reply_markup = word_keyboard_markup(WORD_KEY, word.id, user.id, word.audio)
        text = word.word
        if word.photo:
            if query.message.photo:
                query.edit_message_media(
                    media=InputMediaPhoto(word.photo),
                    caption=text, 
                    reply_markup=reply_markup
                )
            else:
                query.message.reply_photo(
                    photo=word.photo, 
                    caption=text, 
                    reply_markup=reply_markup
                )
                query.message.delete()
            
        else:
            if query.message.photo:
                query.message.reply_text(
                    text=text,
                    reply_markup=reply_markup
                )
                query.message.delete()
            else:
                query.edit_message_text(
                    text=text,
                    reply_markup=reply_markup
                )
    else:
        query.edit_message_text(text="No words", reply_markup=back_keyboard_markup())


def review_words(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    data = query.data.split('-')
    query.answer()
    if len(data) > 3:
        users_words_create(data[2], data[1], data[3])

    user = get_user_data(query.from_user.id)
    word = get_user_review_word(user.id, data[1] if len(data) > 1 else None)
    
    if word:
        reply_markup = word_keyboard_markup(REVIEW_KEY, word.id, user.id, word.audio)
        text = word.word
        if word.photo:
            if query.message.photo:
                query.edit_message_media(
                    media=InputMediaPhoto(word.photo),
                    caption=text, 
                    reply_markup=reply_markup
                )
            else:
                query.message.reply_photo(
                    photo=word.photo, 
                    caption=text, 
                    reply_markup=reply_markup
                )
                query.message.delete()
            
        else:
            if query.message.photo:
                query.message.reply_text(
                    text=text,
                    reply_markup=reply_markup
                )
                query.message.delete()
            else:
                query.edit_message_text(
                    text=text,
                    reply_markup=reply_markup
                )
    else:
        query.edit_message_text(text="No words", reply_markup=back_keyboard_markup())


def check(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    data = query.data.split('-')

    word_id = data[1]
    word = get_word(word_id)

    query.answer(word.word_translation, show_alert=True)
    

def audio(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    data = query.data.split('-')
    query.answer()

    word_id = data[1]
    word = get_word(word_id)

    query.message.reply_audio(
        audio=word.audio, 
        caption=f"<b>{word.word}</b>\n<i>{word.word_translation}</i>",
    )
    