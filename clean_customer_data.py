import pandas as pd
import numpy as np
import re

# Load the raw data
df = pd.read_csv("customer_survey_raw_data.csv")

# ---------------------------
# 1. Remove duplicate rows
# ---------------------------
df = df.drop_duplicates()

# ---------------------------
# 2. Standardise Full Name formatting
# ---------------------------
def clean_name(name):
    if pd.isna(name):
        return np.nan
    name = name.strip()                    # remove leading/trailing spaces
    name = " ".join(name.split())          # remove double/multiple spaces
    return name.title()                    # convert to Title Case

df["Full Name"] = df["Full Name"].apply(clean_name)

# ---------------------------
# 3. Split First and Last Name
# ---------------------------
df["First Name"] = df["Full Name"].apply(lambda x: x.split()[0] if isinstance(x, str) else np.nan)
df["Last Name"]  = df["Full Name"].apply(lambda x: x.split()[-1] if isinstance(x, str) and len(x.split()) > 1 else np.nan)

# ---------------------------
# 4. Clean email formatting
# ---------------------------
def clean_email(email):
    if pd.isna(email):
        return np.nan
    email = email.strip().lower()
    if "@" not in email or "." not in email.split("@")[-1]:
        return email + " (INVALID)"
    return email

df["Email"] = df["Email"].apply(clean_email)

# ---------------------------
# 5. Convert Age to integer (smart extraction)
# ---------------------------
def clean_age(age):
    if pd.isna(age):
        return np.nan
    age_str = str(age)
    match = re.search(r"\d+", age_str)  # find digits anywhere in the string
    if match:
        return int(match.group())       # convert extracted digits to int
    return np.nan

df["Age"] = df["Age"].astype("Int64")

# ---------------------------
# 6. Clean and format Join Date
# ---------------------------
def clean_date(date):
    if pd.isna(date) or str(date).strip() == "":
        return np.nan
    try:
        parsed = pd.to_datetime(date, errors="coerce")
        return parsed.strftime("%Y-%m-%d")
    except:
        return np.nan

df["Join Date"] = df["Join Date"].apply(clean_date)

# ---------------------------
# 7. Replace messy 'N/A' text values with NaN
# ---------------------------
df = df.replace(["N/A", "n/a", "None", "none", ""], np.nan)

# ---------------------------
# 8. Sort by Join Date (newest first)
# ---------------------------
df = df.sort_values(by="Join Date", ascending=False)

# ---------------------------
# 9. Save cleaned file
# ---------------------------
df.to_csv("customer_cleaned_output.csv", index=False)

print("Cleaning complete! Saved as customer_cleaned_output.csv")
