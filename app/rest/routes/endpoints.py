# coding: utf-8

import logging
import json
import time
import datetime
import os
import pandas as pd
from threading import Thread
import pickle

from flask_restplus import Resource
from flask import request

from rest.routes.api_definition import api
from rest.routes.serializers import turbofan_data





ns_latest = api.namespace('api', description='Entry Point')

@ns_latest.route("/test")
class GenericExample(Resource):

    def get(self):

        result = {"result":True, "type": "test", "data":str(request)}
        return result
    
    def post(self):


        result = {"result":True, "type": "test", "data":str(request)}
        return result

    def delete(self):


        result = {"result":True, "type": "test", "data":str(request)}
        return result

    def put(self):


        result = {"result":True, "type": "test", "data":str(request)}
        return result


@ns_latest.route("/aircraft/<string:aircraftid>")
class Aircraft(Resource):

    def get(self, aircraftid=None):
        import datetime
        from rest.flask_factory import engine
        threshold=20
        aircrafts = engine.execute(
            '''select * from flotte where "Nom de l'appareil"=%(aircraftid)s''',
            {"aircraftid": aircraftid}
        ).fetchall()
        query = '''
            select RUL,ts
            from rultrack r
            where r.aircraftid=%(aircraftid)s
            order by ts asc
        '''
        aircraft_res = {}
        for aircraft in aircrafts:
            aircraftid = aircraft[2]
            aircraft_type = aircraft[1]
            res = engine.execute(query, {"aircraftid": aircraftid}).fetchall()
            ruls = [res[i][0] for i in range(len(res))]
            ts = [str(res[i][1]) for i in range(len(res))]
            if(len(res)==0):
                aircraft_res = {"name": aircraftid, "aircraft_type": aircraft_type, "status" : "undefined", "rul": [], "timeseries" : []}
            else:
                status= "healthy"
                if(ruls[-1]<threshold):
                    status="in danger"
                aircraft_res = {
                    "status": status,
                    "name": aircraftid,
                    "aircraft_type": aircraft_type,
                    "rul": ruls,
                    "timeseries": ts
                }
        return aircraft_res

    @api.expect(turbofan_data, validate=True)
    def post(self, aircraftid=None):
        threshold=20
        from rest.flask_factory import predictive_maintenance_model
        from rest.flask_factory import engine
        sensors = dict(api.payload)
        ts = datetime.datetime.strptime(api.payload["TimeStamp"], "%Y-%m-%d %H:%M:%S.%f")
        del sensors["TimeStamp"]
        df = pd.DataFrame([sensors])
        print(df)
        print(ts)

        RUL = predictive_maintenance_model.predict(df)[0]

        query='''
        INSERT INTO rultrack (aircraftid, rul, ts)
        VALUES (%(aircraftid)s, %(RUL)s, %(ts)s)
        '''
        engine.execute(query, {"aircraftid": aircraftid, "RUL": RUL, "ts": str(ts)})
        if (RUL<20):
            from utils.email import send_email
            send_email(aircraftid, RUL)
        return {"result" : True, "RUL": RUL, "aircraftid": aircraftid}
    def delete(self, aircraftid=None):
        from rest.flask_factory import engine
        try:
            query='''delete from rultrack where aircraftid=%(aircraftid)s'''
            engine.execute(query, {"aircraftid": aircraftid})
            return {"result": True}
        except Exception as e:
            return {"result": False, "exception": str(e)}


@ns_latest.route("/aircraft/")
class Aircrafts(Resource):

    def get(self):
        import datetime
        from rest.flask_factory import engine
        threshold=20
        aircrafts = engine.execute("select * from flotte").fetchall()
        query = '''
            select RUL,ts
            from rultrack r
            where r.aircraftid=%(aircraftid)s
            order by ts asc
        '''
        aircrafts_res = []
        for aircraft in aircrafts:
            aircraftid = aircraft[2]
            aircraft_type = aircraft[1]
            res = engine.execute(query, {"aircraftid": aircraftid}).fetchall()
            ruls = [res[i][0] for i in range(len(res))]
            ts = [str(res[i][1]) for i in range(len(res))]
            if(len(res)==0):
                aircrafts_res.append({"name": aircraftid, "aircraft_type": aircraft_type, "status" : "undefined", "rul": [], "timeseries" : []})
            else:
                status= "healthy"
                if(ruls[-1]<threshold):
                    status="in danger"
                aircraft_res = {
                    "status": status,
                    "name": aircraftid,
                    "aircraft_type": aircraft_type,
                    "rul": ruls,
                    "timeseries": ts
                }
                aircrafts_res.append(aircraft_res)
        return aircrafts_res


@ns_latest.route("/flight/<int:day>/<int:month>/<int:year>")
class Flight(Resource):

    def get(self, day=25,
            month=1,
            year=2020):
        from utils.scraping import get_flights_realtime
        try :
            return get_flights_realtime(day, year, month)
        except Exception as e:
            import traceback
            return {"error": str(e), "stacktrace": traceback.format_exc()}