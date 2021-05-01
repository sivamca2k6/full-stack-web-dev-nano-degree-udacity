import json
from flask import request, _request_ctx_stack
from functools import wraps
from jose import jwt
from urllib.request import urlopen


#-------------- Auth0 Config----------------
class AuthConfig:
    AUTH0_DOMAIN = 'sivamca2k6.au.auth0.com'
    ALGORITHMS = ['RS256']
    API_AUDIENCE = 'UdaCastingAPI' 

    casting_agency_assistant_token = {
    'Authorization': "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkNBVDNyM0s2TE4wY0otbDE0Y0VDQSJ9.eyJpc3MiOiJodHRwczovL3NpdmFtY2EyazYuYXUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYwODRkYWYzMmMwMTVhMDA2OTFhNGNmNiIsImF1ZCI6IlVkYUNhc3RpbmdBUEkiLCJpYXQiOjE2MTk4NzUyOTksImV4cCI6MTYxOTk2MTY5OSwiYXpwIjoiYm5PUDZrYVZtaXc5YWJDM2RBZHZCRVhra0ZQU1FySzAiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbInZpZXc6YWN0b3JzIiwidmlldzptb3ZpZXMiXX0.6UA1U7qi73xb2YI8WEUtCsOKQKX0iV1BD7iTo5KUQNYSnK6Wy3LwF_mfOjEGRHUHxe2UWazUEDIYHEGX1YoTlbaBorIaQX9AEs1EXVNCAXD3GOvQBuVW1EewZ4jAAFOO0fxQdksU8D_9PlcuVpSYwzhtfcrLwWBsSNqZL18Ijb5rM1dMyhvVt4QWfyvEt4zRtCWdWQc-TSDxqCsbXCdLFdVFpf6VEHmljwuDLGVjppygQaz5xf7JJuBXKH6rWOEzsw3BsEFI4oiR8-sx5aywE9FzdWhx2NXhY3rFH6B-5FpK2_6Dbeap7X2QzPpmKdfdvL-4lfcTrz20dpzRZZAvAw"}

    casting_agency_director_token = {
    'Authorization': "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkNBVDNyM0s2TE4wY0otbDE0Y0VDQSJ9.eyJpc3MiOiJodHRwczovL3NpdmFtY2EyazYuYXUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYwODRlYTFkMDgxYWZmMDA2OTJiMjc0YiIsImF1ZCI6IlVkYUNhc3RpbmdBUEkiLCJpYXQiOjE2MTk4NzU3MTksImV4cCI6MTYxOTk2MjExOSwiYXpwIjoiYm5PUDZrYVZtaXc5YWJDM2RBZHZCRVhra0ZQU1FySzAiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImNyZWF0ZTphY3RvciIsImRlbGV0ZTphY3RvciIsInVwZGF0ZTphY3RvciIsInVwZGF0ZTptb3ZpZSIsInZpZXc6YWN0b3JzIiwidmlldzptb3ZpZXMiXX0.vfGlz057n4W1MVe9dKJKHOVIPhvbpu_86-3T7Lposbv1w6Iw859qvJub9hscuzX6uGHKIzA1uXKAG1Wc-EE-WfXtaLdGrdFYEJyr-0YrnM79b4CAU1cUgsrpjiChUrYbSLxRV-JUAnBuD1b7k8vEsfqopGR0159jk9J2gMZVhRRYEga3oEUlVarGswmwevNUFidLq9wH-4f3uGrhWgc8pvBg4UkudmZvqpCrY8Hu753t6rqmG04QckT1Wd3dbvblhU6Vqwz5uPjPP54fpCA61RfdifNrVZ4ec_HF21tPoYUNN7jvGN2_TSGyxomMBds_iRCZVrHMQvnVhpcbkPmLJA"}

    casting_agency_producer_token = {
    'Authorization': "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkNBVDNyM0s2TE4wY0otbDE0Y0VDQSJ9.eyJpc3MiOiJodHRwczovL3NpdmFtY2EyazYuYXUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYwODRmNDNmMTMwNTMyMDA3MGJjMzdkZCIsImF1ZCI6IlVkYUNhc3RpbmdBUEkiLCJpYXQiOjE2MTk4NzU4ODcsImV4cCI6MTYxOTk2MjI4NywiYXpwIjoiYm5PUDZrYVZtaXc5YWJDM2RBZHZCRVhra0ZQU1FySzAiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImNyZWF0ZTphY3RvciIsImNyZWF0ZTptb3ZpZSIsImRlbGV0ZTphY3RvciIsImRlbGV0ZTptb3ZpZSIsInVwZGF0ZTphY3RvciIsInVwZGF0ZTptb3ZpZSIsInZpZXc6YWN0b3JzIiwidmlldzptb3ZpZXMiXX0.oVHa5uClA1fvImdh-TSdphI5WfQl9vom4hcl-mU0bw36sP8nVDM9XWBl98u0CVEi23sHD31x3jp_hmqZuz-3cf-wmA4kwtjldEhOiKwukxDHLMGwH-z3sp_kVnJ8C5cNWSZUZ90tZ_3u1MAMZpyH509Oaa8q0zNfVRpmHKt_cDkBVEvCfnfJbQOZz_qj1b9Q91GDBvDfsBvRmMP1hBDIfdTHm6dCyyxDIrUPK6lNFzbRpoxHnhNb5OpZdvesMMs-EadUf0Dhu4K_fPwcnHQ6VU7d8Ofm01C1fNa89VvwikUfdhdsDuPs3k7dvbjZE0LqGxr6ePsC2tD5wliRMpGfRQ"}


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
    jsonurl = urlopen(f'https://{AuthConfig.AUTH0_DOMAIN}/.well-known/jwks.json') 
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
                algorithms=AuthConfig.ALGORITHMS,
                audience=AuthConfig.API_AUDIENCE,
                issuer='https://' + AuthConfig.AUTH0_DOMAIN + '/'
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
        permission: string permission
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
    @INPUTS => permission: string permission 
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