from datetime import datetime,timedelta

# TESTING ALL HACKATHONS API | ENDPOINT: /api/hackathons | METHOD: GET

now = datetime.now().replace(microsecond=0)
next_year = now + timedelta(days=365)
next_year_plus_two_days = next_year + timedelta(days=2)
last_year = now - timedelta(days=365)
last_year_plus_two_days = last_year + timedelta(days=2)

def test_all_hackathons_while_adding_one_hackathon(app,client):
    hackathon1 = {
            "name":"Hackathon1",
            "url":"hack1.com",
        }
    
    with app.app_context():
            from main import db
            db.create_all()
            
    response1 = client.post("/api/hackathons", data=hackathon1)
    assert response1.status_code == 200
    assert response1.json["response"]["success"] == "Successfully added hackathon:Hackathon1!"
    
    #We are making sure that our post requests are valid and successfully reach our backend.
    
    results = client.get("/api/hackathons")
    assert results.status_code == 200
    assert results.json[0]["name"] == "Hackathon1"
    
def test_all_hackathons_while_adding_two_hackathons(app,client):
    hackathon1 = {
            "name":"Hackathon1",
            "url":"hack1.com",
        }
    
    hackathon2 = {
                "name":"Hackathon2",
                "url":"hack2.com",
            }
    
    with app.app_context():
            from main import db
            db.create_all()
            
    response1 = client.post("/api/hackathons", data=hackathon1)
    assert response1.status_code == 200
    assert response1.json["response"]["success"] == "Successfully added hackathon:Hackathon1!"
    
    response2 = client.post("/api/hackathons", data=hackathon2)
    assert response2.status_code == 200
    assert response2.json["response"]["success"] == "Successfully added hackathon:Hackathon2!"
    
    #We are making sure that our post requests are valid and successfully reach our backend.
    
    results = client.get("/api/hackathons")
    assert results.status_code == 200
    assert results.json[0]["name"] == "Hackathon1"
    assert results.json[1]["name"] == "Hackathon2"

def test_all_hackathons_with_wrong_and_right_status_parameter(app,client):
    
    hackathon1 = {
                "name":"Hackathon1",
                "url":"hack1.com",
                "status":"published"
            }
        
    hackathon2 = {
                "name":"Hackathon2",
                "url":"hack2.com",
                "status":"pending"
            }
        
    with app.app_context():
            from main import db
            db.create_all()
            
    response1 = client.post("/api/hackathons", data=hackathon1)
    assert response1.status_code == 200
    assert response1.json["response"]["success"] == "Successfully added hackathon:Hackathon1!"
    
    response2 = client.post("/api/hackathons", data=hackathon2)
    assert response2.status_code == 200
    assert response2.json["response"]["success"] == "Successfully added hackathon:Hackathon2!"
    
    result_test1 = client.get("/api/hackathons?status=published")
    assert result_test1.status_code == 200
    assert result_test1.json[0]["status"] == "published"
    
    result_test2 = client.get("/api/hackathons?status=pending")
    assert result_test2.status_code == 200
    assert result_test2.json[0]["status"] == "pending"
    
    result_test3 = client.get("/api/hackathons?status=something")
    assert result_test3.status_code == 404
    assert result_test3.json["error"] == "Wrong status"
    
def test_all_hackathons_with_wrong_and_right_upcoming_parameter(app,client):
    
    hackathon1 = {
                "name":"Hackathon1",
                "url":"hack1.com",
                "startDate":last_year,
                "endDate":last_year_plus_two_days
            }
        
    hackathon2 = {
                "name":"Hackathon2",
                "url":"hack2.com",
                "startDate":next_year,
                "endDate":next_year_plus_two_days
            }
        
    with app.app_context():
            from main import db
            db.create_all()
    
    response1 = client.post("/api/hackathons", data=hackathon1)
    assert response1.status_code == 200
    assert response1.json["response"]["success"] == "Successfully added hackathon:Hackathon1!"
    
    response2 = client.post("/api/hackathons", data=hackathon2)
    assert response2.status_code == 200
    assert response2.json["response"]["success"] == "Successfully added hackathon:Hackathon2!"

    result_test1 = client.get("api/hackathons?upcoming=True")
    assert result_test1.status_code == 200
    assert result_test1.json[0]["name"] == "Hackathon2"
    
    result_test2 = client.get("api/hackathons?upcoming=False")
    assert result_test2.status_code == 200
    assert result_test2.json[0]["name"] == "Hackathon1"
    
    result_test3 = client.get("api/hackathons?upcoming=something")
    assert result_test3.status_code == 404
    assert result_test3.json["error"] == "Wrong upcoming" 

