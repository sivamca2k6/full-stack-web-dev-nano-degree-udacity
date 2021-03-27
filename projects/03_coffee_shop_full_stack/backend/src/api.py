import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

#relative import from folder .database.models
from .database.models import db_drop_and_create_all_mock_data, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

#comment below code
#db_drop_and_create_all_mock_data()


# ROUTES
@app.route("/")
def home():
    return "Hello, coffe shop full stack!"


@app.route("/drinks")
def get_drinks():
    try:
        drinks = Drink.query.all()
        #print(drinks[0].long(),drinks[0].short())
        drinks_short = [drink.short() for drink in drinks]
        #print(drinks)
    except Exception as e:
        print(e)
        abort(422)
    return jsonify ({"success": True, "drinks": drinks_short,"count":len(drinks_short)})
     

@app.route("/drinks-detail")
def get_drinks_detail(): 
    try:
        drinks = Drink.query.all()
        drinks_short = [drink.long() for drink in drinks]
    except:
        abort(422)
    return jsonify ({"success": True, "drinks": drinks_short})


@app.route('/drinks', methods=['POST'])
def create_drink():
    body = request.get_json()
    title,recipe = validate_create_update(body)
    
    try:
        drink_new = Drink(title=title,recipe=recipe)
        drink_new.insert()
        #print(drink_new.id)
        #drink_new.recipe =  body['recipe']
    except Exception as e:
        print(e)
        abort(422)
    
    return jsonify ({"success": True, "drinks":  drink_new.long(),"count" : len(Drink.query.all())})


@app.route('/drinks/<int:id>',methods=['PATCH'])
def update_drink(id):
    body = request.get_json()
    title,recipe = validate_create_update(body)
    
    drink = Drink.query.get(id)
    if drink is None:
        abort(404,f"{id} not exists.Please provide valid drink data for update.")
    
    try:        
        drink.title= title
        drink.recipe= recipe
        drink.update() 
    except:
        abort(422)
    return jsonify ({"success": True, "drinks": drink.long(),"count" : len(Drink.query.all())})


@app.route('/drinks/<int:id>', methods=['DELETE'])   
def delete_drink(id):
    drink = Drink.query.get(id)
    if drink is None:
        abort(404,f"{id} not exists.Please provide valid drink data.")

    try:  
        drink.delete()
        return jsonify({
        'success': True,
        'delete': id,
        "drinks_count":len(Drink.query.all())
        })
    except:
        abort(422)

#local functions

def validate_create_update(body):
#    print(body) 
    if body is None:
        abort(400,"Request body not valid or found.") # bad request since expected header not avail

    title = body.get('title',None)
    recipe = body.get('recipe',None)
    
    #print(recipe , str(recipe), recipe[0], len(recipe))
    print(len(Drink.query.all()))

    if title is None or recipe is None: 
        abort(400,"Request body data can not not be empty.") 
    if not (all("name" in l for l in recipe)) :
        abort(400,"Request body doest not contain name.") 

    # drink = Drink.query.filter(Drink.title == title)
    # if drink is not None:
    #     abort(404,f"{title} already exists.Please provide new title.")

    #print(f'{recipe}',"""{}""".format(body['recipe'])) 
    return (title,f'{recipe}')

# Error Handling

@app.errorhandler(400)
def bad_request(error):
    message = error.description
    if message is None :
        message ='bad request'
    return jsonify({
        'success': False,
        'error': 400,
        'message': message,
    }), 400

@app.errorhandler(401)
def unprocessable(error):
    return jsonify({
        'success': False,
        'error': 401,
        'message': 'Unauthorized',
        }), 401

@app.errorhandler(403)
def unprocessable(error):
    return jsonify({
        'success': False,
        'error': 403,
        'message': 'Forbidden',
        }), 403

@app.errorhandler(404)
def not_found(error):
    message = error.description
    if message is None :
        message ='resource not found'
    return jsonify({
        'success': False,
        'error': 404,
        'message': message,
        }), 404

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
        'success': False,
        'error': 405,
        'message': 'method not allowed',
        }), 405

@app.errorhandler(422)
def unprocessable(error):
    message = error.description
    if message is None :
        message ='unprocessable'
    return jsonify({
        'success': False,
        'error': 422,
        'message': message
        }), 422



