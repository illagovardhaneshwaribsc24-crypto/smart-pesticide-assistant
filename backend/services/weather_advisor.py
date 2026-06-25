def get_weather_advice(temp, humidity, rain):
    if rain > 70:
        return "Avoid spraying pesticides today"
    elif humidity > 80:
        return "High disease risk, monitor crops closely"
    else:
        return "Normal farming conditions"