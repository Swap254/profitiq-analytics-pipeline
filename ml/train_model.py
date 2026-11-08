from pathlib import Path
import pickle

import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
MODEL_DIR = BASE_DIR / "model"

DATA_FILE = DATA_DIR / "corporate_data.csv"
MODEL_FILE = MODEL_DIR / "random_forest_model.pkl"


def load_data():
    df = pd.read_csv(DATA_FILE)

    required_columns = [
        "rd_spend",
        "admin_cost",
        "marketing_spend",
        "profit",
    ]

    missing_columns = [
        column for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    return df


def train_model(df):
    features = [
        "rd_spend",
        "admin_cost",
        "marketing_spend",
    ]

    X = df[features]
    y = df["profit"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
    )

    model = RandomForestRegressor(
        n_estimators=100,
        random_state=42,
        n_jobs=-1,
    )

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    mae = mean_absolute_error(y_test, predictions)
    rmse = mean_squared_error(
        y_test,
        predictions,
    ) ** 0.5
    r2 = r2_score(y_test, predictions)

    print("\nModel Evaluation")
    print("----------------")
    print(f"MAE : {mae:.2f}")
    print(f"RMSE: {rmse:.2f}")
    print(f"R²  : {r2:.4f}")

    return model


def save_model(model):
    MODEL_DIR.mkdir(parents=True, exist_ok=True)

    with open(MODEL_FILE, "wb") as file:
        pickle.dump(model, file)

    print(f"\nModel saved to: {MODEL_FILE}")


def main():
    print("Loading training data...")
    df = load_data()

    print(f"Dataset shape: {df.shape}")

    model = train_model(df)
    save_model(model)

    print("\nTraining completed successfully.")


if __name__ == "__main__":
    main()