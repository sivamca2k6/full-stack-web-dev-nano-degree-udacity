from flask import Flask, request, jsonify, abort
from functools import wraps

app = Flask(__name__)

def get_token_auth():
    if 'Authorization' not in request.headers :
        abort(401)
    header_part = request.headers['Authorization'].split(' ')
    if len(header_part) != 2 :
         abort(401)
    return header_part[1]

#this is can be used as funcation pointer .. this is get called first then it will call back actual endpoint
def req_auth(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        jwt = get_token_auth()
        return func(jwt,*args, **kwargs)
        
    return wrapper

@app.route('/headers', methods=['GET']) # redirect URL from auth0 after sucess
@req_auth
def headers(jwt):
    print(jwt)
    return 'Not Implemented1'