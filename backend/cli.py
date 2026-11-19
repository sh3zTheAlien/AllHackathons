import click
import json
from main import app, validate_parameters2
from database import db, Hackathon ,Admin, SuperAdmin
from sqlalchemy import select, exists
from datetime import datetime
from argon2 import PasswordHasher

#maybe we can a supeadmin exists decorator
#try to use option in the feature: https://www.google.com/search?q=what+is+the+difference+between+click.argument+and+click.option+in+click+python&sxsrf=AKL5yDihVIj1JbVTcLD-ZXjoF5pirQuC-A%3A1794828373717&udm=50&vsint=&aep=1&ntc=1&cs=1&mstk=AUtExfAtPnrXwgRPPFTiGtCbkRiiK7B2haRaFw4m0Emf2Hin8qheUE2hGlMvggEZm_v63RSc8uniCFUWtXfGjUR41wAeghL1f7c5LAbcsn-VcaXbb_quldXRUX-XczKwqxgx2HZtd1UsyFV7jxqzjRRwPoVsRXFsP2Nb5C15BTq-VSu47f-GNm_okwOo8ksqfeHdMf00IeYdiZv4U7Krra5vpFmPubLkxRulVej8BS31XlIlahZd8WPvZeIGPA&csuir=1

def is_superadmin(superadmin_password_given,superadmin_username_given=None):
    
    superadmin = SuperAdmin.query.first()
    superadmin_actual_name = superadmin.username
    superadmin_actual_password = superadmin.password
    
    if superadmin_username_given and not(superadmin_username_given == superadmin_actual_name):
        return False , "Superadmin Username does not match"
        
    try:
        ph = PasswordHasher()
        is_superadmin = ph.verify(superadmin_actual_password, superadmin_password_given)
        return True , None
    except Exception as e:
        return False , str(e)
    
def is_admin(admin_name:str,admin_password:str):
    
    admin_name2 = Admin.query.filter_by(username=admin_name).first()
    if not admin_name2:
        return False , "Admin not found."
    
    ph = PasswordHasher()
    admin_hashed_password = admin_name2.password
    
    try:
        is_admin = ph.verify(admin_hashed_password, admin_password)
        return True , admin_name2
    except Exception as e:
        return False, str(e)
    
def authenticate_admins():
    
	#TODO: Later implement another func that will update each admins'stats 

	# Making sure that the user is one of the admins
	admin_username = click.prompt("Please enter your admin username", type=str)
	admin_password = click.prompt("Please enter your admin password", hide_input=True)
	
	is_valid_superadmin , superadmin_result = is_superadmin(admin_password,admin_username)
	is_valid_admin , admin_result = is_admin(admin_username,admin_password)

	if (not is_valid_superadmin) and (not is_valid_admin):
		click.echo(f"Authorization failed. Error {admin_result}")
		return False

	click.echo(f"Authorization succeed, you are logged in as {admin_username}")
	return True
    
def superadmin_table_is_empty():
    is_empty =  True if db.session.query(SuperAdmin).first() is None else False
    return is_empty

@app.cli.command("list-admins")
def list_admins():
	all_admins = Admin.query.all()
	
	#Checking if all_admins are empty or not
	if not all_admins: 
		return click.echo("No admins found.")

	click.echo("Username | Email | Joined | Last Login | Hackathons Approved | Hackathons Rejected | Request Status \n")
	for admin in all_admins:
		click.echo(f"{admin.username} | {admin.email} | {admin.joined} | {admin.last_login} | {admin.hackathons_approved} | {admin.hackathons_rejected} | {admin.request_status.value} \n")

@app.cli.command("create-superadmin")
@click.argument("username", required=True, help="The username of the super admin.")
@click.argument("email", required=True, help="The email of the super admin.")
@click.argument("password", required=True, help="The password of the super admin.")
def create_superadmin(username,email,password):
    
    # Checking if a superadmin already exists by verifying if the superadmin table is empty or not
	if not superadmin_table_is_empty():
		return click.echo("A super admin already exists.")

	# Hash the password and create a new superadmin instance
	ph = PasswordHasher()
	hashed_password = ph.hash(password)
	new_superadmin = SuperAdmin(username=username, email=email, password=hashed_password, 
                               joined=datetime.now(),last_login=datetime.now())

	try:
		# Add the new superadmin instance to the database
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
    
    """
    Accessibility: Only SuperAdmin
    """
    
    # Validating if user is a superadmin by veryfying his password
    super_admin_password = click.prompt("Please enter the super admin password to authorize this action", hide_input=True)
    result , error = is_superadmin(super_admin_password,None)
    if not result: #result can only be False or True
        return click.echo(f"Authorization failed. Only super admins can create new admins. Error: {error}")

 	# Hash the password and create a new admin instance
    ph = PasswordHasher()
    hashed_password = ph.hash(password)
    new_admin = Admin(username=username, email=email, password=hashed_password, 
                               joined=datetime.now(),last_login=datetime.now())

    try:
        db.session.add(new_admin)
        db.session.commit()
        click.echo(f"Admin '{username}' created successfully.")
    except Exception as e:
        click.echo(f"Error creating admin: {e}")
        
