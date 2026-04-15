import pandas as pd
import random
GAS_CONSUMPTION=30
CAR_COST_PER_KM=2

def generate_freight_rates(n_samples=2000):
    data = []
    for _ in range(n_samples):
        distance = random.randint(200, 2500)
        fuel_price = round(random.uniform(6.50, 8.50), 2)
        month = random.randint(1, 12)
        day_of_week = random.randint(0, 6)
        driver_rate=round(random.uniform(0.8, 1.2), 2)
        rate_per_km = ((GAS_CONSUMPTION*fuel_price/100)+driver_rate+CAR_COST_PER_KM)*1.2
        
        if month in [11, 12]: rate_per_km *= 1.25  
        if day_of_week >= 4: rate_per_km *= 1.10  

        rate_per_km += random.uniform(-0.5, 0.5)
        
        final_rate = round(distance * rate_per_km, 2)
        
        data.append([distance, fuel_price, month, day_of_week, driver_rate, final_rate])
    
    return pd.DataFrame(data, columns=['distance', 'fuel_price', 'month', 'day_of_week','driver_rate', 'final_rate'])

df = generate_freight_rates()
df.to_csv('shipping_history.csv', index=False)
print("Plik 'shipping_history.csv' wygenerowany!")