from sqlalchemy.orm import sessionmaker
from db.engine import engine
from db.table import WordsTable, UsersWordsTable
from sqlalchemy.sql.expression import func, select


def get_user_word(user_id):
    # Return new word for user with user_id
    # If there is no new word for user, return None

    Session = sessionmaker(bind=engine)
    session = Session()
    subquery = session.query(UsersWordsTable.word_id).filter(
        UsersWordsTable.user_id == user_id).subquery()
    result = session.query(WordsTable).filter(
        WordsTable.id.not_in(subquery)).order_by(func.random()).first()
    return result if result else None
