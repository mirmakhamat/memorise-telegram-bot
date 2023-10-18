import os
import dotenv
dotenv.load_dotenv()

DB_URL = os.getenv('DB_URL')

import sqlalchemy as db
engine = db.create_engine(DB_URL)
