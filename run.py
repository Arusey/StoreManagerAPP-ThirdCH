from app import create_app
from app.api.v2.models.databaseModel import Db
app = create_app("development")
@app.route("/")
def index():
    return "<h1>find the app documentation</h1><a href='https://documenter.getpostman.com/view/4790487/RzZ4q21V'>here</a></p>"
if __name__ ==  '__main__':
    app.run()
