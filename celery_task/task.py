from flask import Flask
from celery import Celery
from pymongo import MongoClient

app = Flask(__name__)
MONGODB_URL = "mongodb://localhost:27017/"
DB_NAME = "my_cel_db"

MONGODB_CON_STR = "{}{}".format(MONGODB_URL, DB_NAME)

# app.config['CELERY_RESULT_BACKEND'] = MONGODB_CON_STR
db = MongoClient(MONGODB_URL)[DB_NAME]

celery = Celery(app.name, broker='amqp://localhost:5672//')


@app.route('/')
def add_nums():
    add_num.delay()
    return "Done"


@celery.task()
def add_num():
    # with app.app_context():
    for i in range(50, 80):
        res = f"Hello={i}"
        db.results.insert_one({"res": res})
    return "Task Done"


if __name__ == '__main__':
    app.run(debug=True)
