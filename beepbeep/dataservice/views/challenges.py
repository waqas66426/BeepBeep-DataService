import os
from flakon import SwaggerBlueprint
from flask import request, jsonify
from beepbeep.dataservice.database import db, Challenge

HERE = os.path.dirname(__file__)
YML = os.path.join(HERE, '..', 'static', 'api-swagger.yaml')
challenges_api = SwaggerBlueprint('challenges', __name__, swagger_spec=YML)


def json_to_challenge(db_challenge, json_challenge, runner_id_):

    db_challenge.runner_id = runner_id_
    db_challenge.run_id = json_challenge['run_id']
    db_challenge.latest_run_id = json_challenge['latest_run_id']

    return db_challenge


@challenges_api.operation('getChallenges')
def get_challenges(id):
    challenges = db.session.query(Challenge).filter(Challenge.runner_id == id)
    return jsonify([challenge.to_json() for challenge in challenges])


@challenges_api.operation('addChallenge')
def add_challenge(id):
    runner_id = id
    challenge = request.get_json()

    if db.session.query(Challenge).filter(Challenge.runner_id == runner_id).first() is not None:
        return "", 400

    db_challenge = json_to_challenge(Challenge(), challenge, runner_id)
    db.session.add(db_challenge)

    db.session.commit()

    challenge = db.session.query(Challenge).filter(Challenge.runner_id == runner_id).first()
    return jsonify(challenge.to_json())


@challenges_api.operation('getChallengeById')
def get_challenge(id, challengeId):
    challenge = db.session.query(Challenge).filter(Challenge.runner_id == id, Challenge.id == challengeId).first()
    if challenge is None:
        return jsonify({"error": "run not found"}), 404
    else:
        return jsonify(challenge.to_json())


@challenges_api.operation('updateChallengeById')
def update_challenge(id, challengeId):
    challenge = db.session.query(Challenge).filter(Challenge.runner_id == id, Challenge.id == challengeId).first()

    if challenge is None:
        return jsonify({"error": "run not found"}), 404

    json_to_challenge(challenge, request.get_json(), id)
    db.session.commit()

    challenge = db.session.query(Challenge).filter(Challenge.runner_id == id, Challenge.id == challengeId).first()
    return jsonify(challenge.to_json())

@challenges_api.operation('deleteChallengeById')
def delete_run(id, challengeId):
    challenge = db.session.query(Challenge).filter(Challenge.runner_id == id, Challenge.id == challengeId).first()

    if challenge is None:
        return jsonify({"error": "run not found"}), 404
    else:
        db.session.delete(challenge)
        db.session.commit()
        return "", 204
