import argparse
from main import app
from main import alembic
from database import StatusEnum,ModeEnum,db,Hackathon
from datetime import datetime,timedelta
from werkzeug.exceptions import NotFound
import enum


today = datetime.now().replace(microsecond=0)
tommorow = today + timedelta(days=1)
#Refference for Flask Alembic --> https://flask-alembic.readthedocs.io/en/stable/api/    

def current_migrations():
    """
    Gets the list of current migrations.
    (head) is the current version of migration 
    applied to the db while others are previously applied versions of migrations 
    """
    
    with app.app_context():
        migrations = alembic.current()
        print("All Migrations:")
        [print(i) for i in migrations]
        print(f"Current Migration: {migrations[0].revision}")

def migrate():
    """
    Generate a new Alembic migration script based on detected model changes.
    """
    
    with app.app_context():
        alembic.revision("made_changes")

def upgrade():
    """
    Apply all pending migration scripts to the database, bringing its
    schema up to date with the current models.
    """
    
    with app.app_context():
        alembic.upgrade()

def add_row(id=None,name=None,url=None,description=None,startDate=today,endDate=tommorow,location=None,mode=None,organizer=None,hasPrize : bool = None, prizeDetails = None, tags=None,status = None,submittedAt=today,updatedAt=today,interestCount : int = 0):
    
    """"
    Manually add a row in Hackathons table.
    This function was implemented for test purposes only.
    Note: id,name,url are required parameters for the function to work.
    """
    
    if not(id) or not(name) or not(url):
        raise ValueError("Sorry id,name,url params are required.")
    
    if mode is not None: #testing if mode contains one of the desired values
        try:
            mode = ModeEnum(mode)  #converts string "online" to ModeEnum.online
        except ValueError:
            raise ValueError(f"Wrong mode name: {mode}")

    if status is not None: #testing if status contains one of the desired values
        try:
            status = StatusEnum(status)
        except ValueError:
            raise ValueError(f"Wrong status name: {status}")
    
    with app.app_context():
        new_hackathon = Hackathon(id=id,name=name,url=url,description=description,startDate=startDate,endDate=endDate,location=location,mode=mode,
                                  organizer=organizer,hasPrize=hasPrize,prizeDetails=prizeDetails,tags=tags,status=status,
                                  submittedAt=submittedAt,updatedAt=updatedAt,interestCount=interestCount)
        db.session.add(new_hackathon)
        db.session.commit()
        print(f"Successfully added row with an id: {id} , name: {name} , url: {url}.")

def check_constant_value(constant,constantEnum:enum.EnumMeta):
    if constant is not None: #testing if status contains one of the desired values
        try:
            status = constantEnum(status)
        except ValueError:
            raise ValueError(f"Wrong status name: {status}")
    return None

def update_row(id,**kwargs):
    allowed = ["name", "url", "description", "startDate", "endDate", "updatedAt", "submittedAt", "location", "mode",
           "organizer", "hasPrize", "prizeDetails", "tags", "status", "interestCount"]
    
    """"
    Manually update a row in Hackathons table.
    This function was implemented for test purposes only.
    Note: id parameter is required for the function to properly work.
    """
    
    if not(id):
        raise ValueError("Sorry id param is required.")
    
    with app.app_context():
        try:
            hackathon_to_update = db.get_or_404(Hackathon,id) 
            
            for key , value in kwargs.items():
                if key in allowed and value is not None:
                    
                    if key == "mode":
                        try:
                            ModeEnum(value)  #converts string "online" to ModeEnum.online
                        except ValueError:
                            raise ValueError(f"Wrong mode name: {key}")
                        
                    elif key == "status":
                        try:
                            StatusEnum(value)
                        except ValueError:
                            raise ValueError(f"Wrong status name: {key}")
                        
                    setattr(hackathon_to_update, key,value)
                    print(f"Successfully updated {key} with a value of {str(value)}!")
                    #Why are we using setattr() here:
                    #The issue is that hackathon_to_update.key = value sets a literal attribute 
                    # named key on the object,it doesn't use the value of our key variable
                    # To dynamically set an attribute using a variable name, use the setattr() method.

            hackathon_to_update.updatedAt = today
            db.session.commit()

        except NotFound:
            raise ValueError(f"Sorry there is no hackathon with an id: {id} to update.")
            
        
def delete_row(id):
    
    """"
    Manually delete a row in Hackathons table.
    This function was implemented for test purposes only.
    Note: id argument is required for the function to work.
    """
    
    if not(id):
        raise ValueError("Sorry id parameter is required.")
    
    with app.app_context():
        hackathon_to_delete = Hackathon.query.filter_by(id=id).first() #id is unique so .first() doesnt affect anywhere
        db.session.delete(hackathon_to_delete)
        db.session.commit()
        print(f"Successfully deleted row with an id: {id}.")
        
