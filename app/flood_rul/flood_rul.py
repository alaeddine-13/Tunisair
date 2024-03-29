import requests as rq
import pandas as pd 
import datetime
import json

import  sqlalchemy as db
import sys


DB="postgres://opengovdatahackdb.cec7rz0ixyvl.us-east-1.rds.amazonaws.com:5432/postgres?user=dev&password=12345678"
engine = db.create_engine(DB, use_batch_mode=True)


target_var = ['Target_Remaining_Useful_Life']
index_columns_names =  ["aircraftId","Cycle"]
op_settings_columns = ["Op_Setting_"+str(i) for i in range(1,4)]
sensor_columns =["Sensor_"+str(i) for i in range(1,22)]
column_names = index_columns_names + op_settings_columns + sensor_columns


column_names_ = column_names + ["_", "__"]
# load data
test = pd.read_csv('test_FD004.txt', sep=" ", header=None, names = column_names_)

columns_to_drop=['Sensor_4','Sensor_5','Sensor_9','Sensor_15','Sensor_17','Sensor_18',]
test.drop(columns_to_drop, axis=1, inplace=True)

print(test.groupby('aircraftId').count())

sys.exit(0)

aircrafts = engine.execute('''select "Nom de l'appareil" from flotte''').fetchall()
print(aircrafts)
for aircraft in aircrafts:
	aircraft = aircraft[0]
	df=test[test['aircraftId']==aircraft]
	df.drop(['aircraftId','Cycle','Op_Setting_1','Op_Setting_2','Op_Setting_3','_','__'], axis=1, inplace=True)

	records=df.to_dict('records')
	time=datetime.datetime.strptime('2020-01-01 00:00:00.1', '%Y-%m-%d %H:%M:%S.%f')
	td = datetime.timedelta(days=1)
	result=[]
	for record in records:
	    record['TimeStamp']=str(time)
	    time = time + td
	    result.append(record)
	


	# In[74]:


	headers = {
	  'Content-Type': 'application/json'
	}
	if(len(result)>0):
		print(aircraft)
	for record in result:
		resp = rq.post('http://18.212.69.214:5000/api/aircraft/{}'.format(aircraft),headers=headers, data= json.dumps(record))
		#print(resp.text)



