from flask_restplus import fields
from rest.routes.api_definition import api


turbofan_data = api.model('TurbofanData', {
    "Sensor_1": fields.Float(required=True, description="T2 Total temperature at fan inlet", example= 1),
    "Sensor_2": fields.Float(required=True, description="T24 Total temperature at LPC outlet ", example= 1),
    "Sensor_3": fields.Float(required=True, description="T30 Total temperature at HPC outlet ", example= 1),
    "Sensor_6": fields.Float(required=True, description="P15 Total pressure in bypass-duct", example= 1),
    "Sensor_7": fields.Float(required=True, description="P30 Total pressure at HPC outlet", example= 1),
    "Sensor_8": fields.Float(required=True, description="Nf Physical fan speed", example= 1),
    "Sensor_10": fields.Float(required=True, description="epr Engine pressure ratio (P50/P2)", example= 1),
    "Sensor_11": fields.Float(required=True, description="Ps30 Static pressure at HPC outlet", example= 1),
    "Sensor_12": fields.Float(required=True, description="phi Ratio of fuel flow to Ps30", example= 1),
    "Sensor_13": fields.Float(required=True, description="NRf Corrected fan speed", example= 1),
    "Sensor_14": fields.Float(required=True, description="NRc Corrected core speed", example= 1),
    "Sensor_16": fields.Float(required=True, description="farB Burner fuel-air ratio", example= 1),
    "Sensor_19": fields.Float(required=True, description="PCNfR_dmd Demanded corrected fan speed", example= 1),
    "Sensor_20": fields.Float(required=True, description="W31 HPT coolant bleed", example= 1),
    "Sensor_21": fields.Float(required=True, description="W32 LPT coolant bleed", example= 1),
    "TimeStamp": fields.DateTime(required=True, description="datetime for the record", example="1984-06-07T00:00:00")
    })