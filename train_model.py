import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
import joblib

df = pd.read_csv('shipping_history.csv')

X = df.drop('final_rate', axis=1)
y = df['final_rate']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=67)

model = xgb.XGBRegressor(
    n_estimators=1000, 
    learning_rate=0.05, 
    max_depth=6, 
    random_state=67
)

model.fit(
    X_train, y_train,
    eval_set=[(X_test, y_test)],
    verbose=False
)

predictions = model.predict(X_test)
mae = mean_absolute_error(y_test, predictions)
r2 = r2_score(y_test, predictions)

print(f"--- RAPORT TRENINGU ---")
print(f"Średni błąd (MAE): {round(mae, 2)} PLN")
print(f"Dokładność (R2 Score): {round(r2 * 100, 2)}%")

joblib.dump(model, 'freight_predictor_model.pkl')
print("Model zapisany jako 'freight_predictor_model.pkl'")