@app.cli.command("update-admin")
@click.argument("username", required=True, help="The username of the admin that you want to update.")
@click.argument("email", required=True, help="The email of the admin that you want to update.")
def update_admin(username,email):
    
    """
    Accessibility: Only SuperAdmin
    """
    
    # Validating if user is a superadmin by veryfying his password
    ph = PasswordHasher()
    super_password = click.prompt("Please enter the super admin password to authorize this action", hide_input=True)
    result , error = is_superadmin(super_password)
    if not result:
        return click.echo(f"Authorization failed. Only super admins can update admins. Error: {error}")

	# Fetch the admin to update
    admin_to_update = Admin.query.filter_by(username=username, email=email).first()
    
	# Prompt superadmin to set new credentials for the admin he wants to update
    new_username = click.prompt("Please enter the new username for the admin or press - to keep the current one", type=str)
    new_username = None if new_username == "-" else new_username
    new_email = click.prompt("Please enter the new email for the admin or press - to keep the current one", type=str)
    new_email = None if new_email == "-" else new_email
    new_password = click.prompt("Please enter the new password for the admin or press - to keep the current one", hide_input=False, type=str)
    new_password = None if new_password == "-" else ph.hash(new_password)

    try:
		# Pass the new credentials for the admin to update
        admin_to_update.username = new_username if new_username else admin_to_update.username
        admin_to_update.email = new_email if new_email else admin_to_update.email
        admin_to_update.password = new_password if new_password else admin_to_update.password
        
        db.session.commit()
        click.echo(f"Admin '{username}' updated successfully.")
    except Exception as e:
        click.echo(f"Error updating admin: {e}")
        
@app.cli.command("delete-admin")
@click.argument("username", required=True, help="The username of the admin that you want to delete.")
@click.argument("email", required=True, help="The email of the admin that you want to delete.")
def delete_admin(username,email):
    
    """
    Accessibility: Only SuperAdmin
    """
    
    # Validating if user is a superadmin by veryfying his password
    ph = PasswordHasher()
    super_admin_password = click.prompt("Please enter the super admin password to authorize this action", hide_input=True)
    result , error = is_superadmin(super_admin_password)
    if not result:
        return click.echo(f"Authorization failed. Only super admins can delete admins. Error: {error}")

	# Fetch the admin to delete
    admin_to_delete = Admin.query.filter_by(username=username, email=email).first()

    try:
		# Delete the admin from the database
        db.session.delete(admin_to_delete)
        db.session.commit()
        click.echo(f"Admin '{username}' deleted successfully.")
    except Exception as e:
        click.echo(f"Error deleting admin: {e}")
        
        
@app.cli.command("list-all-hackathons")
def list_all_hackathons():
    
    """
    Accessibility: All users
    This function is going to list all hacthons stored in the db.
    For now many fields will not be displayed but we might add them
    later in case this is needed.
    """
    
    #Fetching all hackathons from the database
    all_hackathons = db.session.query(Hackathon).all()
    
    # Checking if all_hackathons are empty or not (all_hackathons is a python list of Hackathon objects)
    if not all_hackathons:
        return click.echo("No hackathons found.")
    
    # Displaying the hackathons in a tabular format
    click.echo("Hackathon Name | Description | URL | Start Date | End Date | Status \n")
    for hackathon in all_hackathons:
        click.echo(f"{hackathon.name} | {hackathon.description} | {hackathon.url} | {hackathon.startDate} | {hackathon.endDate} | {hackathon.status.value} \n")

@app.cli.command("add-hackathon")
@click.option("--name", required=True, help="The name of the hackathon.")
@click.option("--url", required=True, help="The URL of the hackathon.")
@click.option("--description", required=False, help="The description of the hackathon.")
@click.option("--startDate","startDate" , default=None, required=False, help="The start date of the hackathon.")
@click.option("--endDate", "endDate",default=None, required=False, help="The end date of the hackathon.")
@click.option("--location", required=False, help="The location of the hackathon.")
@click.option("--mode", required=False, help="The mode of the hackathon.")
@click.option("--organizer", required=False, help="The organizer of the hackathon.")
@click.option("--hasPrize", "hasPrize", required=False, help="The prize of the hackathon.")
@click.option("--prizeDetails", "prizeDetails", required=False, help="The prize details of the hackathon.")
@click.option("--tags", required=False, help="The tags of the hackathon.")
@click.option("--status", required=False, default="pending", help="The status of the hackathon defaults to pending.")
@click.option("--interestCount", "interestCount", required=False, default=0, help="The interest count of the hackathon.")
def add_hackathon(name,url,description,startDate,endDate,location,mode,organizer,hasPrize,prizeDetails,tags,status,interestCount):
	
	"""
	Accessibility: All users (default_fallback: pending) only admins can update status to 'published' using update
	Only name and url parameters are required for you to create a hackathon, all other parameters are optional. If you don't provide them they will be set to None or default values.
	"""
 
	# Parsing parameters
	params = {
		"name": name,
		"url": url,
		"description": description,
		"startDate": startDate,
		"endDate": endDate,
		"location": location,
		"mode": mode,
		"organizer": organizer,
		"hasPrize": hasPrize,
		"prizeDetails": prizeDetails,
		"tags": tags,
		"status": status,
		"interestCount": interestCount
	}
	
	# Validating parameters
	results_are_valid , validated_params = validate_parameters2(params, method="cli-command-post")
	
	if not results_are_valid:
		return click.echo(f"Error: {validated_params}")

 	#Creating Hackathon Instance and inserting in db same logic as API
	try:
		new_hackathon = Hackathon(
			name=validated_params["name"],
			url=validated_params["url"],
			description=validated_params["description"],
			startDate=validated_params["startDate"],
			endDate=validated_params["endDate"],
			location=validated_params["location"],
			mode=validated_params["mode"],
			organizer=validated_params["organizer"],
			hasPrize=validated_params["hasPrize"],
			prizeDetails=validated_params["prizeDetails"],
			tags=validated_params["tags"],
			status=validated_params["status"],
			interestCount=validated_params["interestCount"]
		)
  
		db.session.add(new_hackathon)
		db.session.commit()
		return click.echo(f"Hackathon '{validated_params['name']}' created successfully.")
	except Exception as e:
		return click.echo(f"Error creating hackathon: {e}")

