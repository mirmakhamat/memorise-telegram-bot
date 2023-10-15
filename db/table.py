from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, String, MetaData, DateTime, ForeignKey, Enum
import datetime
import enum
meta = MetaData()
Base = declarative_base()

UsersTable = Table(
    'users', meta,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('first_name', String),
    Column('last_name', String),
    Column('telegram_id', Integer, unique=True),
    Column('created_at', DateTime, default=datetime.datetime.now),
    Column('updated_at', DateTime, default=datetime.datetime.now,
           onupdate=datetime.datetime.now)
)


class WordsTable(Base):
    __tablename__ = 'words'

    id = Column(Integer, primary_key=True, autoincrement=True)
    word = Column(String)
    word_translation = Column(String)
    photo = Column(String, nullable=True)
    audio = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, default=datetime.datetime.now,
                        onupdate=datetime.datetime.now)


class StatusEnum(enum.Enum):
    know = 1
    learn = 2


class UsersWordsTable(Base):
    __tablename__ = 'users_words'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    word_id = Column(Integer, ForeignKey('words.id'))
    status = Column(Enum(StatusEnum))
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, default=datetime.datetime.now,
                        onupdate=datetime.datetime.now)
