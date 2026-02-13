import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import pickle

df = pd.read_csv("shape_dataset.csv")

X = df[['ไหล่','อก','เอว','สะโพก','น้ำหนัก','ส่วนสูง']]
y = df['WHR']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

print("MSE:", mean_squared_error(y_test,y_pred))
print("R2 Score:", r2_score(y_test,y_pred))

pickle.dump(model, open("model.pkl","wb"))
print("บันทึก model.pkl เรียบร้อย")
