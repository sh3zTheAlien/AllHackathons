from datetime import datetime

# TESTING ALL HACKATHONS API | ENDPOINT: /api/hackathons | METHOD: GET


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

def test_all_hackathons_with_wrong_and_right_status(app,client):
    
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
    
def test_all_hackathons_with_wrong_and_right_upcoming(app,client):
    
    hackathon1 = {
                "name":"Hackathon1",
                "url":"hack1.com",
                "startDate":"2025-02-04 15:00:00",
                "endDate":"2025-02-06 18:00:00"
            }
        
    hackathon2 = {
                "name":"Hackathon2",
                "url":"hack2.com",
                "startDate":"2027-06-05 15:00:00",
                "endDate":"2027-07-01 15:00:20"
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

def test_all_hackathons_with_wrong_and_right_past(app,client):
    
    hackathon1 = {
                "name":"Hackathon1",
                "url":"hack1.com",
                "startDate":"2025-02-04 15:00:00",
                "endDate":"2025-02-06 18:00:00"
            }
        
    hackathon2 = {
                "name":"Hackathon2",
                "url":"hack2.com",
                "startDate":"2027-06-05 15:00:00",
                "endDate":"2027-07-01 15:00:20"
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