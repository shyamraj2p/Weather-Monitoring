import requests
import sqlite3
import time

# Define the API key and cities for which you want to fetch weather data
API_KEY = "81528908afc09eb2538ede5aff17286c"  # Replace with your actual API key
cities = {
    'Delhi': {'lat': 28.6667, 'lon': 77.2167},
    'Mumbai': {'lat': 19.0760, 'lon': 72.8777},
    'Chennai': {'lat': 13.0827, 'lon': 80.2707},
    'Bangalore': {'lat': 12.9716, 'lon': 77.5946},
    'Kolkata': {'lat': 22.5726, 'lon': 88.3639},
    'Hyderabad': {'lat': 17.3850, 'lon': 78.4867}
}

# Initialize the SQLite database and create the necessary table
def init_db():
    conn = sqlite3.connect('weather_data.db')
    cursor = conn.cursor()

    # Create a table to store weather data
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

# Fetch weather data from OpenWeatherMap API
def fetch_weather(city):
    lat, lon = cities[city]['lat'], cities[city]['lon']
    url = f'http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric'
    
    response = requests.get(url)

    # Check for successful response
    if response.status_code != 200:
        print(f"Error fetching data for {city}. HTTP Status Code: {response.status_code}")
        return None, None, None, None, None

    data = response.json()
    
    # Check if 'main' key exists in the response
    if 'main' not in data or 'temp' not in data['main'] or 'feels_like' not in data['main']:
        print(f"Invalid response for {city}. Response: {data}")
        return None, None, None, None, None

    temp = data['main']['temp']
    feels_like = data['main']['feels_like']
    weather_condition = data['weather'][0]['main']
    timestamp = data['dt']  # Unix timestamp
    readable_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp))
    print(f"Fetched data for {city}:")
    print(f"Weather Condition: {weather_condition}")
    print(f"Temperature: {temp:.2f}°C")
    print(f"Feels Like: {feels_like:.2f}°C")
    print(f"Last Updated: {readable_time}")
    
    return city, temp, feels_like, weather_condition, timestamp

# Check for user-defined thresholds (for temperature alerts)
def check_thresholds(city, temp):
    threshold = 35  # Example threshold for temperature in Celsius
    if temp > threshold:
        print(f"ALERT: Temperature in {city} exceeded {threshold}°C! Current temp: {temp}°C")

# Main function to run the weather monitoring system
def main():
    init_db()  # Initialize the database

    # Fetch weather data every 5 minutes (300 seconds)
    while True:
        for city_name in cities.keys():
            city, temp, feels_like, weather_condition, timestamp = fetch_weather(city_name)
            
            # Check if fetch_weather returned valid data
            if city is None:
                print(f"Skipping {city_name} due to error fetching data.")
                continue
            
            # Insert the weather data into the database
            insert_weather_data(city, temp, feels_like, weather_condition, timestamp)
            print(f"Inserted weather data for {city_name} into the database.")

            # Check for alerts
            check_thresholds(city, temp)
        
        # Wait for 5 minutes before the next API call
        print("Waiting for 5 minutes before the next round of weather data fetch...")
        time.sleep(300)

# Run the main function
if __name__ == "__main__":
    main()
