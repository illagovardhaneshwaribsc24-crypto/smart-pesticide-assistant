def get_recommendation(disease):
    data = {
        "rust": "Use sulfur-based fungicide",
        "blight": "Use copper oxychloride",
        "leaf spot": "Use neem oil spray"
    }

    return data.get(disease.lower(), "Consult agricultural expert")