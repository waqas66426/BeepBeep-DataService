import os
from datetime import datetime

from flakon import SwaggerBlueprint
from flask import request, jsonify
from beepbeep.dataservice.database import db, Run
from sqlalchemy import func
import json
from json import loads

HERE = os.path.dirname(__file__)
YML = os.path.join(HERE, '..', 'static', 'api-swagger.yaml')
runs_api = SwaggerBlueprint('runs', __name__, swagger_spec=YML)



def json_to_run(db_run, json_run, runner_id):

    db_run.strava_id = json_run['strava_id']
    db_run.distance = json_run['distance']
    db_run.start_date = datetime.fromtimestamp(json_run['start_date'])
    db_run.elapsed_time = json_run['elapsed_time']
    db_run.average_speed = json_run['average_speed']
    db_run.average_heartrate = json_run['average_heartrate']
    db_run.total_elevation_gain = json_run['total_elevation_gain']
    db_run.runner_id = runner_id
    db_run.title = json_run['title']
    db_run.description = json_run['description']

    return db_run


@runs_api.operation('getRuns')
def get_runs(id):
    runs = db.session.query(Run).filter(Run.runner_id == id)
    return jsonify([run.to_json() for run in runs])


@runs_api.operation('addRuns')
def add_runs(id):
    added = 0
    runner_id = id
    for run in request.get_json():

        if db.session.query(Run).filter(Run.strava_id == run['strava_id']).first() is None:
            db_run = json_to_run(Run(), run, runner_id)
            db.session.add(db_run)
            added += 1

    if added > 0:
        db.session.commit()

    runs = db.session.query(Run).filter(Run.runner_id == id)
    return jsonify([run.to_json() for run in runs])


@runs_api.operation('getRun')
def get_run(id, runId):
    run = db.session.query(Run).filter(Run.runner_id == id, Run.id == runId).first()
    if run is None:
        return jsonify({"error": "run not found"}), 404
    else:
        return jsonify(run.to_json())


@runs_api.operation('updateRunById')
def update_run(id, runId):
    run = db.session.query(Run).filter(Run.runner_id == id, Run.id == runId).first()

    if request.get_json() is None:
        return "Invalid run body", 400

    if run is None:
        return jsonify({"error": "run not found"}), 404

    json_to_run(run, request.get_json(), id)
    db.session.commit()

    run = db.session.query(Run).filter(Run.runner_id == id, Run.id == runId).first()
    return jsonify(run.to_json())


@runs_api.operation('deleteRunById')
def delete_run(id, runId):
    run = db.session.query(Run).filter(Run.runner_id == id, Run.id == runId).first() # .delete
    if run is None:
        return jsonify({"error": "run not found"}), 404
    else:
        db.session.delete(run)
        db.session.commit()
        return "", 204


@runs_api.operation('getMaxId')
def get_run_maxId(id):
    max_id = db.session.query(func.max(Run.id)).scalar()
    return jsonify({"max_id": max_id})