@app.cli.command("update-hackathon")
@click.option("--hackathon_id", required=True, help="The id of the hackathon you want to update.")
@click.option("--name", required=False, help="The name of the hackathon you want to update.")
@click.option("--url", required=False, help="The URL of the hackathon you want to update.")
@click.option("--description", required=False, help="The description of the hackathon you want to update.")
@click.option("--startDate","startDate" , default=None, required=False, help="The start date of the hackathon you want to update.")
@click.option("--endDate", "endDate",default=None, required=False, help="The end date of the hackathon you want to update.")
@click.option("--location", required=False, help="The location of the hackathon you want to update.")
@click.option("--mode", required=False, help="The mode of the hackathon you want to update.")
@click.option("--organizer", required=False, help="The organizer of the hackathon you want to update.")
@click.option("--hasPrize", "hasPrize", required=False, help="The prize of the hackathon you want to update.")
@click.option("--prizeDetails", "prizeDetails", required=False, help="The prize details of the hackathon you want to update.")
@click.option("--tags", required=False, help="The tags of the hackathon you want to update.")
@click.option("--status", required=False, help="The status of the hackathon defaults to pending you want to update.")
@click.option("--interestCount", "interestCount", required=False, default=0, help="The interest count of the hackathon you want to update.")
def update_hackathon(hackathon_id,name,url,description,startDate,endDate,location,mode,organizer,hasPrize,prizeDetails,tags,status,interestCount):

	"""
	Accessibility: Only superadmin & admins can update Hackathons.
	Only id of the hackathon is required for you to update the hackathon, all other parameters are optional.
	If you don't provide them they will be set to None or default values.
	"""

	# Authenticating admins
	if not authenticate_admins():
		return

	# Fetching Hackathon that we want to update
	hackathon_to_update = Hackathon.query.filter_by(id=hackathon_id).first()

	if not hackathon_to_update:
		click.echo(f"Hackathon with an id of {hackathon_id} was not found")

	# Parsing parameters
	params = {
		"name": name,
		"url": url,
		"description": description,
		"startDate": startDate,
		"endDate": endDate,
		"location": location,
		"mode": mode,
		"organizer": organizer,
		"hasPrize": hasPrize,
		"prizeDetails": prizeDetails,
		"tags": tags,
		"status": status,
		"interestCount": interestCount
	}

	# Validating parameters
	results_are_valid , validated_params = validate_parameters2(params, method="cli-command-patch", hackathon_to_update=hackathon_to_update)

	if not results_are_valid:
		return click.echo(f"Error: {validated_params}")

 	# Update selected Hackathon instance in db same logic as API
	try:
		for key,value in validated_params.items():
			setattr(hackathon_to_update, key,value)
		db.session.commit()
		return click.echo(f"Hackathon with an id of {hackathon_id} updated successfully.")
	except Exception as e:
		return click.echo(f"Error creating hackathon: {e}")

@app.cli.command("delete-hackathon")
@click.option("--hackathon_id", required=True, help="The id of the hackathon you want to delete.")
def delete_hackathon(hackathon_id):

	"""
	Accessibility: Only superadmin & admins can delete Hackathons.
	Only id of the hackathon is required for you to delete the hackathon.
	"""

	# Authenticating admins
	if not authenticate_admins():
		return

	# Fetching Hackathon that we want to delete
	hackathon_to_delete = Hackathon.query.filter_by(id=hackathon_id).first()

	print(hackathon_to_delete)

	if not hackathon_to_delete:
		click.echo(f"Hackathon with an id of {hackathon_id} was not found")

	# Delete the selected hackathon from the database
	try:
		db.session.delete(hackathon_to_delete)
		db.session.commit()
		click.echo(f"Hackathon with an id of {hackathon_id} was successfully deleted")
	except Exception as e:
		click.echo(f"Error: {e}")

#delete-hackathon: access only from superadmin or admin