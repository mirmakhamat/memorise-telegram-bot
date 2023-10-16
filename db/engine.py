import os
DB_URL = os.getenv('DB_URL')

import sqlalchemy as db
engine = db.create_engine(DB_URL)
