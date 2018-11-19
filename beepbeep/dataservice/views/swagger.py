import os
from datetime import datetime

from flakon import SwaggerBlueprint
from flask import request, jsonify
from beepbeep.dataservice.database import db, User, Run
import json
from json import loads

HERE = os.path.dirname(__file__)
YML = os.path.join(HERE, '..', 'static', 'api-swagger.yaml')
api = SwaggerBlueprint('API', __name__, swagger_spec=YML)


@api.operation('getRuns')
def get_runs(id):
    runs = db.session.query(Run).filter(Run.runner_id == id)
    return jsonify([run.to_json() for run in runs])


@api.operation('addRuns')
def add_runs(id):
    added = 0
    runner_id = id
    for run in request.get_json():

        db_run = Run()
        db_run.strava_id = run['strava_id']
        db_run.distance = run['distance']
        db_run.start_date = datetime.fromtimestamp(run['start_date'])
        db_run.elapsed_time = run['elapsed_time']
        db_run.average_speed = run['average_speed']
        db_run.average_heartrate = run['average_heartrate']
        db_run.total_elevation_gain = run['total_elevation_gain']
        db_run.runner_id = runner_id
        db_run.title = run['title']
        db_run.description = run['description']
        db.session.add(db_run)

        added += 1

    if added > 0:
        db.session.commit()

    runs = db.session.query(Run).filter(Run.runner_id == id)
    return jsonify([run.to_json() for run in runs])