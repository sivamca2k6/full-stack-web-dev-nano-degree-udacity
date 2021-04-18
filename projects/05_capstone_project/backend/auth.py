import json
from flask import request, _request_ctx_stack
from functools import wraps
from jose import jwt
from urllib.request import urlopen


AUTH0_DOMAIN = 'sivamca2k6.au.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'UdaCoffeAPI'

## AuthError Exception
'''
AuthError Exception
A standardized way to communicate auth failure modes
'''
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


## Auth Header

'''
    Get Token from the Authorization Header and validate
    Authorization Header format : bearer  'token'
    return the token[1] part of the header
'''
def get_token_auth_header():
    #print(request.headers)
    #Obtains the Access Token from the Authorization Header
    auth = request.headers.get('Authorization', None)
    if not auth:
        raise AuthError({
            'code': 'authorization_header_missing',
            'description': 'Authorization header is expected.'
        }, 401)

    #split bearer and the token
    parts = auth.split()
    if parts[0].lower() != 'bearer':
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must start with "Bearer".'
        }, 401)

    elif len(parts) == 1: #AuthError if the header is malformed
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Token not found.'
        }, 401)

    elif len(parts) > 2: #AuthError if the header is malformed
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must be bearer token.'
        }, 401)

    token = parts[1]
    return token


'''
    @INPUTS =>  token: a json web token (string) from client
    return the decoded payload
    !!NOTE urlopen has a common certificate error described here: https://stackoverflow.com/questions/50236117/scraping-ssl-certificate-verify-failed-error-for-http-en-wikipedia-org
'''
def verify_decode_jwt(token):
    
    # To verify , gets token from auth0 server to validate aganist client one
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json') 
    jwks = json.loads(jsonurl.read())

    #kid from client call
    unverified_header = jwt.get_unverified_header(token)
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)

    #check Auth0 token with key id (kid),validate the claims
    rsa_key = {}
    for key in jwks['keys']: 
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }

    #validate and decode the payload from the token
    if rsa_key: 
        try: 
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )
            #print(payload)
            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please, check the audience and issuer.'
            }, 401)
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)
    raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to find the appropriate key.'
            }, 400)

'''
    @INPUTS
        permission: string permission (i.e. 'post:drink')
        payload: decoded jwt payload
    =>Note : RBAC settings in Auth0 need to be enabled.
'''
def check_permissions(permission, payload):
    #print(payload)
    #print(payload['permissions'])
    # raise an AuthError if permissions are not included in the payload
    if 'permissions' not in payload: 
                        raise AuthError({
                            'code': 'invalid_claims',
                            'description': 'Permissions not included in JWT.'
                        }, 400)

    #raise an AuthError if the requested permission string is not in the payload permissions array
    if permission not in payload['permissions']: 
        raise AuthError({
            'code': 'unauthorized',
            'description': 'Permission not found.'
        }, 403)
    return True

'''
    this decorator can be reused at multiple API endpoints
    @INPUTS => permission: string permission (i.e. 'post:drink')
    return the decorator which passes the decoded payload to the decorated method
'''
def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload) # validate claims and check the requested permission
            return f(payload, *args, **kwargs)
        return wrapper
    return requires_auth_decorator