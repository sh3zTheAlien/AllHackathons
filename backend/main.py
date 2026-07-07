from flask import Flask,jsonify
from database import db,Hackathon
from flask_alembic import Alembic
import os

db_dir = os.path.abspath("./db")
os.makedirs(db_dir,exist_ok=True)

app = Flask(__name__,instance_path=db_dir)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///hackathon.db"
db.init_app(app)

alembic = Alembic()
alembic.init_app(app) 

with app.app_context():
    db.create_all()
    
@app.route("/",methods=['GET']) #future api/hackathons endpoint
def hackathons():
    try:
        hackathons_query = db.session.execute(db.select(Hackathon))
        hackathons = hackathons_query.scalars().all()
    except LookupError: #in case mode or status dont contain a constant value
        return jsonify({"error": "One or more records contain an invalid mode/status value"}), 500
    return jsonify([hackathon.to_dict() for hackathon in hackathons])


@app.route("/health")
def health():
    return "Healthy!\n"


@app.route("/ping")
def ping():
    return "Pong!\n"


if __name__ == '__main__':
    app.run(debug=True)
