from telegram import Update, InputMediaPhoto
from telegram.ext import CallbackContext, ConversationHandler
from bot.keyboards.word import word_keyboard_markup, back_keyboard_markup, confirm_keyboard_markup, REVIEW_KEY, WORD_KEY
from db.functions.word import get_user_word, users_words_create, get_user_review_word, get_word, get_word_examples, create_word,update_word
from db.functions.user import get_user_data, get_user_today_words
from bot import states

def update_words(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    data = query.data.split('-')
    query.answer()

    user_today_words = get_user_today_words(query.from_user.id)
    if len(user_today_words) == 10:
        query.edit_message_text(
            text="You have already 10 words today",
            reply_markup=back_keyboard_markup()
        )
        return

    if len(data) > 3:
        users_words_create(data[2], data[1], data[3])

    user = get_user_data(query.from_user.id)
    word = get_user_word(user.id)

    if word:
        reply_markup = word_keyboard_markup(
            WORD_KEY, word.id, user.id, word.audio)
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
        query.edit_message_text(
            text="No words", reply_markup=back_keyboard_markup())


def review_words(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    data = query.data.split('-')
    query.answer()
    if len(data) > 3:
        users_words_create(data[2], data[1], data[3])

    user = get_user_data(query.from_user.id)
    word = get_user_review_word(user.id, data[1] if len(data) > 1 else None)

    if word:
        reply_markup = word_keyboard_markup(
            REVIEW_KEY, word.id, user.id, word.audio)
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
                    reply_markup=reply_markup,
                    api_kwargs={"has_spoiler": True}
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
        query.edit_message_text(
            text="No words", reply_markup=back_keyboard_markup())


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


def example(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    data = query.data.split('-')
    query.answer()

    word_id = data[1]
    examples = get_word_examples(word_id)
    word = get_word(word_id)
    text = f"{word.word}"
    for example in examples:
        text += f"\n\n{example.example}\n<tg-spoiler>{example.example_translation}</tg-spoiler>"

    query.edit_message_text(
        text=text,
        parse_mode="HTML",
    )


def add_word(update: Update, context: CallbackContext) -> None:
    reply_markup = confirm_keyboard_markup()
    text = update.message.text
    if update.message.photo:
        text = update.message.caption
    if len(text.split('\n')) != 2:
        update.message.reply_text(
            text="Invalid format"
        )
        return
    update.message.copy(update.effective_chat.id, reply_markup=reply_markup)


def add_new_word(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    text = query.message.text
    photo = None
    if query.message.photo:
        text = query.message.caption
        photo = query.message.photo[-1].file_id

    word, word_translation = text.split('\n')
    
    word_id = create_word(word, word_translation, photo)

    query.edit_message_text(
        text="Muvafaqqiyatli qo'shildi\n\nAgar mavjud bo'lsa audio yuboring, bo'lmasa /skip yuboring",
    )
    context.user_data['word_id'] = word_id

    return states.AUDIO

def add_audio(update: Update, context: CallbackContext) -> None:
    audio = update.message.audio.file_id
    update_word(context.user_data['word_id'], audio=audio)
    update.message.reply_text(text="Audio qo'shildi.")
    return ConversationHandler.END