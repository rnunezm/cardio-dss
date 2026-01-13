import pandas as pd

def clean_data(csv_path):
    df = pd.read_csv(csv_path)

    df = df[
        ["age", "gender", "height", "weight", "ap_hi",
         "cholesterol", "gluc", "smoke", "cardio"]
    ]

    df["age"] = (df["age"] / 365).astype(int)
    df["bmi"] = df["weight"] / ((df["height"] / 100) ** 2)
    df["blood_pressure"] = df["ap_hi"]
    df["diabetes"] = df["gluc"].apply(lambda x: 1 if x > 1 else 0)

    df = df.rename(columns={
        "gender": "sex",
        "smoke": "smoker",
        "cardio": "target"
    })

    df_final = df[
        ["age", "sex", "cholesterol", "blood_pressure",
         "smoker", "diabetes", "bmi", "target"]
    ]

    return df_final.dropna()
