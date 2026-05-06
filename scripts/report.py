from datetime import datetime

import pandas as pd
import os
import logging


try:
    logging.basicConfig(level=logging.INFO)
    logging.info("Starting report generation...")

    # Ensure output directory exists
    os.makedirs("output", exist_ok=True)

 #   print("Loading data...")
    logging.info("Loading data...")

    df = pd.read_parquet("data/sample_data.parquet")
    #df.loc[0, "price"] = -10.0 Ha ido y ha saltado el error en la pipeline

#    print("Processing data...")
    logging.info("Processing data...")

    if (df["price"] < 0).any():
        raise ValueError("Price cannot be negative.")
    

    df["revenue"] = df["price"] * df["qty"]

    # Compute summary
    summary = df.groupby("category").agg(
        total_revenue=("revenue", "sum"),
        total_quantity=("qty", "sum"),
        avg_price=("price", "mean"),
        transaction_count=("qty", "count")
    ).reset_index()

#    print("Saving report...")
    logging.info("Saving report...")
    summary.to_csv("output/report.csv", index=False)
    summary.to_json("output/report.json", orient="records")
    summary.to_parquet("output/report.parquet")

    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    summary.to_csv(f"output/report_{timestamp}.csv", index=False)


  #  print("✅ Report generated at output/report.csv")
    logging.info("Report generation completed successfully.")

except Exception as e:
    logging.error(f"An error occurred: {e}")
    print(f"❌ An error occurred: {e}")

