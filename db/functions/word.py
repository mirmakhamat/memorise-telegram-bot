from sqlalchemy.orm import sessionmaker
from db.engine import engine
from db.table import WordsTable, UsersWordsTable, StatusEnum
from sqlalchemy.sql.expression import func


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
    subquery = session.query(UsersWordsTable.word_id).filter(
        UsersWordsTable.user_id == user_id,
        UsersWordsTable.status == StatusEnum.learn,
        UsersWordsTable.word_id != word_id
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
        word.status = StatusEnum(int(status))

    else:
        userswords = UsersWordsTable(user_id=user_id, word_id=word_id, status=StatusEnum(int(status)))
        session.add(userswords)

    session.commit()

def get_word(word_id):
    Session = sessionmaker(bind=engine)
    session = Session()
    result = session.query(WordsTable).filter(WordsTable.id == word_id).first()
    return result if result else None


def add_word(word, word_translation, photo=None, audio=None):
    Session = sessionmaker(bind=engine)
    session = Session()

    session.add(WordsTable(word=word, word_translation=word_translation, photo=photo, audio=audio))
    session.commit()