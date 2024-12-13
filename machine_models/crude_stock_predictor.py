import os
import sys
import pandas as pd
import joblib
import numpy as np
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model_with_scalers.pkl")

model_package = joblib.load(MODEL_PATH)
scaler_feature = model_package['scaler_feature']
scaler_target = model_package['scaler_target']
model = model_package['model']

def predict_crude_stock(Date, Adj_Close, Close, Open, Volume):
    try:
        date = pd.to_datetime(Date)
        year = date.year
        month = date.month
        day_of_week = date.dayofweek

        month_sin = np.sin(2 * np.pi * month / 12)
        month_cos = np.cos(2 * np.pi * month / 12)

        df = pd.DataFrame([{
            'Adj_Close': Adj_Close,
            'Close': Close,
            'Open': Open,
            'Volume': Volume,
            'Year': year,
            'Month': month,
            'DayOfWeek': day_of_week,
            'Month_sin': month_sin,
            'Month_cos': month_cos
        }])

        scaled_features = scaler_feature.transform(df)
        scaled_prediction = model.predict(scaled_features)
        og_scale_prediction = scaler_target.inverse_transform(scaled_prediction)

        return json.dumps({
            'High': og_scale_prediction[0][0],
            'Low': og_scale_prediction[0][1]
        })

    except Exception as e:
        return json.dumps({"error": str(e)})

if __name__ == "__main__":
    try:
        Date = sys.argv[1]
        Adj_Close = float(sys.argv[2])
        Close = float(sys.argv[3])
        Open = float(sys.argv[4])
        Volume = float(sys.argv[5])

        result = predict_crude_stock(Date, Adj_Close, Close, Open, Volume)
        print(result)
    except Exception as e:
        print(json.dumps({"error": str(e)}))
