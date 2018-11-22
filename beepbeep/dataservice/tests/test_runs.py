from beepbeep.dataservice.database import Run


RUNSPATH = "/users/1"

def test_create_run(db,client):
    global RUNSPATH
    r = client.post( "/users/1/runs" , json=[{
        "title" : "Example Run",
        "description" : "Nice run",
        "strava_id" : 42,
        "distance" : 25,
        "start_date" : 20181122,
        "elapsed_time" : 42,
        "average_speed" : 10,
        "average_heartrate" : 22 ,
        "total_elevation_gain" : 10,
        "runner_id" : 1
    }])


    request = r.get_json()[0]
    assert  request['strava_id'] == 42             
    

def test_get_runs(db, client):
    global RUNSPATH
    r = client.get( RUNSPATH +  "/runs")
    runs = r.get_json()
    assert r.status_code == 200, "Should return the runs list"
    assert len(runs) == 1, "Should return 2 run"


def test_get_run_by_id(db, client):
    global RUNSPATH
    r = client.get( RUNSPATH + "/runs/1" )
    run = r.get_json()
    assert r.status_code == 200, "Should return the run with 200 status code"
    assert run['id'] == 1, "Should return run 1"
    assert run['runner_id'] == 1, "Should return the runner id"


def test_get_run_404(db, client):
    global RUNSPATH
    r = client.get( RUNSPATH + "/runs/1999" )
    assert r.status_code == 404, "Missing run should return 404"


def test_update_run(db, client):
    global RUNSPATH
    r = client.put( RUNSPATH + "/runs/1", json={
        "id": 1,
        "title": "UpdatedRun",
        "description": "UpdatedRun",
        "strava_id" : 42,
        "distance" : 14,
        "start_date" : 20181122,
        "elapsed_time" : 13,
        "average_speed" : 15,
        "average_heartrate" : 34 ,
        "total_elevation_gain" : 10,
        "runner_id" : 1
    })
    assert r.status_code == 200, "Should update the run"
    run = r.get_json()
    assert run['title'] == "UpdatedRun", "Should update the run name"

def test_update_run_missing_body(db, client):
    global RUNSPATH
    r = client.put( RUNSPATH + "/runs/1" )
    assert r.status_code == 400, "missing data"

def test_update_404_run(db, client):
    global RUNSPATH
    r = client.put( RUNSPATH + "/runs/999", json={
        "id": 999,
        "name": "Updated404Run",
        "strava_id" : 34,
        "distance" : 21,
        "start_date" : "2018-11-22",
        "elapsed_time" : 13,
        "average_speed" : 56,
        "average_heartrate" : 13 ,
        "total_elevation_gain" : 67,
        "runner_id" : 1
    })
    assert r.status_code == 404, "Should return 404"

def test_delete_run_by_id(db, client):
    global RUNSPATH
    r = client.delete( RUNSPATH + "/runs/1" )
    assert r.status_code == 204, "Successfully deleted"
    r = client.get( RUNSPATH + "/runs/1" )
    assert r.status_code == 404, "Should have deleted run"

def test_delete_404_run(db, client):
    global RUNSPATH
    r = client.delete( RUNSPATH + "/runs/666" )
    assert r.status_code == 404, "Should return 404 status code" 

def test_delete_run_missing_id(db, client):
    global RUNSPATH
    r = client.delete( RUNSPATH + "/runs/" )
    assert r.status_code == 404, "Should return 404 status code"                             

def test_get_max_run_id(db, client):
    global RUNSPATH
    r = client.get( RUNSPATH + "/runs/getMaxId" )
    assert r.status_code == 200, "Should return the run MaxId"