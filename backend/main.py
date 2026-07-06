from flask import Flask
from database import db

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///hackathon.db"
db.init_app(app)

with app.app_context():
    db.create_all()


@app.route("/health")
def health():
    return "Healthy!\n"


@app.route("/ping")
def ping():
    return "Pong!\n"
