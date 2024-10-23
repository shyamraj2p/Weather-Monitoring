# Threshold for temperature alert
alert_threshold = 35  # 35 degrees Celsius

# Check if the temperature exceeds the threshold
def check_thresholds(city, temp):
    if temp > alert_threshold:
        print(f"ALERT: {city} temperature exceeds {alert_threshold}°C!")
