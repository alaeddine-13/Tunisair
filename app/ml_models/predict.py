from joblib import load
from sklearn import preprocessing
from sklearn.preprocessing import StandardScaler
from sklearn import ensemble
from sklearn.ensemble import GradientBoostingRegressor
from sklearn import model_selection
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV

model = load('predictive_maintenance.joblib')

test = pd.read_csv('test_FD001.txt', sep=" ", header=None, names = column_names_)
vars_to_drop = ["Sensor_"+str(i) for i in [5, 15, 9, 17, 4, 18]]
vars_to_drop = vars_to_drop + ["_", "__", "UnitNumber", "Cycle", "Op_Setting_1", "Op_Setting_2", "Op_Setting_3"]
test = test.drop(vars_to_drop, axis = 1)
prediction = model.predict(test)
y = open("RUL_FD001.txt","r").read().split("\n")[:-1]
y = [int(i.replace(" ", "")) for i in y]

plt.scatter([i for i in range(len(y))], y, marker = ".")
plt.scatter([i for i in range(len(prediction))], prediction, c = "red", marker = ".")
plt.show()

prediction = [str(i) for i in prediction]

open("res.txt", "w").write("\n".join(prediction))