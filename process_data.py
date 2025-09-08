import pandas as pd


files = [
    "data/daily_sales_data_0.csv",
    "data/daily_sales_data_1.csv",
    "data/daily_sales_data_2.csv"
]

df = pd.concat([pd.read_csv(f) for f in files])

df = df[df["product"] == "pink morsel"]


df["numeric_price"] = df["price"].str.replace('$', '').astype(float)


df["sales"] = df["quantity"] * df["numeric_price"]

df["sales"] = "$" + df["sales"].round(2).astype(str)


final_df = df[["sales", "date", "region"]]


final_df.to_csv("data/processed_sales_data.csv", index=False)

print("Processed sales data saved  to data/processed_sales_data.csv")
