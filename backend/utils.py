import argparse
from main import app
from main import alembic
from database import StatusEnum,ModeEnum,db,Hackathon
from datetime import datetime,timedelta
from werkzeug.exceptions import NotFound


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

def add_row(id=None,name=None,url=None,startDate=today,endDate=tommorow,location=None,mode=None,organizer=None,hasPrize : bool = None, prizeDetails = None, tags=None,status = None,submittedAt=today,updatedAt=today,interestCount : int = 0):
    
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
        new_hackathon = Hackathon(id=id,name=name,url=url,startDate=startDate,endDate=endDate,location=location,mode=mode,
                                  organizer=organizer,hasPrize=hasPrize,prizeDetails=prizeDetails,tags=tags,status=status,
                                  submittedAt=submittedAt,updatedAt=updatedAt,interestCount=interestCount)
        db.session.add(new_hackathon)
        db.session.commit()
        print(f"Successfully added row with an id: {id} , name: {name} , url: {url}.")

def update_row(id,name=None,url=None,startDate=None,endDate=None,location=None,mode=None,organizer=None,hasPrize : bool = None, prizeDetails = None, tags=None,status = None,updatedAt=today,interestCount : int = None):
    
    """"
    Manually update a row in Hackathons table.
    This function was implemented for test purposes only.
    Note: id is require for the function to properly work.
    """
    
    if not(id):
        raise ValueError("Sorry id param is required.")
    
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
        try:
            hackathon_to_update = db.get_or_404(Hackathon,id) #id is unique so .first() doesnt affect anywhere
            hackathon_to_update.name = name if name is not None else hackathon_to_update.name
            hackathon_to_update.url = url if url is not None else hackathon_to_update.url
            hackathon_to_update.startDate = startDate if startDate is not None else hackathon_to_update.startDate
            hackathon_to_update.endDate = endDate if endDate is not None else hackathon_to_update.endDate
            hackathon_to_update.location = location if location is not None else hackathon_to_update.location
            hackathon_to_update.mode = mode
            hackathon_to_update.organizer = organizer if organizer is not None else hackathon_to_update.organizer
            hackathon_to_update.hasPrize = hasPrize if hasPrize is not None else hackathon_to_update.hasPrize
            hackathon_to_update.prizeDetails = prizeDetails if prizeDetails is not None else hackathon_to_update.prizeDetails
            hackathon_to_update.tags = tags if tags is not None else hackathon_to_update.tags
            hackathon_to_update.status = status
            hackathon_to_update.interestCount = interestCount if interestCount is not None else hackathon_to_update.interestCount
            db.session.commit()
            print(f"Successfully updated row with an id: {id}.")
            
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

    startDate = datetime.strptime(args.startDate, "%Y-%m-%d %H:%M:%S") if args.startDate else today
    endDate = datetime.strptime(args.endDate, "%Y-%m-%d %H:%M:%S") if args.endDate else tommorow
    if args.submittedAt: 
        submittedAt = datetime.strptime(args.submittedAt, "%Y-%m-%d %H:%M:%S") 
    
    if args.updatedAt:
        updatedAt = datetime.strptime(args.updatedAt, "%Y-%m-%d %H:%M:%S")  
    
    if args.delete_all_rows:
        return delete_all_rows()
    
    if args.delete_row:
        return delete_row(id=args.id)
        
    if args.add_row:
        return add_row(
            id=args.id, name=args.name, url=args.url,
            startDate=startDate, endDate=endDate,
            updatedAt=today,submittedAt=today,
            location=args.location, mode=args.mode, organizer=args.organizer,
            hasPrize=args.hasPrize, prizeDetails=args.prizeDetails, tags=args.tags,
            status=args.status, interestCount=args.interestCount
        )
    
    if args.update_row:
        return update_row(
            id=args.id,name=args.name,url=args.url,
            startDate=startDate, endDate=endDate,updatedAt=today,
            location=args.location, mode=args.mode, organizer=args.organizer,
            hasPrize=args.hasPrize, prizeDetails=args.prizeDetails, tags=args.tags,
            status=args.status,interestCount=args.interestCount)
    
   
    if args.migrate: #if args.wipe doesnt exist it returns None and if gets skipped 
        return migrate()
    
    if args.upgrade:
        return upgrade()
    
    if args.current_migrations:
        return current_migrations()
    
    return
    

if __name__ == "__main__":
    main()    