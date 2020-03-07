#!/usr/bin/env python
# coding: utf-8

from flask import Flask, request
from flask import jsonify
import json
import numpy as np
import os
import pandas as pd
import requests
import threading



# Import of the main flask app object, important
from rest.flask_factory import app, predictive_maintenance_model

DB = os.getenv('DB', None) 

PORT = os.getenv('PORT', 5000)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=PORT, threaded=True)