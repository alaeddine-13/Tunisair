from flask import Flask, Response, request
from rest.router import configure_api
import requests
import os, sys
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask import g
import datetime
from ml_models.predictive_maintenance import train_model as predictive_maintenance_train_model
import threading


from joblib import load
from sklearn import preprocessing
from sklearn.preprocessing import StandardScaler
from sklearn import ensemble
from sklearn.ensemble import GradientBoostingRegressor
from sklearn import model_selection
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
import pandas as pd
import  sqlalchemy as db
import os

DB=os.getenv("DB")

engine = db.create_engine(DB, use_batch_mode=True)


app = Flask(__name__)

app.config['DEBUG'] = True


CORS(app, support_credentials=True)

settings  = app.config


#Adding routing and handling API functionability
configure_api(app)

predictive_maintenance_model = load('ml_models/predictive_maintenance.joblib')

@app.after_request
def after_request(response):
  response.headers.set('Access-Control-Allow-Origin', '*')
  response.headers.set('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.set('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  response.headers.set('Access-Control-Allow-Credentials', 'true')
  return response