def delete_all_rows():
    
    """"
    Manually delete Hackathons table.
    This function was implemented for test purposes only.
    Note: Later a parameter named 'table_to_delete' will be added
    in order to specify the table that we want to delete.
    For now only Hackathons table exists in our database.
    """
    
    answer = str(input(f"Are you sure you want to delete the WHOLE table? (y/n)").lower())
    if answer == "y":
        with app.app_context():
            Hackathon.query.delete()
            db.session.commit()
        print("Successfully deleted the WHOLE table.")
    
    
def main():
    parser = argparse.ArgumentParser()
    
    parser.add_argument(
        "--migrate",
        action="store_true",
        help="migrate-db") #we add an argument to the parser named --revesion
    
    parser.add_argument(
        "--upgrade",
        action="store_true",
        help="upgrade-db"
    )
    
    parser.add_argument(
        "--current_migrations",
        action="store_true",
        help="current-migrations-db"
    )
    
    parser.add_argument(
        "--add_row",
        action="store_true",
        help="add-a-row-in-the-database"
    )
    
    parser.add_argument(
        "--update_row",
        action="store_true",
        help="add-a-row-in-the-database"
    )
    
    parser.add_argument(
        "--delete_row",
        action="store_true",
        help="delete-a-row-in-the-database"
    )
    
    parser.add_argument(
        "--delete_all_rows",
        action="store_true",
        help="delete-table-in-the-database"
    )
    
    # arguments for add_row
    parser.add_argument("--id", type=str)
    parser.add_argument("--name", type=str)
    parser.add_argument("--url", type=str)
    
    #datetime type is not gonna work so we have to make it str first and then convert it to datetime
    parser.add_argument("--description", type=str, default=None)
    parser.add_argument("--startDate", type=str, default=None,help="Format: YYYY-MM-DD HH:MM:SS")
    parser.add_argument("--endDate", type=str, default=None,help="Format: YYYY-MM-DD HH:MM:SS")
    parser.add_argument("--submittedAt", type=str, default=None)
    parser.add_argument("--updatedAt", type=str, default=None)
    parser.add_argument("--location", type=str, default=None)
    parser.add_argument("--mode", type=str, default=None)
    parser.add_argument("--organizer", type=str, default=None)
    parser.add_argument("--hasPrize", type=lambda x: x.lower() == "true", default=None)
    parser.add_argument("--prizeDetails", type=str, default=None)
    parser.add_argument("--tags", type=str, default=None)
    parser.add_argument("--status", type=str, default=None)
    parser.add_argument("--interestCount", type=int, default=0)
    
    
    args = parser.parse_args() #reads the actual text the user typed after the script name in the terminal
                               #and matches it against all the args that we have defined except (--help)

    startDate = datetime.strptime(args.startDate, "%Y-%m-%d %H:%M:%S") if args.startDate else None
    endDate = datetime.strptime(args.endDate, "%Y-%m-%d %H:%M:%S") if args.endDate else None
    submittedAt = datetime.strptime(args.submittedAt, "%Y-%m-%d %H:%M:%S") if args.submittedAt else None
    updatedAt = datetime.strptime(args.updatedAt, "%Y-%m-%d %H:%M:%S") if args.updatedAt else None
    
    kwargs = {
        "name": args.name,
        "url": args.url,
        "description":args.description,
        "location": args.location,
        "startDate": startDate,
        "endDate": endDate,
        "updatedAt": updatedAt,
        "submittedAt": submittedAt,
        "mode": args.mode,
        "organizer": args.organizer,
        "hasPrize": args.hasPrize,
        "prizeDetails": args.prizeDetails,
        "tags": args.tags,
        "status": args.status,
        "interestCount": args.interestCount,
    }    
    
    if args.delete_all_rows:
        return delete_all_rows()
    
    if args.delete_row:
        return delete_row(id=args.id)
        
    if args.add_row:
        return add_row(
            id=args.id, name=args.name, url=args.url,description=args.description,
            startDate=startDate, endDate=endDate,
            updatedAt=today,submittedAt=today,
            location=args.location, mode=args.mode, organizer=args.organizer,
            hasPrize=args.hasPrize, prizeDetails=args.prizeDetails, tags=args.tags,
            status=args.status, interestCount=args.interestCount
        )
    
    if args.update_row:
        return update_row(id=args.id,**kwargs)
    
    if args.migrate: #if args.wipe doesnt exist it returns None and if gets skipped 
        return migrate()
    
    if args.upgrade:
        return upgrade()
    
    if args.current_migrations:
        return current_migrations()
    
    return
    

if __name__ == "__main__":
    main()    