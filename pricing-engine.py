import pandas as pd
import yfinance as yf

def get_live_fuel_price():
    try:
        oil = yf.Ticker("BZ=F")
        current_price = oil.history(period="1d")['Close'].iloc[-1]
        
        estimated_pln_price = (current_price * 0.08)  
        return round(estimated_pln_price, 2)
    except:
        return 6.50

def calculate_base_costs(distance, fuel_price, consumption=30, driver_km_rate=0.8, maintenance_km_rate=0.5):
    fuel_cost = (distance / 100) * consumption * fuel_price
    driver_cost = distance * driver_km_rate
    maintenance_cost = distance * maintenance_km_rate
    
    total_base_cost = fuel_cost + driver_cost + maintenance_cost
    return round(total_base_cost, 2)

today_price = get_live_fuel_price()
print(f"Aktualna cena paliwa (estymowana): {today_price} PLN")
total_cost = calculate_base_costs(1000, today_price)
print(f"Koszt trasy 1000km przy dzisiejszych cenach: {total_cost} PLN")