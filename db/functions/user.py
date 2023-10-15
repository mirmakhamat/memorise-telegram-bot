from db.table import UsersTable
from db.engine import engine


def register(telegram_id, first_name, last_name):
    """
    Register a user in the database
    """
    try:
        statement = UsersTable.insert().values(telegram_id=telegram_id,
                                               first_name=first_name, last_name=last_name)
        with engine.connect() as connection:
            connection.execute(statement)
            connection.commit()
    except Exception as e:
        print(e)
