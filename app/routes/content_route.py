from flask import Blueprint, request, jsonify, make_response
from flask import abort
from app import db
from os import abort
from sqlalchemy import Enum


from app.models.content import Content



content_bp = Blueprint('contents', __name__, url_prefix='/contents')

@content_bp.route('/<content_id>', methods=['DELETE'])
def delete_one_content(content_id):
    content = validate_content(content_id)

    db.session.delete(content)
    db.session.commit()

    rsp = {'msg': f'Content #{content.content_id} successfully deleted!'}
    return jsonify(rsp), 200


def validate_content(content_id):
    try:
        content_id = int(content_id)
    except:
        rsp = {"msg": f"Content with id {content_id} is invalid."}
        abort(make_response(rsp, 400))

    content = Content.query.get(content_id)

    if not content:
        rsp = {'msg': f'Could not find content with id {content_id}.'}
        abort(make_response(rsp, 404))

    return content



@content_bp.route('/<content_id>', methods=['PUT'])
def update_one_content(content_id):
    content = validate_content(content_id)
    request_body = request.get_json()
    
    try:
        if "like_count" in request_body:
            content.like_count += 1
    
    except KeyError:
        return {
            'msg': 'Update failed!'
        }, 400

    db.session.add(content)
    db.session.commit()
   
    response=jsonify({
        'content': content.content,
        'content_id': content.content_id,
        'like_count': content.like_count,
        'comment': content.comment,
        # 'color': content.color,
        # 'PosX': content.PosX,
        # 'posY': content.PosY,


    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
