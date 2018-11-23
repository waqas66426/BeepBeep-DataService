import os
from flakon import SwaggerBlueprint
from flask import request, jsonify
from beepbeep.dataservice.database import db, Objective


HERE = os.path.dirname(__file__)
YML = os.path.join(HERE, '..', 'static', 'api-swagger.yaml')
objectives_api = SwaggerBlueprint('objectives', __name__, swagger_spec=YML)


def json_to_objective(db_objective, json_objective, runner_id):

    db_objective.user_id = runner_id
    db_objective.distance = json_objective['distance']

    return db_objective


@objectives_api.operation('getObjectives')
def get_objectives(id):
    objectives = db.session.query(Objective).filter(Objective.user_id == id)
    return jsonify([objective.to_json() for objective in objectives])


@objectives_api.operation('setObjective')
def add_objective(id):
    runner_id = id
    objective = request.get_json()

    db_objective = json_to_objective(Objective(), objective, runner_id)
    db.session.add(db_objective)

    db.session.commit()

    objective = db.session.query(Objective).filter(Objective.user_id == runner_id).first()
    return jsonify(objective.to_json())


@objectives_api.operation('getObjectiveById')
def get_objective(id, objectiveId):
    objective = db.session.query(Objective).filter(Objective.user_id == id, Objective.id == objectiveId).first()
    if objective is None:
        return jsonify({"error": "objective not found"}), 404
    else:
        return jsonify(objective.to_json())


@objectives_api.operation('updateObjectiveById')
def update_objective(id, objectiveId):
    objective = db.session.query(Objective).filter(Objective.user_id == id, Objective.id == objectiveId).first()

    if request.get_json() is None:
        return "Invalid objective body", 400

    if objective is None:
        return jsonify({"error": "objective not found"}), 404

    json_to_objective(objective, request.get_json(), id)
    db.session.commit()

    objective = db.session.query(Objective).filter(Objective.user_id == id, Objective.id == objectiveId).first()
    return jsonify(objective.to_json())


@objectives_api.operation('deleteObjectiveById')
def delete_run(id, objectiveId):
    objective = db.session.query(Objective).filter(Objective.user_id == id, Objective.id == objectiveId).first()

    if objective is None:
        return jsonify({"error": "objective not found"}), 404
    else:
        db.session.delete(objective)
        db.session.commit()
        return "", 204
