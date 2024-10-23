import sqlite3
import pandas as pd
# Initialize the SQLite database
def init_db():
    conn = sqlite3.connect('weather_data.db')
    cursor = conn.cursor()

    # Create a table for weather data
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS weather_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city TEXT,
            temperature REAL,
            feels_like REAL,
            weather_condition TEXT,
            timestamp INTEGER
        )
    ''')
    conn.commit()
    conn.close()

# Insert weather data into the database
def insert_weather_data(city, temp, feels_like, weather_condition, timestamp):
    conn = sqlite3.connect('weather_data.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO weather_data (city, temperature, feels_like, weather_condition, timestamp)
        VALUES (?, ?, ?, ?, ?)
    ''', (city, temp, feels_like, weather_condition, timestamp))
    
    conn.commit()
    conn.close()

# Retrieve daily weather summary
def get_daily_summary():
    conn = sqlite3.connect('weather_data.db')
    query = '''
        SELECT city, 
               DATE(timestamp, 'unixepoch') as day, 
               AVG(temperature) as avg_temp, 
               MAX(temperature) as max_temp, 
               MIN(temperature) as min_temp, 
               weather_condition
        FROM weather_data
        GROUP BY city, day
    '''
    df = pd.read_sql(query, conn)
    conn.close()
    return df
