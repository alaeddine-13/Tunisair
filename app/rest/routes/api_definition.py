import logging
from flask_restplus import Api
from werkzeug.exceptions import NotFound

log = logging.getLogger(__name__)

api = Api(
    #version=settings.get("API_VERSION","1.0"), 
    #title=settings.get("API_TITLE","data Engine API"),
    #description=settings.get("API_DESC","data"),
    #authorizations=authorizations,
    #decorators=decorators
    )


@api.errorhandler
def default_error_handler(e):
    """Default Error Handles
    
    Args:
        e (Exception): Any exeption generated
    
    Returns:
        json: A proper json message
    """
    message = 'An unhandled exception occurred.'
    log.exception(message)
    print(type(message))

    return {'message': message, 'message': message.specific}, 500
    #return {'message': message}, 500

    

@api.errorhandler(NotFound)
def handle_no_result_exception(error):
    '''Return a custom not found error message and 404 status code'''
    return {'message': error.specific}, 404