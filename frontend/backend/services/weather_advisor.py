def get_weather_advice(temp, humidity, rain):
    advice = []

    if rain > 60:
        advice.append("Rain probability is high. Avoid pesticide spraying.")

    if temp > 35:
        advice.append("Spray during morning or evening.")

    if humidity > 80:
        advice.append("High fungal disease risk detected.")

    if not advice:
        advice.append("Weather conditions are suitable.")

    return advice
