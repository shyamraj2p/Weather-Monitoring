import sqlite3
import pandas as pd
import time
from collections import Counter

# Function to calculate the dominant weather condition
def get_dominant_condition(conditions):
    # Count the frequency of weather conditions
    condition_count = Counter(conditions)
    # Get the most common condition
    dominant_condition = condition_count.most_common(1)[0][0]
    return dominant_condition

# Function to calculate daily weather summary
def calculate_daily_summary():
    conn = sqlite3.connect('weather_data.db')
    
    query = '''
        SELECT city, 
               DATE(timestamp, 'unixepoch') AS day, 
               AVG(temperature) AS avg_temp, 
               MAX(temperature) AS max_temp, 
               MIN(temperature) AS min_temp, 
               GROUP_CONCAT(weather_condition) AS conditions
        FROM weather_data
        GROUP BY city, day
    '''
    df = pd.read_sql(query, conn)
    df['dominant_condition'] = df['conditions'].apply(lambda x: get_dominant_condition(x.split(',')))
    
    conn.close()
    return df

# Function to store the daily summaries in a separate table
def store_daily_summaries():
    conn = sqlite3.connect('weather_data.db')
    cursor = conn.cursor()

    # Create a table for daily summaries if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS daily_summary (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city TEXT,
            day TEXT,
            avg_temp REAL,
            max_temp REAL,
            min_temp REAL,
            dominant_condition TEXT
        )
    ''')

    daily_summary = calculate_daily_summary()
    for index, row in daily_summary.iterrows():
        cursor.execute('''
            INSERT INTO daily_summary (city, day, avg_temp, max_temp, min_temp, dominant_condition)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (row['city'], row['day'], row['avg_temp'], row['max_temp'], row['min_temp'], row['dominant_condition']))
        # Print the daily summary values after inserting them into the database
        print(f"Daily Summary for {row['city']} on {row['day']}:")
        print(f"  Avg Temp: {row['avg_temp']:.2f}°C")
        print(f"  Max Temp: {row['max_temp']:.2f}°C")
        print(f"  Min Temp: {row['min_temp']:.2f}°C")
        print(f"  Dominant Condition: {row['dominant_condition']}")
        print("-" * 40)  # Separator for better readability

    conn.commit()
    conn.close()

# Alerting based on temperature thresholds
def alert_on_threshold(city, threshold=35, consecutive_count=2):
    alert_threshold = threshold
    conn = sqlite3.connect('weather_data.db')
    
    query = '''
        SELECT temperature 
        FROM weather_data 
        WHERE city = ? 
        ORDER BY timestamp DESC 
        LIMIT ?
    '''
    result = pd.read_sql(query, conn, params=(city, consecutive_count))
    conn.close()
    
    # Check if the temperature for the consecutive updates exceeds the threshold
    if len(result) == consecutive_count and all(result['temperature'] > alert_threshold):
        print(f"ALERT: Temperature in {city} exceeded {alert_threshold}°C for {consecutive_count} consecutive updates!")

# Monitor the database for temperature thresholds every few minutes
def monitor_thresholds(threshold=35, consecutive_count=2):
    while True:
        store_daily_summaries()  # Update daily summaries
        cities = ['Delhi', 'Mumbai', 'Chennai', 'Bangalore', 'Kolkata', 'Hyderabad']
        
        for city in cities:
            # Check if a temperature threshold is crossed
            alert_on_threshold(city=city, threshold=threshold, consecutive_count=consecutive_count)
        
        # Sleep for 5 minutes before the next check
        print("Monitoring thresholds... Waiting 5 minutes for next check.")
        time.sleep(300)

if __name__ == "__main__":
    monitor_thresholds()  # Start monitoring


