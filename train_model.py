import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
import joblib
import matplotlib.pyplot as plt

df = pd.read_csv('shipping_history.csv')

df['fuel_costs'] = (df['distance'] / 100) * 30 * df['fuel_price']
df['operating_costs'] = df['distance'] * (df['driver_rate'] + 2)

df['total_costs'] = df['fuel_costs'] + df['operating_costs']
df['actual_margin_pln'] = df['final_rate'] - df['total_costs']

df['margin_percentage'] = (df['actual_margin_pln'] / df['final_rate']) * 100

X = df[['distance', 'month', 'day_of_week']]
y = df['margin_percentage']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=67)

model = xgb.XGBRegressor(
    n_estimators=500, 
    learning_rate=0.04, 
    max_depth=5, 
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
print(f"Średni błąd (MAE): {round(mae, 2)} %")
print(f"Dokładność (R2 Score): {round(r2 * 100, 2)}%")
xgb.plot_importance(model)
plt.show()

joblib.dump(model, 'freight_predictor_model.pkl')
print("Model zapisany jako 'freight_predictor_model.pkl'")