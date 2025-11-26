#importing libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import missingno as msno
import datetime
from datetime import datetime

# Drop column
df = df.drop(columns=['HCPCS'])

# Remove Close and Rejected Claims in status column
df = df[~df['Status'].isin(['Closed', 'Rejected'])]

# Convert blank/whitespace-only strings to NaN
df = df.replace(r'^\s*$', pd.NA, regex=True)

# Drop rows where ANY column has a null/blank value
df = df.dropna()

# Sort A to Z by Patient Name
df = df.sort_values(by="Patient Name")

# Remove rows where Balance is negative
df = df[df['Balance'] > 0]
df = df[df['Charge'] > 0]

# ---- Step 1: Calculate total charge by Invoice ----
summary = df.groupby("Invoice", as_index=False).agg(
    Total_Charge=("Charge", "sum")
)

# ---- Step 2: Merge total charge back into original file ----
df = df.merge(summary, on="Invoice", how="left")

# ---- Step 1: Calculate total balance by Invoice ----
summary = df.groupby("Invoice", as_index=False).agg(
    Total_Balance=("Balance", "sum")
)

# ---- Step 2: Merge total balance back into original file ----
df = df.merge(summary, on="Invoice", how="left")

# Remove duplicate invoices (keep first occurrence)
df = df.drop_duplicates(subset=["Invoice"], keep="first")

# Convert DOS From column to datetime
df["DOS From"] = pd.to_datetime(df["DOS From"], errors="coerce")

# Today's date as a pandas Timestamp
today_ts = pd.Timestamp(datetime.today().date())

# Calculate difference in days
df["Age of Claims"] = (today_ts - df["DOS From"]).dt.days

# Sort from 0 to infinity
df = df.sort_values(by="Age of Claims", ascending=True)

# Correct bucket logic
conditions = [
    (df["Age of Claims"] >= 0) & (df["Age of Claims"] <= 30),
    (df["Age of Claims"] > 30) & (df["Age of Claims"] <= 60),
    (df["Age of Claims"] > 60) & (df["Age of Claims"] <= 90),
    (df["Age of Claims"] > 90) & (df["Age of Claims"] <= 120),
    (df["Age of Claims"] > 120)
]

bucket_labels = [
    "Bucket - 1",
    "Bucket - 2",
    "Bucket - 3",
    "Bucket - 4",
    "Bucket - 5"
]

# Assign bucket column
df["Bucket"] = np.select(conditions, bucket_labels, default="Uncategorized")

output_path = '/content/Invoice_Clean.csv'
df.to_csv(output_path, index=False)
print(f"\n✅ Cleaned data saved successfully to: {output_path}")
