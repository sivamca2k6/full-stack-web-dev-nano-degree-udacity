import logging
import os
from flask import Flask, request, abort, jsonify
from flask_cors import CORS
from sqlalchemy.sql.sqltypes import DateTime
from models import setup_db,db_refresh_with_mock_data,Movies,Actors

def create_app(test_config=None): # create and configure the app
  app = Flask(__name__)
  app.config.from_object('config')
  CORS(app)
  setup_db(app)
  #return app
  #app = create_app()

  #uncomment below func to reset the db with data
  #db_refresh_with_mock_data()

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
  def get_movies():
    try:
        movies = Movies.query.all()
        movies_formated = [movie.format() for movie in movies]
        #print(movies_formated)
    except Exception as e:
        abort(422)
    return jsonify ({"success": True, "movies": movies_formated,"count":len(movies_formated)})
  
  @app.route("/actors/")
  def get_actors():
    try:
        actors = Actors.query.all()
        actors_formated = [actor.format() for actor in actors]
        #print(actors_formated)
    except Exception as e:
        abort(422)
    return jsonify ({"success": True, "actors": actors_formated,"count":len(actors_formated)})

  if __name__ == '__main__':
      app.run(host='0.0.0.0', port=8080, debug=True)


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


      return jsonify({
          "success": False, 
          "error": AuthError.status_code,
          "message": "authentification fails."
          }), 401

  return app