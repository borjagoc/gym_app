import json
from flask import request, _request_ctx_stack
from functools import wraps
from jose import jwt
from urllib.request import urlopen


AUTH0_DOMAIN = 'dev-9-hxj2sw.us.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'sweat'

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

# To get the token from the Authorization Header and check for malformations
def get_token_auth_header():
    auth = request.headers.get('Authorization', None)
    if auth is None:
        raise AuthError('Authorization is not present in the header', 401)
    else:
        header_parts = auth.split()
        if header_parts[0].lower() != 'bearer':
            raise AuthError('Authorization header must start with "Bearer"', 401)
        elif len(header_parts) != 2:
            raise AuthError('Authorization header must be formed by "Bearer" + Token')
        else:
            token = header_parts[1]
            return token
        

# Checking that the payload in the JWT includes the right permissions
def check_permissions(permission, payload):
    if 'permissions' not in payload:
        raise AuthError('Permissions are not included in the payload', 400 )
    elif permission not in payload['permissions']:
        raise AuthError('The user does not have permission to perform the requested action', 403 )
    return True


'''
To verify the JWT:
    !!NOTE urlopen has a common certificate error described here: https://stackoverflow.com/questions/50236117/scraping-ssl-certificate-verify-failed-error-for-http-en-wikipedia-org
'''

# Verifying the authenticity of the JWT
def verify_decode_jwt(token):
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)

    rsa_key = {}

    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )

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


# Implementing the decorator to apply all checks
def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator
