from pathlib import Path

import numpy as np
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_FILE = DATA_DIR / "corporate_data.csv"


def generate_dataset(rows=10000):
    np.random.seed(42)

    rd_spend = np.random.uniform(10000, 500000, rows)
    admin_cost = np.random.uniform(10000, 300000, rows)
    marketing_spend = np.random.uniform(10000, 500000, rows)

    profit = (
            0.55 * rd_spend
            + 0.30 * marketing_spend
            - 0.40 * admin_cost
            + 50000
    )

    noise = np.random.normal(0, 25000, rows)
    profit = profit + noise

    df = pd.DataFrame({
        "rd_spend": rd_spend.round(2),
        "admin_cost": admin_cost.round(2),
        "marketing_spend": marketing_spend.round(2),
        "profit": profit.round(2),
    })

    return df


def main():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    df = generate_dataset(rows=10000)
    df.to_csv(DATA_FILE, index=False)

    print("Dataset generated successfully.")
    print(f"File: {DATA_FILE}")
    print(f"Rows: {len(df)}")
    print(f"Columns: {list(df.columns)}")
    print("\nFirst 5 rows:")
    print(df.head())


if __name__ == "__main__":
    main()