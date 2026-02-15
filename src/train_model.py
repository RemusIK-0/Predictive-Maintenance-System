import pandas as pd
import sqlite3
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score


def train_model():
    conn = sqlite3.connect("data/maintenance.db")
    df = pd.read_sql_query("SELECT * FROM telemetry", conn)
    conn.close

    if len(df) < 50:
        print("Not enought data yet, please run the simulator for a few more minutes")
        return
    
    x = df[['temperature', 'vibration', 'preasure']]
    y = df['failure_label']

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

    print("Training AI model started")
    model = RandomForestClassifier(n_estimators=100)
    model.fit(x_train, y_train)

    predictions = model.predict(x_test) 
    accuracy = accuracy_score(y_test, predictions)
    print(f"Model trained with an accuracy of {accuracy * 100:.2f}%")

    joblib.dump(model, 'data/model.pkl')
    print("Model saved as data/model.pkl")

if __name__ == "__main__":
    train_model()