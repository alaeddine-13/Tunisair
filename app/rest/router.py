import traceback
import logging
from flask import Blueprint, request, Response
from flask_cors import CORS
from rest.routes.api_definition import api
import requests

from rest.routes.endpoints import ns_latest as ns_latest



log = logging.getLogger(__name__)
logging.getLogger('flask_cors').level = logging.DEBUG


def _configure_namespaces(api):
	api.add_namespace(ns_latest)


def configure_api(flask_app):
	blueprint = Blueprint('api', __name__)
	api.init_app(blueprint)
	_configure_namespaces(api)
	flask_app.register_blueprint(blueprint)

