import logging
import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  CORS(app)
  app.config.from_object('config')
  return app

APP = create_app()


# LOG
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

@APP.route('/')
def hello_world():
    return 'Hello, Udacity Full Stack - Final Capstone Project!\n'

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)