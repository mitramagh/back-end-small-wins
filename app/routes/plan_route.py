from flask import Blueprint, request, jsonify, make_response
from flask import abort
from app import db
from os import abort
import os
import requests
from datetime import datetime


from app.models.plan import Plan
from app.models.content import Content
# from app.models.content import ContentType

plan_bp = Blueprint("plan_bp", __name__, url_prefix="/plans")


@plan_bp.route("", methods=["POST"])
def create_one_plan():
    request_body = request.get_json()
    request_body = validate_plan_input(request_body)

    new_plan = Plan(idea=request_body['idea'], planner=request_body['planner'])

    # if "completed_at" in request_body:
    #     new_plan.completed_at = request_body["completed_at"]
    # if new_plan.completed_at:
    #     completed = True
    # else:
    #     completed = False

    db.session.add(new_plan)
    db.session.commit()
    return {
        'id': new_plan.plan_id,
        'idea': new_plan.idea,
        'planner': new_plan.planner,
        'created_date': new_plan.created_date,
        'completed_at':new_plan.completed_at,
        'msg': f'{new_plan.planner} created {new_plan.idea} at {new_plan.created_date}'
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
            'created_date':plan.created_date,
            'completed_at':plan.completed_at,
        })

    return jsonify(plans_response), 200


# GET - Read; Select a specific plan

@plan_bp.route("/<plan_id>", methods=["GET"])
def get_one_plan(plan_id):
    chosen_plan = validate_plan(plan_id)
  
    response = {
        "id": chosen_plan.plan_id,
        "idea": chosen_plan.idea,
        "planner": chosen_plan.planner,
        'created_date':chosen_plan.created_date,
        'completed_at':chosen_plan.completed_at,
    }
    return jsonify(response), 200


# Helper function to validate plan_id:
def validate_plan(plan_id):
    try:
        plan_id = int(plan_id)
    except ValueError:
        abort(make_response(
            {"message": f"Plan: {plan_id} is not a valid plan id"}, 400))
    plan = Plan.query.get(plan_id)
    if not plan:
        abort(make_response(
            {"message": f"Plan: #{plan_id} not found"}, 404))
    return plan

# DELETE - delete; delete a specific plan


@plan_bp.route('/<plan_id>', methods=['DELETE'])
def delete_one_plan(plan_id):
    plan = validate_plan(plan_id)

    db.session.delete(plan)
    db.session.commit()

    rsp = {'msg': f'Plan #{plan.plan_id} successfully deleted!'}
    return jsonify(rsp), 200


# update chosen plan is completed
@plan_bp.route('/<plan_id>/mark_complete', methods=['PATCH'])
def update_plan_is_complete(plan_id):
    chosen_plan = validate_plan(plan_id)

    chosen_plan.completed_at = datetime.utcnow()
    db.session.commit()

    response = {
        "id": chosen_plan.plan_id,
        "idea": chosen_plan.idea,
        "planner": chosen_plan.planner,
        'created_date':chosen_plan.created_date,
        'completed_at':chosen_plan.completed_at,
    }
    return jsonify(response), 200

    # update chosen plan is Incompleted
@plan_bp.route('/<plan_id>/mark_incomplete', methods=['PATCH'])
def update_plan_is_incomplete(plan_id):
    chosen_plan = validate_plan(plan_id)

    chosen_plan.completed_at = None
    db.session.commit()

    response = {
        "id": chosen_plan.plan_id,
        "idea": chosen_plan.idea,
        "planner": chosen_plan.planner,
        'created_date':chosen_plan.created_date,
        'completed_at':chosen_plan.completed_at,
    }
    return jsonify(response), 200

# POST: Create a new content for the selected plan,
@plan_bp.route("/<plan_id>/contents", methods=["POST"])
def create_content_for_plan(plan_id):
    plan = validate_plan(plan_id)
    request_body = request.get_json()
    print(request_body)
   
    new_content = Content(
        type=request_body["type"],
        content=request_body["content"],

        plan=plan,
    )
    print(new_content)
    db.session.add(new_content)
    db.session.commit()

    return {
        'msg': f'Succesfully created new content for {plan.idea}',
        'type': new_content.type,
        'content': new_content.content,
        'content_id': new_content.content_id,
        'like_count': new_content.like_count,
        'comment': new_content.comment,
        'plan_id': plan_id,
        # 'color':new_content.color,
        # "PosX": new_content.PosX,
        # "PosY": new_content.PosY,
    }, 201

    # color=request_body['color'],
    # PosX=100,
    # PosY=0,

"""
# POST: Create a new content for a specific content type for the selected plan,
@plan_bp.route("/<plan_id>/contents/<type>", methods=["POST"])
def create_image_content_for_plan(plan_id, type):
    plan = validate_plan(plan_id)
    # type = validate_plan_content(ContentType[type])
    request_body = request.get_json()
    if "content" not in request_body:
        return {"content": "Please add something to post a content"}, 400
    print(ContentType(type))
    new_content = Content(
        type=ContentType(type).value,
        content=request_body["content"],
        plan=plan,
    )
    db.session.add(new_content)
    db.session.commit()

    return {
        'msg': f'Succesfully created new content for {plan.idea}',
        'type': new_content.type,
        'content': new_content.content,
        'content_id': new_content.content_id,
        'like_count': new_content.like_count,
        'comment': new_content.comment,
        'plan_id': plan_id
    }, 201
    """

    # GET- Read all contents in a selected plan

@plan_bp.route("/<plan_id>/contents", methods=["GET"])
def get_all_contents_for_plan(plan_id):
    chosen_plan = validate_plan(plan_id)
    chosen_plan_contents = []
    for content in chosen_plan.contents:
        chosen_plan_contents.append({
            'type': content.type,
            'content': content.content,
            'content_id': content.content_id,
            'like_count': content.like_count,
            'comment': content.comment,
            'plan_id': content.plan_id
        })
    return jsonify(chosen_plan_contents), 200
