import pandas as pd

df = pd.read_csv("data/disease_data.csv")

def get_recommendation(disease):
    result = df[df["disease"].str.lower() == disease.lower()]

    if result.empty:
        return None

    return result.iloc[0].to_dict()