def test_all_hackathons_with_wrong_and_right_past_parameter(app,client):
    
    hackathon1 = {
                "name":"Hackathon1",
                "url":"hack1.com",
                "startDate":last_year,
                "endDate":last_year_plus_two_days
            }
        
    hackathon2 = {
                "name":"Hackathon2",
                "url":"hack2.com",
                "startDate":next_year,
                "endDate":next_year_plus_two_days
            }
        
    with app.app_context():
            from main import db
            db.create_all()
    
    response1 = client.post("/api/hackathons", data=hackathon1)
    assert response1.status_code == 200
    assert response1.json["response"]["success"] == "Successfully added hackathon:Hackathon1!"
    
    response2 = client.post("/api/hackathons", data=hackathon2)
    assert response2.status_code == 200
    assert response2.json["response"]["success"] == "Successfully added hackathon:Hackathon2!"

    result_test1 = client.get("api/hackathons?past=True")
    assert result_test1.status_code == 200
    assert result_test1.json[0]["name"] == "Hackathon1"
    
    result_test2 = client.get("api/hackathons?past=False")
    assert result_test2.status_code == 200
    assert result_test2.json[0]["name"] == "Hackathon2"
    
    result_test3 = client.get("api/hackathons?past=something")
    assert result_test3.status_code == 404
    assert result_test3.json["error"] == "Wrong past"

def test_all_hackathons_tags_parameter(app,client):
    
    hackathon1 = {
                "name":"Hackathon1",
                "url":"hack1.com",
                "tags":"Web Development"
            }

    hackathon2 = {
                "name":"Hackathon2",
                "url":"hack2.com",
                "tags":"Cybersecurity"
            }
    
    with app.app_context():
        from main import db
        db.create_all()
    
    response1 = client.post("/api/hackathons", data=hackathon1)
    assert response1.status_code == 200
    assert response1.json["response"]["success"] == "Successfully added hackathon:Hackathon1!"

    response2 = client.post("/api/hackathons", data=hackathon2)
    assert response2.status_code == 200
    assert response2.json["response"]["success"] == "Successfully added hackathon:Hackathon2!"

    result_test1 = client.get("/api/hackathons?tags=Web Development")
    result_test1.status_code == 200
    result_test1.json[0]["name"] == "Hackathon1"
    result_test1.json[0]["tags"] == "Web Development"

    result_test2 = client.get("/api/hackathons?tags=Cybersecurity")
    result_test2.status_code == 200
    result_test2.json[0]["name"] == "Hackathon2"
    result_test2.json[0]["tags"] == "Cybersecurity"
    
    result_test3 = client.get("api/hackatonhs?tags=something")
    result_test3.status_code == 200
    result_test3.json == None
    
def test_all_hackathons_q_parameter(app,client):
    
    hackathon1 = {
                    "name":"Hackathon1",
                    "url":"hack1.com",
                    "description": "Another Description",
                    "location": "Kavala",
                    "tags":"Cybersecurity"
                }
    
    hackathon2 = {
                "name":"Hackathon2",
                "url":"hack2.com",
                "description": "Cool Description",
                "location": "Athens,Greece",
                "hasPrize":"true",
                "prizeDetails": "1500$",
                "tags":"AI,ML,Python"
            }
    
    hackathon3 = {
                    "name":"Hackathon3",
                    "url":"hack3.com",
                    "tags":"Cybersecurity",
                    "location":"Crete"
                }
    
    with app.app_context():
            from main import db
            db.create_all()
    
    response1 = client.post("/api/hackathons", data=hackathon1)
    assert response1.status_code == 200
    assert response1.json["response"]["success"] == "Successfully added hackathon:Hackathon1!"

    response2 = client.post("/api/hackathons", data=hackathon2)
    assert response2.status_code == 200
    assert response2.json["response"]["success"] == "Successfully added hackathon:Hackathon2!"
    
    response3 = client.post("/api/hackathons", data=hackathon3)
    assert response3.status_code == 200
    assert response3.json["response"]["success"] == "Successfully added hackathon:Hackathon3!"