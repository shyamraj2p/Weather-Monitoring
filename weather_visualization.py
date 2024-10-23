import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Function to fetch daily summaries from the database
def fetch_daily_summaries():
    conn = sqlite3.connect('weather_data.db')
    query = '''
        SELECT city, day, avg_temp, max_temp, min_temp, dominant_condition 
        FROM daily_summary
    '''
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Function to plot daily weather summaries
def plot_daily_summary(city):
    df = fetch_daily_summaries()
    city_data = df[df['city'] == city]

    if city_data.empty:
        print(f"No data found for {city}.")
        return

    # Plotting the temperature trends with scatter plots for clearer visibility
    plt.figure(figsize=(12, 8))  # Increased figure size for better visibility
    plt.scatter(city_data['day'], city_data['avg_temp'], label='Avg Temp (°C)', color='blue', marker='o')
    plt.scatter(city_data['day'], city_data['max_temp'], label='Max Temp (°C)', color='red', marker='x')
    plt.scatter(city_data['day'], city_data['min_temp'], label='Min Temp (°C)', color='green', marker='^')

    plt.xlabel('Day')
    plt.ylabel('Temperature (°C)')
    plt.title(f'Daily Weather Summary for {city}')
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.grid()

    # Setting limits to zoom in on the temperature values
    plt.ylim(city_data['min_temp'].min() - 5, city_data['max_temp'].max() + 5)  # Adjusting limits for zoom effect
    plt.xlim(city_data['day'].min(), city_data['day'].max())

    plt.show()

# Function to show temperature alerts over time
def plot_alerts():
    conn = sqlite3.connect('weather_data.db')
    query = '''
        SELECT city, timestamp, temperature 
        FROM weather_data
        WHERE temperature > 35
    '''
    df = pd.read_sql(query, conn)
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
    
    conn.close()

    if df.empty:
        print("No alerts found.")
        return

    plt.figure(figsize=(12, 8))  # Increased figure size for better visibility
    for city in df['city'].unique():
        city_data = df[df['city'] == city]
        plt.scatter(city_data['timestamp'], city_data['temperature'], label=city, marker='o')

    plt.axhline(y=35, color='r', linestyle='--', label='Alert Threshold (35°C)')
    plt.xlabel('Timestamp')
    plt.ylabel('Temperature (°C)')
    plt.title('Temperature Alerts (Above 35°C)')
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.grid()

    # Setting limits to zoom in on the temperature alerts
    plt.ylim(df['temperature'].min() - 5, df['temperature'].max() + 5)  # Adjusting limits for zoom effect
    plt.xlim(df['timestamp'].min(), df['timestamp'].max())

    plt.show()

# Main visualization menu
def visualize_data():
    print("Weather Data Visualization")
    print("1. Plot Daily Summary for a City")
    print("2. Plot Temperature Alerts")
    choice = input("Choose an option (1 or 2): ")

    if choice == '1':
        city = input("Enter the city name: ")
        plot_daily_summary(city)
    elif choice == '2':
        plot_alerts()
    else:
        print("Invalid choice")

if __name__ == "__main__":
    visualize_data()
