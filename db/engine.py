import sqlalchemy as db
engine = db.create_engine(
    'postgresql+psycopg2://postgres:postgres@localhost:5432/memorise')
