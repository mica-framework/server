from flask import Blueprint, json, make_response
routes = Blueprint('routes', __name__)


def __create_response__(status_code, message=None, data=None):
    # response tuple for the make_response (body, status, headers)
    response_tuple = (json.dumps({
        'message': message,
        'data': data
    }), 200, None)
    return make_response(response_tuple)

# import the components
from .docker import *
from .log import *
from .attack import *
