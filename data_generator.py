import pandas as pd
import random

def generate_freight_rates(n_samples=2000):
    data = []
    for _ in range(n_samples):
        distance = random.randint(200, 2500)
        fuel_price = round(random.uniform(6.50, 8.50), 2)
        month = random.randint(1, 12)
        day_of_week = random.randint(0, 6)
        
        rate_per_km = 7.0 
        
        if month in [11, 12]: rate_per_km *= 1.25  
        if day_of_week >= 4: rate_per_km *= 1.10  
        if fuel_price > 7.50: rate_per_km *= 1.05 

        rate_per_km += random.uniform(-0.5, 0.5)
        
        final_rate = round(distance * rate_per_km, 2)
        
        data.append([distance, fuel_price, month, day_of_week, final_rate])
    
    return pd.DataFrame(data, columns=['distance', 'fuel_price', 'month', 'day_of_week', 'final_rate'])

df = generate_freight_rates()
df.to_csv('shipping_history.csv', index=False)
print("Plik 'shipping_history.csv' wygenerowany!")