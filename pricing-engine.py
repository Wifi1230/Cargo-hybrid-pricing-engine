import pandas as pd

def calculate_base_costs(distance, fuel_price, consumption=30, driver_km_rate=0.8, maintenance_km_rate=0.5):
    fuel_cost = (distance / 100) * consumption * fuel_price
    driver_cost = distance * driver_km_rate
    maintenance_cost = distance * maintenance_km_rate
    
    total_base_cost = fuel_cost + driver_cost + maintenance_cost
    return round(total_base_cost, 2)

# TEST: Trasa 1000km, paliwo po 6.50 zł
print(f"Koszt bazowy trasy: {calculate_base_costs(1000, 6.50)} PLN")