import pandas as pd
import yfinance as yf
import joblib
from datetime import datetime
import sys

try:
    model = joblib.load('freight_predictor_model.pkl')
except:
    print("Blad: Nie znaleziono pliku freight_predictor_model.pkl! Najpierw odpal trening.")
    sys.exit()

def get_live_fuel_price():
    try:
        oil = yf.Ticker("BZ=F")
        current_price = oil.history(period="1d")['Close'].iloc[-1]
        estimated_pln_price = (current_price * 0.07)  
        return round(estimated_pln_price, 2)
    except:
        return 6.50

def calculate_base_costs(distance, fuel_price, consumption=30, driver_km_rate=1.1, maintenance_km_rate=2):
    fuel_cost = (distance / 100) * consumption * fuel_price
    driver_cost = distance * driver_km_rate
    maintenance_cost = distance * maintenance_km_rate
    return round(fuel_cost + driver_cost + maintenance_cost, 2)

print("=== CARGO KING INTELLIGENT PRICING SYSTEM ===")
print("System ready. Fetching live market data...")

today_price = get_live_fuel_price()
print(f"Current estimated fuel price: {today_price} PLN/L")

while True:
    print("\n" + "="*50)
    user_input = input("Enter route distance in km (or type 'exit' to quit): ").strip().lower()

    if user_input == 'exit':
        print("Closing system... Standby.")
        break
    
    if not user_input:
        print("Error: Input cannot be empty!")
        continue

    try:
        distance_input = float(user_input.replace(',', '.'))

        if distance_input <= 0:
            print("Error: Distance must be a positive number!")
            continue
        
        if distance_input > 15000:
            print("Warning: Extreme distance detected. Results may be less accurate.")

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
        print(f"OFFER FOR ROUTE: {distance_input} km")
        print("-" * 40)
        print(f"Operational Costs:   {total_cost} PLN")
        print(f"Predicted Margin:    {predicted_margin_pct}% (+/- 3%)")
        print("-" * 40)
        print(f"MINIMUM PRICE:    {price_min} PLN (Margin: {margin_low}%)")
        print(f"SUGGESTED PRICE:  {price_mid} PLN (Margin: {predicted_margin_pct}%)")
        print(f"MAXIMUM PRICE:    {price_max} PLN (Margin: {margin_high}%)")
        print("-" * 40)
        
    except ValueError:
        print(f"Error: '{user_input}' is not a valid number. Please try again.")
        continue

print("System shutdown. Goodbye.")
