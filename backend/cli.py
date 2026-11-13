import click
from main import app
from database import db, Administrators, SuperAdmin
from sqlalchemy import select, exists
from datetime import datetime
from argon2 import PasswordHasher


def is_superadmin(superadmin_password):
    try:
        superadmin_hashed_password = SuperAdmin.query.first().password
        ph = PasswordHasher()
        is_superadmin = ph.verify(superadmin_hashed_password, superadmin_password)
        return True , None
    except Exception as e:
        return False , str(e)
    
def superadmin_table_is_empty():
    is_empty =  True if db.session.query(SuperAdmin).first() is None else False
    return is_empty

@app.cli.command("list-admins")
def list_admins():
	all_admins = Administrators.query.all()
 
	if not all_admins: #all_admins return an empty list if there are no admins in the database
		return click.echo("No admins found.")

	click.echo("Username | Email | Joined | Last Login | Hackathons Approved | Hackathons Rejected | Request Status \n")
	for admin in all_admins:
		click.echo(f"{admin.username} | {admin.email} | {admin.joined} | {admin.last_login} | {admin.hackathons_approved} | {admin.hackathons_rejected} | {admin.request_status.value} \n")

@app.cli.command("create-superadmin")
@click.argument("username", required=True, help="The username of the super admin.")
@click.argument("email", required=True, help="The email of the super admin.")
@click.argument("password", required=True, help="The password of the super admin.")
def create_superadmin(username,email,password):
    
	if not superadmin_table_is_empty(): #then there is a record so someone is already a superadmin
		return click.echo("A super admin already exists.")

	ph = PasswordHasher()
	hashed_password = ph.hash(password)
	new_superadmin = SuperAdmin(username=username, email=email, password=hashed_password, 
                               joined=datetime.now(),last_login=datetime.now())

	try:
		db.session.add(new_superadmin)
		db.session.commit()
		click.echo(f"Super Admin '{username}' created successfully.")
	except Exception as e:
		click.echo(f"Error creating super admin: {e}")


@app.cli.command("create-admin")
@click.argument("username", required=True, help="The username of the new admin.")
@click.argument("email", required=True, help="The email of the new admin.")
@click.argument("password", required=True, help="The password of the new admin.")
def create_admin(username,email,password):
    
    password = click.prompt("Please enter the super admin password to authorize this action", hide_input=True)
    result , error = is_superadmin(password)
    if not result:
        return click.echo(f"Authorization failed. Only super admins can create new admins. Error: {error}")
    #print(is_superadmin(password))
    
    #is_superadmin() will be called here to check if the user is a superadmin before creating a new admin.
    ph = PasswordHasher()
    hashed_password = ph.hash(password)
    new_admin = Administrators(username=username, email=email, password=hashed_password, 
                               joined=datetime.now(),last_login=datetime.now())

    try:
        db.session.add(new_admin)
        db.session.commit()
        click.echo(f"Admin '{username}' created successfully.")
    except Exception as e:
        click.echo(f"Error creating admin: {e}")