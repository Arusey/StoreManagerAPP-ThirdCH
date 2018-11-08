from app import create_app
from app.api.v2.models.databaseModel import Db
app = create_app("development")
db_obj = Db()
db_obj.create_tables()
if __name__ ==  '__main__':
    app.run()
