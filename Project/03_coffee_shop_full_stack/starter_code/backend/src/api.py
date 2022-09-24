import os
import this
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS
from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
!! Running this funciton will add one
'''
db_drop_and_create_all()


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods',
                         'GET,PUT,POST,DELETE,OPTIONS')
    return response


# ROUTES
'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
        returns status code 200 and json {"success": True, "drinks": drinks}
        where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks')
# @requires_auth('get:drinks')
def get_drinks():
    all_drinks_query = Drink.query.all()
    if not all_drinks_query:
        abort(404, "No drink available")
    # return jsonify([
    #     drink.short()
    #     for drink in all_drinks_query
    # ])
    return jsonify({
        "drinks": [drink.short() for drink in all_drinks_query]
    })


'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
        returns status code 200 and json {"success": True, "drinks": drinks}
        where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def get_drinks_detail():
    all_drinks_query = Drink.query.all()
    if not all_drinks_query:
        abort(404, "No drink available")
    # return jsonify([
    #    drink.long()
    #    for drink in all_drinks_query
    # ])
    return jsonify({
        "drinks": [drink.long() for drink in all_drinks_query]
    })


'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
        returns status code 200 and json {"success": True, "drinks": drink}
        where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def create_new_drink():
    drink_post_data = request.get_json()
    drink = Drink(
        title=drink_post_data['title'],
        recipe=json.dumps(drink_post_data['recipe'])
    )
    drink.insert()
    return jsonify({
        "success": True,
        "drinks": {
            "id": drink.id,
            "title": drink.title,
            "recipe": drink.recipe
        }
    })


'''

@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
        returns status code 200 and json {"success": True, "drinks": drink}
        where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks/<id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drink(id):
    drink_id = int(id)
    all_drinks_query = Drink.query.all()
    all_drinks_ids = [drink.id for drink in all_drinks_query]
    if drink_id not in all_drinks_ids:
        abort(404, "Drink id not found")

    drink_to_update = request.get_json()
    updating_drink = Drink.query.get(drink_id)

    if 'title' in drink_to_update:
        updating_drink.title = drink_to_update['title']
    if 'recipe' in drink_to_update:
        updating_drink.recipe = json.dumps(drink_to_update['recipe'])
    # ('[{'+
    #     '"name"'+':"'+str(drink_to_update["recipe_name"])+'", '+
    #     '"color"'+':"'+str(drink_to_update["recipe_color"])+'", '+
    #     '"parts"'+':'+str(drink_to_update["recipe_parts"])+
    #     '}]'
    # )
    updating_drink.update()
    return jsonify({
        "success": True,
        "drinks": [{
            "id": updating_drink.id,
            "title": updating_drink.title,
            "recipe": updating_drink.recipe
        }]
    })


'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
        returns status code 200 and json {"success": True, "delete": id}
        where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks/<id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(id):
    drink_id = int(id)
    all_drinks_query = Drink.query.all()
    all_drinks_ids = [drink.id for drink in all_drinks_query]
    if drink_id not in all_drinks_ids:
        abort(404, "Drink id not found")

    drink_to_delete = Drink.query.get(drink_id)
    drink_to_delete.delete()
    return jsonify({
        "success": True,
        "delete": drink_id
    })


# Error Handling
'''
Example error handling for unprocessable entity
'''


@app.errorhandler(404)
def unfound_request(error):
    response = jsonify({
        'message': error.description,
        'success': False,
    })
    response.status_code = 404
    return response


@app.errorhandler(422)
def unprocessable(error):
    response = jsonify({
        'message': error.description,
        'success': False,
    })
    response.status_code = 422
    return response


'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''

'''
@TODO implement error handler for 404
    error handler should conform to general task above
'''


'''
@TODO implement error handler for AuthError
    error handler should conform to general task above
'''
