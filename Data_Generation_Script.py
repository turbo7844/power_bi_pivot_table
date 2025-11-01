import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# Параметры датасета
num_rows = 25_000_000  # 25 млн строк
chunk_size = 1_000_000  # Размер блока

# Списки возможных значений
countries = countries = [
    "USA", "UK", "Germany", "France", "Japan", "Canada", "Australia", "Brazil", "India", "China",
    "Italy", "Spain", "Mexico", "Indonesia", "Netherlands", "South Korea", "Turkey", "Saudi Arabia", 
    "Switzerland", "Argentina", "Sweden", "Nigeria", "Poland", "Belgium", "Thailand", "Austria", 
    "Norway", "United Arab Emirates", "Israel", "South Africa", "Denmark", "Malaysia", "Singapore", 
    "Philippines", "Egypt", "Finland", "Ireland", "Pakistan", "Greece", "Portugal", "Iraq", "Vietnam", 
    "Chile", "Czech Republic", "Romania", "Bangladesh", "Colombia", "Peru", "New Zealand", "Algeria", 
    "Kazakhstan", "Qatar", "Hungary", "Malta", "Morocco", "Angola", "Ecuador", "Slovakia", "Oman", 
    "Belarus", "Azerbaijan", "Sri Lanka", "Myanmar", "Tanzania", "Dominican Republic", "Kenya", 
    "Bulgaria", "Guatemala", "Cuba", "Tunisia", "Ghana", "Serbia", "Croatia", "Lebanon", "Lithuania", 
    "Costa Rica", "Jordan", "Panama", "Uruguay", "Uganda", "Nepal", "Latvia", "Slovenia", "Cambodia", 
    "Paraguay", "El Salvador", "Honduras", "Zimbabwe", "Cameroon", "Iceland", "Senegal", "Zambia", 
    "Cyprus", "Estonia", "Jamaica", "Trinidad and Tobago", "Botswana", "Namibia", "Rwanda", "Mozambique", "Mauritius", "Vanuatu"]

segments = ["Small Business", "Government", "Enterprise", "Individual", "Startups",
            "Non-Profit", "Education", "Healthcare", "Finance", "E-commerce",
            "Sport", "Retail Chains", "Freelancers", "Agriculture", "Hospitality"]

products = products = [
    "Stellar", "Pulse", "Nova", "Vega", "Quartz",
    "Aurora", "Blaze", "Cipher", "Dynamo", "Eclipse",
]
channels = ["Online", "Retail", "Wholesale", "Partner"]

manufacturers = [
    "Celestia", "Novaris", "Solvix", "Etheron", "Yralos",
    "Aetheris", "Borealis", "Cynexis", "Dynovix", "Eclipton",
]

# Коэффициенты для создания различий между группами
country_coef = {country: np.random.uniform(0.5, 2.0) for country in countries}
segment_coef = {segment: np.random.uniform(0.7, 1.5) for segment in segments}
product_coef = {product: np.random.uniform(0.6, 1.8) for product in products}
channel_coef = {channel: np.random.uniform(0.8, 1.7) for channel in channels}
manufacturer_coef = {manuf: np.random.uniform(0.5, 1.9) for manuf in manufacturers}

# Генерация случайных дат
def random_date(start_year=2020, end_year=2023):
    start = datetime(start_year, 1, 1)
    end = datetime(end_year, 12, 31)
    random_days = random.randint(0, (end - start).days)
    return (start + timedelta(days=random_days)).date()

# Генерация данных с учетом коэффициентов
def generate_data_chunk(num_rows_chunk):
    data = {
        "Date": [random_date() for _ in range(num_rows_chunk)],
        "Country": np.random.choice(countries, num_rows_chunk),
        "Channel": np.random.choice(channels, num_rows_chunk),
        "Manufacturer": np.random.choice(manufacturers, num_rows_chunk),
        "Product": np.random.choice(products, num_rows_chunk),
        "Segment": np.random.choice(segments, num_rows_chunk),
    }
    
    df = pd.DataFrame(data)
    
    # Генерация Units Sold с учетом коэффициентов
    units_base = np.random.randint(1, 10, num_rows_chunk)
    df["Units Sold"] = np.round(units_base * 
                               df["Country"].map(country_coef) * 
                               df["Segment"].map(segment_coef) * 
                               df["Product"].map(product_coef) * 
                               df["Channel"].map(channel_coef) * 
                               df["Manufacturer"].map(manufacturer_coef)).astype(int)
    
    # Генерация Gross Sales с разными коэффициентами
    sales_base = np.random.uniform(100, 10000, num_rows_chunk)
    df["Gross Sales"] = np.round(sales_base * 
                                df["Country"].map(country_coef) * 
                                df["Segment"].map(segment_coef) * 
                                df["Product"].map(product_coef) * 1.2 * 
                                df["Channel"].map(channel_coef) * 0.9 * 
                                df["Manufacturer"].map(manufacturer_coef), 2)
    
    # Генерация COGS с другими коэффициентами
    cogs_base = np.random.uniform(50, 5000, num_rows_chunk)
    df["COGS"] = np.round(cogs_base * 
                         df["Country"].map(country_coef) * 0.8 * 
                         df["Segment"].map(segment_coef) * 1.1 * 
                         df["Product"].map(product_coef) * 
                         df["Channel"].map(channel_coef) * 1.3 * 
                         df["Manufacturer"].map(manufacturer_coef) * 0.7, 2)
    
    return df

# Настройки экспорта
output_file = "sales_extra.csv"
export_params = {
    "sep": "|",
    "decimal": ",",
    "float_format": "%.2f",
    "index": False
}

# Генерация и сохранение
for i in range(0, num_rows // chunk_size):
    chunk = generate_data_chunk(chunk_size)
    if i == 0:
        chunk.to_csv(output_file, mode='w', header=True, **export_params)
    else:
        chunk.to_csv(output_file, mode='a', header=False, **export_params)
    print(f"Блок {i+1}/{(num_rows // chunk_size)} сохранён")

print(f"Файл {output_file} успешно создан")