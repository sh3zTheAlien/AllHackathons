from flask import Flask,jsonify,request
from database import db,Hackathon,ModeEnum,StatusEnum
from flask_alembic import Alembic
from werkzeug.exceptions import NotFound
from datetime import datetime
import os

db_dir = os.path.abspath("./db")
os.makedirs(db_dir,exist_ok=True)

app = Flask(__name__,instance_path=db_dir)
app.json.sort_keys = False #prevents alphabetical order when json is returned
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///hackathon.db"
app.config['ALEMBIC_RENDER_AS_BATCH'] = True
db.init_app(app)

alembic = Alembic()
alembic.init_app(app) 

with app.app_context():
    db.create_all()
    
@app.route("/",methods=['GET','POST']) #future api/hackathons endpoint
def hackathons():
    params = {
        "status" : request.args.get('status'),
        "upcoming" : request.args.get('upcoming'),
        "past" : request.args.get('past'),
        "tag" : request.args.get('tag'),
        "q" : request.args.get('q'),
        "sort" : request.args.get('sort')
    }
    
    query = db.session.query(Hackathon) # Arxiko query pou kanei build up stin sinexeia
                                        # me vasi ta params pou exoun epistrafei
        
    #status parameter
    if params["status"]:
        if (params["status"] in (StatusEnum.draft.value, StatusEnum.pending.value, StatusEnum.published.value, StatusEnum.needs_changes.value)):
            query = query.filter(Hackathon.status == params["status"])
        else:
            return jsonify(error={"Hackathon Not Found": f"Sorry, there is no hackathon with a status of {params['status']}. "f"Available parameters for status are: ?status= ('draft' | 'pending' | 'published' | 'needs-changes')"}), 404
    
    #upcoming parameter fix Hackathon.startDate comparing value
    if params["upcoming"] == "true":
        query = query.filter(Hackathon.startDate > datetime.now().replace(microsecond=0))
    elif params["upcoming"] == "false":
        query = query.filter(Hackathon.startDate < datetime.now().replace(microsecond=0))
    elif params["upcoming"]:
        return jsonify(error={"Hackathon Not Found": f"Sorry, there is no hackathon with a status of {params['status']}. "f"Available parameters for upcoming are: ?upcoming= ('true' | 'false')"}), 404
    
    # #past parameter    
    # if params["past"]:
    #     query = query.filter(Hackathon.start_date < datetime.now())
        
    results = query.all()
    return [result.to_dict() for result in results]
    
    try:
        hackathons_query = db.session.execute(db.select(Hackathon))
        hackathons = hackathons_query.scalars().all()
    except LookupError: #in case mode or status doesnt contain a constant value
        return jsonify({"error": "One or more records contain an invalid mode/status value"}), 500
    return jsonify([hackathon.to_dict() for hackathon in hackathons])

@app.route("/api/hackathons/<int:hackathon_id>",methods=['GET'])
def find_hackathon(hackathon_id):
    try:
        hackathon = db.get_or_404(Hackathon, hackathon_id)
        return jsonify(hackathon.to_dict())
    except NotFound:
        return jsonify(error={"Hackathon Not Found":f"Sorry, there is no hackathon with an id of {hackathon_id}."}),404

@app.route("/health")
def health():
    return "Healthy!\n"


@app.route("/ping")
def ping():
    return "Pong!\n"