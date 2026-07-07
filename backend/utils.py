import argparse
from main import app
from main import alembic

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
    
    args = parser.parse_args() #reads the actual text the user typed after the script name in the terminal
                               #and matches it against all the args that we have defined except (--help)
    if args.migrate: #if args.wipe doesnt exist it returns None and if gets skipped 
        return migrate()
    
    if args.upgrade:
        return upgrade()
    
    if args.current_migrations:
        return current_migrations()
    
    return
    

if __name__ == "__main__":
    main()    