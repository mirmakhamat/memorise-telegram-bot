from sqlalchemy import Table, Column, Integer, String, MetaData, DateTime, ForeignKey, Enum
import datetime
import enum
meta = MetaData()

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

WordsTable = Table(
    'words', meta,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('word', String),
    Column('word_translation', String),
    Column('photo', String, nullable=True),
    Column('audio', String, nullable=True),


    Column('created_at', DateTime, default=datetime.datetime.now),
    Column('updated_at', DateTime, default=datetime.datetime.now,
           onupdate=datetime.datetime.now)
)


class StatusEnum(enum.Enum):
    know = 1
    learn = 2


UsersWordsTable = Table(
    'users_words', meta,
    Column('id', Integer, primary_key=True, autoincrement=True),

    Column('user_id', Integer, ForeignKey('users.id')),
    Column('word_id', Integer, ForeignKey('words.id')),

    Column('status', Enum(StatusEnum)),

    Column('created_at', DateTime, default=datetime.datetime.now),
    Column('updated_at', DateTime, default=datetime.datetime.now,
           onupdate=datetime.datetime.now)
)
