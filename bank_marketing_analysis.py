
import pandas as pd
from pathlib import Path

# STEP 1: Locate the dataset and output folder
project_folder = Path(__file__).resolve().parent.parent
data_file = project_folder / "data" / "bank-additional-full.csv"
output_folder = project_folder / "Python Analysis" / "outputs"
output_folder.mkdir(parents=True, exist_ok=True)

# STEP 2: Load the dataset
df = pd.read_csv(data_file, sep=";")

print("\n========== ORIGINAL DATA ==========")
print("Dataset shape:", df.shape)
print("\nColumn names:")
print(df.columns.tolist())

# Confirm the final two columns are separate
print("\nCheck final two columns:")
print(df[["nr.employed", "y"]].head())

# STEP 3: Check the original data quality
print("\n========== DATA QUALITY CHECK ==========")
print("\nMissing values before cleaning:")
print(df.isnull().sum())

print("\nExact duplicate rows:", df.duplicated().sum())

# STEP 4: Standardize column names and text
df.columns = df.columns.str.strip().str.lower()

for col in df.select_dtypes(include=["object", "string"]).columns:
    df[col] = df[col].astype("string").str.strip()

# STEP 5: Convert numeric columns
numeric_columns = [
    "age", "duration", "campaign", "pdays", "previous",
    "emp.var.rate", "cons.price.idx", "cons.conf.idx",
    "euribor3m", "nr.employed"
]

for col in numeric_columns:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

# STEP 6: Clean the outcome column
df["y"] = df["y"].str.lower()

rows_before = len(df)
df = df[df["y"].isin(["yes", "no"])].copy()

print("\nRecords removed due to invalid outcome:",
      rows_before - len(df))

# We are NOT automatically deleting exact duplicates.
# This dataset has no unique customer ID to verify them.
# We are also keeping 'unknown' as a valid category.

# STEP 7: Create the conversion indicator
df["converted"] = (df["y"] == "yes").astype(int)

# STEP 8: Create contact-frequency groups
df["contact_frequency"] = pd.cut(
    df["campaign"],
    bins=[0, 1, 3, 5, float("inf")],
    labels=[
        "1 contact",
        "2-3 contacts",
        "4-5 contacts",
        "6+ contacts"
    ]
)

# STEP 9: Create age groups for comparison
df["age_group"] = pd.cut(
    df["age"],
    bins=[0, 25, 35, 45, 55, 65, 120],
    labels=[
        "25 or younger",
        "26-35",
        "36-45",
        "46-55",
        "56-65",
        "Over 65"
    ]
)

# STEP 10: Calculate overall conversion metrics
total_records = len(df)
subscribed = int(df["converted"].sum())
not_subscribed = total_records - subscribed

conversion_rate = (
    subscribed / total_records * 100
    if total_records else 0
)

print("\n========== OVERALL RESULTS ==========")
print("Records analyzed:", total_records)
print("Subscribed:", subscribed)
print("Did not subscribe:", not_subscribed)
print(f"Subscription conversion rate: {conversion_rate:.2f}%")

print("\nMissing values after cleaning:")
print(df.isnull().sum())

# STEP 11: Create grouped performance summaries
def make_summary(data, group_column, output_name):
    summary = data.groupby(
        group_column, dropna=False, observed=True
    ).agg(
        Records=("converted", "size"),
        Subscribed=("converted", "sum"),
        Conversion_Rate=("converted", "mean")
    ).reset_index()

    summary["Not_Subscribed"] = (
        summary["Records"] - summary["Subscribed"]
    )
    summary["Conversion_Rate"] *= 100

    summary.to_csv(output_folder / output_name, index=False)
    return summary

# Contact method: cellular vs telephone
contact_summary = make_summary(
    df, "contact", "contact_method_summary.csv"
)

# Month-by-month performance in calendar order
month_order = [
    "jan", "feb", "mar", "apr", "may", "jun",
    "jul", "aug", "sep", "oct", "nov", "dec"
]

df["month"] = pd.Categorical(
    df["month"],
    categories=month_order,
    ordered=True
)

monthly_summary = make_summary(
    df, "month", "monthly_summary.csv"
)

monthly_summary = monthly_summary.sort_values("month")
monthly_summary.to_csv(
    output_folder / "monthly_summary.csv", index=False
)

# Compare job categories
job_summary = make_summary(
    df, "job", "job_summary.csv"
).sort_values("Conversion_Rate", ascending=False)

job_summary.to_csv(
    output_folder / "job_summary.csv", index=False
)

# Compare number of campaign contacts
frequency_summary = make_summary(
    df, "contact_frequency", "contact_frequency_summary.csv"
)

# Compare age groups
age_summary = make_summary(
    df, "age_group", "age_group_summary.csv"
)

# STEP 12: Export the cleaned dataset for Power BI
df.to_csv(
    output_folder / "cleaned_bank_marketing.csv",
    index=False
)

print("\n========== CONTACT METHOD PERFORMANCE ==========")
print(contact_summary.round(2).to_string(index=False))

print("\n========== MONTHLY PERFORMANCE ==========")
print(monthly_summary.round(2).to_string(index=False))

print("\n========== JOB PERFORMANCE ==========")
print(job_summary.round(2).to_string(index=False))

print("\n========== CONTACT FREQUENCY ==========")
print(frequency_summary.round(2).to_string(index=False))

print("\n========== AGE GROUP PERFORMANCE ==========")
print(age_summary.round(2).to_string(index=False))

print("\nSUCCESS! All output files are saved in:")
print(output_folder)
