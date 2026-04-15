import pandas as pd
import yfinance as yf
import joblib
from datetime import datetime

try:
    model = joblib.load('freight_predictor_model.pkl')
except:
    print("Błąd: Nie znaleziono pliku modelu! Najpierw odpal trening.")
    exit()

def get_live_fuel_price():
    try:
        oil = yf.Ticker("BZ=F")
        current_price = oil.history(period="1d")['Close'].iloc[-1]
        
        estimated_pln_price = (current_price * 0.08)  
        return round(estimated_pln_price, 2)
    except:
        return 6.50

def calculate_base_costs(distance, fuel_price, consumption=30, driver_km_rate=1.1, maintenance_km_rate=2):
    fuel_cost = (distance / 100) * consumption * fuel_price
    driver_cost = distance * driver_km_rate
    maintenance_cost = distance * maintenance_km_rate
    return round(fuel_cost + driver_cost + maintenance_cost, 2)

distance_input = 1200
today_price = get_live_fuel_price()
now = datetime.now()
current_month = now.month
current_day = now.weekday()

total_cost = calculate_base_costs(distance_input, today_price)

input_df = pd.DataFrame([[distance_input, current_month, current_day]], 
                        columns=['distance', 'month', 'day_of_week'])

predicted_margin_pct = round(float(model.predict(input_df)[0]), 2)

error_margin = 3.0
margin_low = round(predicted_margin_pct - error_margin, 2)
margin_high = round(predicted_margin_pct + error_margin, 2)

price_min = round(total_cost / (1 - (margin_low / 100)), 2)
price_mid = round(total_cost / (1 - (predicted_margin_pct / 100)), 2)
price_max = round(total_cost / (1 - (margin_high / 100)), 2)

print("-" * 40)
print(f"OFERTA DLA KLIENTA - TRASA {distance_input}km")
print("-" * 40)
print(f"Koszty operacyjne: {total_cost} PLN")
print(f"Przewidywana marża: {predicted_margin_pct}% (+/- 3%)")
print("-" * 40)
print(f"CENA MINIMALNA:  {price_min} PLN (Marża: {margin_low}%)")
print(f"CENA SUGEROWANA: {price_mid} PLN (Marża: {predicted_margin_pct}%)")
print(f"CENA MAKSYMALNA: {price_max} PLN (Marża: {margin_high}%)")
print("-" * 40)