import logging
import os
from flask import Flask, request, abort, jsonify
from flask_cors import CORS
from sqlalchemy.sql.sqltypes import DateTime
from models import setup_db,db_refresh_with_mock_data,Movies,Actors
from auth import AuthError, requires_auth

def create_app(test_config=None): # create and configure the app
    app = Flask(__name__)
    app.config.from_object('config')
    CORS(app)
    setup_db(app)

    @app.after_request 
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    #uncomment below func to reset the db with data
    db_refresh_with_mock_data()

    #------------------ LOG ---------------------------------------
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    def _logger():
        '''
        Setup logger format, level, and handler.

        RETURNS: log object
        '''
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        log = logging.getLogger(__name__)
        log.setLevel(LOG_LEVEL)

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)

        log.addHandler(stream_handler)
        return log

    LOG = _logger()
    print(LOG_LEVEL)
    LOG.debug("Starting with log level: %s" % LOG_LEVEL) 


    @app.route('/')
    def hello_world():
        return 'Hello, Udacity Full Stack - Final Capstone Project!\n'

    #------------------ GET ---------------------------------------
    @app.route("/movies/")
    @requires_auth('view:movies')
    def get_movies(payload):
        try:
            movies = Movies.query.all()
            movies_formated = [movie.format() for movie in movies]
            #print(movies_formated)
        except Exception as e:
            abort(422)
        return jsonify ({"success": True, "movies": movies_formated,"count":len(movies_formated)})
    
    @app.route("/actors/")
    @requires_auth('view:actors')
    def get_actors(payload):
        try:
            actors = Actors.query.all()
            actors_formated = [actor.format() for actor in actors]
            #print(actors_formated)
        except Exception as e:
            abort(422)
        return jsonify ({"success": True, "actors": actors_formated,"count":len(actors_formated)})

 #------------------ DELETE ---------------------------------------
    @app.route("/actor/<int:id>/",methods =['DELETE'])
    @requires_auth('delete:actor')
    def delete_actor(payload,id):
        #actor = Actors.query.get(id)
        actor = Actors.query.filter(Actors.id == id).one_or_none()
        if actor is None:
            abort(404,f"{id} not exists.Please provide valid actor info.")

        try:  
            print(id)
            actor.delete()
            return jsonify({ 
            'success': True,
            'deleted_actor_id': id
            })
        except Exception as e:
            print(e)
            abort(422)

    @app.route("/movies/<int:id>/",methods =['DELETE'])
    @requires_auth('delete:movie')
    def delete_movie(payload,id):
        movie = Movies.query.get(id)
        if movie is None:
            abort(404,f"{id} not exists.Please provide valid actor info.")

        try:  
            movie.delete()
            return jsonify({ 
            'success': True,
            'deleted_movie_id': id
            })
        except Exception as e:
            print(e)
            abort(422)

#------------------ POST ---------------------------------------
    @app.route('/movies/', methods=['POST'])
    @requires_auth('create:movie')
    def create_movie(payload=''):
        body = request.get_json()
        title,release_date = movie_validate_create_update(body)
        try:
            movie_new = Movies(title=title,release_date=release_date)
            movie_new.insert()
        except Exception as e:
            print(e)
            abort(422)
        
        return jsonify ({"success": True, "movie":  movie_new.format(),"count" : len(Movies.query.all())})

    @app.route('/actors/', methods=['POST'])
    @requires_auth('create:actor')
    def create_actor(payload=''):
        body = request.get_json()
        name,age,gender = actor_validate_create_update(body)
        try:
            actor_new = Actors(name=name,age=age,gender=gender)
            actor_new.insert()
        except Exception as e:
            print(e)
            abort(422)
        
        return jsonify ({"success": True, "actor":  actor_new.format(),"count" : len(Actors.query.all())})

#------------------ PATCH ---------------------------------------
    @app.route('/actors/<int:id>/', methods=['PATCH'])
    @requires_auth('update:actor')
    def update_actor(payload,id):
        body = request.get_json()
        name,age,gender = actor_validate_create_update(body,False)
        
        actor = Actors.query.get(id)
        if actor is None:
            abort(404,f"{id} not exists.Please provide valid data for update.")
        
        try:        
            actor.name= name
            actor.age= age 
            actor.gender= gender
            actor.update() 
        except:
            abort(422)
        return jsonify ({"success": True, "actor": actor.format(),"count" : len(Actors.query.all())})

    @app.route('/movies/<int:id>/', methods=['PATCH'])
    @requires_auth('update:movie')
    def update_movie(payload,id):
        body = request.get_json()
        title,release_date = movie_validate_create_update(body)
        
        movie = Movies.query.get(id)
        if movie is None:
            abort(404,f"{id} not exists.Please provide valid data for update.")
        
        try:        
            movie.title= title
            movie.release_date= release_date 
            movie.update() 
        except:
            abort(422)
        return jsonify ({"success": True, "movie": movie.format(),"count" : len(Movies.query.all())})

#------------------ LOCAL FUNC ---------------------------------------

    def movie_validate_create_update(body,is_create = True):
        #print(body) 
        if body is None:
            abort(400,"Request body not valid or found.") # bad request since expected header not avail

        title = body.get('title',None)
        release_date = body.get('release_date',None)

        if title is None or release_date is None: 
            abort(400,"Request body data can not not be empty.") 
        
        if title is not None and is_create:
            movie = Movies.query.filter(Movies.title == title).one_or_none()
            if movie is not None:
                abort(404,f"{title} already exists.Please provide new title.")
        
        return (title,release_date)

    def actor_validate_create_update(body,is_create = True):
        #print(body) 
        if body is None:
            abort(400,"Request body not valid or found.") # bad request since expected header not avail

        name = body.get('name',None)
        age = body.get('age',None)
        gender = body.get('gender',None)

        if name is None or age is None or gender is None: 
            abort(400,"Request body data can not not be empty or valid.") 
        
        if name is not None and is_create:
            actor = Actors.query.filter(Actors.name == name).one_or_none()
            if actor is not None:
                abort(422,f"{name} already exists.Please provide new name.")
        
        return (name,age,gender) 

#------------------ Error Handling ---------------------------------------
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
    def not_authenticated(error):
        return jsonify({
            'success': False,
            'error': 401,
            'message': 'authentication fails.',
            }), 401

    @app.errorhandler(403)
    def no_valid_permission_authorization(error):
        return jsonify({
            'success': False,
            'error': 403,
            'message': 'Authentication good,dont have valid authorization/permission.',
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

    @app.errorhandler(AuthError)
    def authentification_failed(AuthError): 
        return jsonify({
            "success": False, 
            "error": AuthError.status_code,
            "message": "authentication fails."
            }), 401

    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)