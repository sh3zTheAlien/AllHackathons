from flask import Flask,jsonify,request
from database import db,Hackathon,ModeEnum,StatusEnum
from flask_alembic import Alembic
from werkzeug.exceptions import NotFound
from datetime import datetime,timedelta
import os

today = datetime.now().replace(microsecond=0)
tommorow = today + timedelta(days=1)

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
    if request.method == "POST":
        #params
        id = request.form.get("id")
        name = request.form.get("name")
        url = request.form.get("url")
        description = request.form.get("description")
        organizer = request.form.get("organizer")
        status = request.form.get("status")
        mode = request.form.get("mode")
        tags = request.form.get("tags")
        startDate = datetime.strptime(request.form.get("startDate"), "%Y-%m-%d %H:%M:%S")
        endDate = datetime.strptime(request.form.get("endDate"), "%Y-%m-%d %H:%M:%S")
        location = request.form.get("location")
        hasPrize = request.form.get("hasPrize")
        prizeDetails = request.form.get("prizeDetails")
        submittedAt = today
        updatedAt = today
        interestCount = 0
        print(f"The type of startDate is: {type(startDate)}")
        #params validation
        if not(id) or not(name) or not(url):
            return jsonify(error={"Missing Fields": "name and url are required."}),400
        
        if mode is not None: #testing if mode contains one of the desired values
            try:
                mode = ModeEnum(mode)  #converts string "online" to ModeEnum.online
            except ValueError:
                #raise ValueError(f"Wrong mode name: {mode}")
                return jsonify(error={f"Wrong mode name: {mode}"}),400

        if status is not None: #testing if status contains one of the desired values
            try:
                status = StatusEnum(status)
            except ValueError:
                return jsonify(error={f"Wrong status name: {status}"}),400
        
        with app.app_context():
            new_hackathon = Hackathon(id=id,name=name,url=url,description=description,startDate=startDate,endDate=endDate,location=location,mode=mode,
                                    organizer=organizer,hasPrize=hasPrize,prizeDetails=prizeDetails,tags=tags,status=status,
                                    submittedAt=submittedAt,updatedAt=updatedAt,interestCount=interestCount)
            db.session.add(new_hackathon)
            db.session.commit()
        return jsonify(response={"success":f"Successfully added hackathon:{name}!"}), 200
    
    elif request.method == "GET":
        now = datetime.now().replace(microsecond=0) #Formats time like this: YYYY-MM-DD HH:MM:SS example: 2026-05-01 15:12:00
        
        params = {
            "status" : request.args.get('status'),
            "upcoming" : request.args.get('upcoming'),
            "past" : request.args.get('past'),
            "tags" : request.args.get('tags'),
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
            query = query.filter(Hackathon.startDate > now)
        elif params["upcoming"] == "false":
            query = query.filter(Hackathon.startDate < now)
        elif params["upcoming"]:
            return jsonify(error={"Hackathon Not Found": f"Sorry, there is no hackathon with an upcoming value of {params["upcoming"]}. "f"Available parameters for upcoming are: ?upcoming= ('true' | 'false')"}), 404
        
        #past parameter    
        if params["past"] == "true":
            query = query.filter(Hackathon.startDate < now)
        elif params["past"] == "false":
            query = query.filter(Hackathon.startDate > now)
        elif params["past"]:
            return jsonify(error={"Hackathon Not Found": f"Sorry, there is no hackathon with an upcoming value of {params["upcoming"]}. "f"Available parameters for past are: ?past= ('true' | 'false')"}), 404
        
        #tags parameter
        if params["tags"]:
            query = query.filter(Hackathon.tags == params["tags"])
        
        #q parameter will be added later
        # if params["q"]:
        #     query = query.filter(Hackathon.name == params["q"])
        
        #sort parameter
        if params["sort"]:
            if params["sort"] == "name":
                query = query.order_by(Hackathon.name)
            elif params["sort"] == "startDate":
                query = query.order_by(Hackathon.startDate)
            elif params["sort"] == "endDate":
                query = query.order_by(Hackathon.endDate)
            elif params["sort"] == "sumbittedAt":
                query = query.order_by(Hackathon.submittedAt)
            elif params["sort"] == "updatedAt":
                query = query.order_by(Hackathon.updatedAt)
            elif params["sort"] == "interestCount":
                query = query.order_by(Hackathon.interestCount)
                
        results = query.all()
        return [result.to_dict() for result in results]
        
        #if no param passed all hackathons get returned
        try:
            hackathons_query = db.session.execute(db.select(Hackathon))
            hackathons = hackathons_query.scalars().all()
        except LookupError: #in case mode or status doesnt contain a constant value
            return jsonify({"error": "One or more records contain an invalid mode/status value"}), 500
        return jsonify([hackathon.to_dict() for hackathon in hackathons])

@app.route("/api/hackathons/<hackathon_id>",methods=['GET'])
def find_hackathon(hackathon_id):
    try:
        hackathon = db.get_or_404(Hackathon, hackathon_id)
        return jsonify(hackathon.to_dict())
    except NotFound:
        return jsonify(error={"Hackathon Not Found":f"Sorry, there is no hackathon with an id of {hackathon_id}."}),404