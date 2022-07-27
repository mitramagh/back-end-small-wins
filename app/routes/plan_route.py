from flask import Blueprint, request, jsonify, make_response
from flask import abort
from app import db
from os import abort
import os
import requests


from app.models.plan import Plan
from app.models.planner import Planner

plan_bp = Blueprint("plan_bp", __name__, url_prefix="/plans")

@plan_bp.route("", methods=["POST"])
def create_one_plan():
    request_body = request.get_json()
    request_body = validate_plan_input(request_body)

    new_plan = Plan(
        idea=request_body['idea'], planner=request_body['planner'])

    db.session.add(new_plan)
    db.session.commit()
    return {
        'id': new_plan.plan_id,
        'idea': new_plan.idea,
        'planner': new_plan.planner,
        'msg': f'{new_plan.planner} created {new_plan.idea}'
    }, 201


# helper function:

def validate_plan_input(request_body):
    if "idea" not in request_body or "idea" == "":
        abort(make_response(
            {"details": "Invalid data. idea missing or invalid"}, 400))
    if "planner" not in request_body or "planner" == "":
        abort(make_response(
            {"details": "Invalid data. planner missing or invalid "}, 400))
    return request_body


# GET- Read; View a list of all plans

@plan_bp.route("", methods=["GET"])
def get_all_plans():
    plans = Plan.query.all()
    plans_response = []
    for plan in plans:
        plans_response.append({
            "id": plan.plan_id,
            "idea": plan.idea,
            "planner": plan.planner,
        })

    return jsonify(plans_response), 200


# GET - Read; Select a specific board

@plan_bp.route("/<plan_id>", methods=["GET"])
def get_one_plan(plan_id):
    chosen_plan = validate_plan(plan_id)

    response = {
            "id": chosen_plan.plan_id,
            "idea": chosen_plan.idea,
            "planner": chosen_plan.planner,
    }
    return jsonify(response), 200


# Helper function to validate plan_id:
def validate_plan(plan_id):
    try:
        plan_id = int(plan_id)
    except:
        abort(make_response(
            {"message": f"Board: {plan_id} is not a valid plan id"}, 400))
    plan = Plan.query.get(plan_id)
    if not plan:
        abort(make_response(
            {"message": f"Plan: #{plan_id} not found"}, 404))
    return plan