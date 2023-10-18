from sqlalchemy.orm import sessionmaker
from db.engine import engine
from db.table import WordsTable, UsersWordsTable, StatusEnum, ExamplesTable
from sqlalchemy.sql import func
import datetime


def get_user_word(user_id):
    Session = sessionmaker(bind=engine)
    session = Session()
    subquery = session.query(UsersWordsTable.word_id).filter(
        UsersWordsTable.user_id == user_id).subquery()
    result = session.query(WordsTable).filter(
        WordsTable.id.not_in(subquery)).order_by(func.random()).first()
    return result if result else None


def get_user_review_word(user_id, word_id=None):
    Session = sessionmaker(bind=engine)
    session = Session()
    current_day = datetime.date.today()
    subquery = session.query(UsersWordsTable.word_id).filter(
        UsersWordsTable.user_id == user_id,
        UsersWordsTable.word_id != word_id,
        UsersWordsTable.status == StatusEnum.learn,
        func.date_trunc('day', UsersWordsTable.updated_at) != current_day
    ).subquery()
    result = session.query(WordsTable).filter(
        WordsTable.id.in_(subquery)).order_by(func.random()).first()
    return result if result else None


def users_words_create(user_id, word_id, status):
    Session = sessionmaker(bind=engine)
    session = Session()
    word = session.query(UsersWordsTable).filter(
        UsersWordsTable.user_id == user_id,
        UsersWordsTable.word_id == word_id
    ).first()
    if word:
        if word.count < 3:
            if status == "1":
                word.count += 1
        else:
            word.status = StatusEnum(int(status))

    else:
        userswords = UsersWordsTable(user_id=user_id, word_id=word_id, status=StatusEnum(2))
        session.add(userswords)

    session.commit()

def get_word(word_id):
    Session = sessionmaker(bind=engine)
    session = Session()
    result = session.query(WordsTable).filter(WordsTable.id == word_id).first()
    return result if result else None


def get_word_examples(word_id):
    Session = sessionmaker(bind=engine)
    session = Session()
    result = session.query(ExamplesTable).filter(ExamplesTable.word_id == word_id).all()
    return result


def create_word(word, word_translation, photo=None, audio=None):
    Session = sessionmaker(bind=engine)
    session = Session()
    word = WordsTable(word=word, word_translation=word_translation, photo=photo, audio=audio)
    session.add(word)
    session.flush()
    session.commit()

    return word.id

def update_word(word_id, word=None, word_translation=None, photo=None, audio=None):
    Session = sessionmaker(bind=engine)
    session = Session()
    word = session.query(WordsTable).filter(WordsTable.id == word_id).first()
    if word:
        word.word = word
    if word_translation:
        word.word_translation = word_translation
    if photo:
        word.photo = photo
    if audio:
        word.audio = audio

    session.commit()
    