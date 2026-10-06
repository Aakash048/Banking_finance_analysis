import pandas as pd

# Load cleaned data
df = pd.read_csv("/Users/aakasha/Documents/New project/Banking data analysis/Data/cleaned_data/bank_data_cleaned.csv")

# Convert date
df["transaction_date"] = pd.to_datetime(
    df["transaction_date"],
    errors="coerce"
)

print("Dataset shape:", df.shape)


# =========================================================
# 1. BASIC FINANCIAL KPIs
# =========================================================

total_transactions = len(df)

total_transaction_value = df["amount_inr"].sum()

average_transaction_value = df["amount_inr"].mean()

median_transaction_value = df["amount_inr"].median()

print("\n===== BASIC KPIs =====")

print("Total Transactions:", total_transactions)

print("Total Transaction Value: ₹{:,.2f}".format(
    total_transaction_value
))

print("Average Transaction Value: ₹{:,.2f}".format(
    average_transaction_value
))

print("Median Transaction Value: ₹{:,.2f}".format(
    median_transaction_value
))


# =========================================================
# 2. TRANSACTION STATUS
# =========================================================

status_counts = df["status"].value_counts()

print("\n===== TRANSACTION STATUS =====")
print(status_counts)


# Calculate percentages
status_percentage = (
    df["status"]
    .value_counts(normalize=True)
    .mul(100)
    .round(2)
)

print("\nStatus Percentage:")
print(status_percentage)


# =========================================================
# 3. SUCCESS RATE
# =========================================================

success_rate = (
    (df["status"] == "SUCCESS").mean() * 100
)

failure_rate = (
    (df["status"] == "FAILED").mean() * 100
)

reversal_rate = (
    (df["status"] == "REVERSED").mean() * 100
)

print("\n===== PERFORMANCE KPIs =====")

print("Success Rate: {:.2f}%".format(success_rate))

print("Failure Rate: {:.2f}%".format(failure_rate))

print("Reversal Rate: {:.2f}%".format(reversal_rate))


# =========================================================
# 4. CREDIT VS DEBIT
# =========================================================

transaction_type = (
    df.groupby("transaction_type")
    .agg(
        transaction_count=("transaction_id", "count"),
        total_value=("amount_inr", "sum"),
        average_value=("amount_inr", "mean")
    )
    .sort_values("total_value", ascending=False)
)

print("\n===== CREDIT VS DEBIT =====")
print(transaction_type)


# =========================================================
# 5. ANALYSIS BY BANK
# =========================================================

bank_analysis = (
    df.groupby("bank_name")
    .agg(
        transaction_count=("transaction_id", "count"),
        total_value=("amount_inr", "sum"),
        average_transaction=("amount_inr", "mean")
    )
    .sort_values("total_value", ascending=False)
)

print("\n===== BANK ANALYSIS =====")
print(bank_analysis)


# =========================================================
# 6. ANALYSIS BY CHANNEL
# =========================================================

channel_analysis = (
    df.groupby("channel")
    .agg(
        transaction_count=("transaction_id", "count"),
        total_value=("amount_inr", "sum"),
        average_transaction=("amount_inr", "mean")
    )
    .sort_values("transaction_count", ascending=False)
)

print("\n===== CHANNEL ANALYSIS =====")
print(channel_analysis)


# =========================================================
# 7. ANALYSIS BY CATEGORY
# =========================================================

category_analysis = (
    df.groupby("category")
    .agg(
        transaction_count=("transaction_id", "count"),
        total_value=("amount_inr", "sum"),
        average_transaction=("amount_inr", "mean")
    )
    .sort_values("total_value", ascending=False)
)

print("\n===== CATEGORY ANALYSIS =====")
print(category_analysis)


# =========================================================
# 8. MONTHLY ANALYSIS
# =========================================================

df["month"] = df["transaction_date"].dt.to_period("M")

monthly_analysis = (
    df.groupby("month")
    .agg(
        transaction_count=("transaction_id", "count"),
        total_value=("amount_inr", "sum"),
        average_transaction=("amount_inr", "mean")
    )
    .reset_index()
)

print("\n===== MONTHLY ANALYSIS =====")
print(monthly_analysis)


# =========================================================
# 9. MONTH-OVER-MONTH GROWTH
# =========================================================

monthly_analysis["mom_growth_%"] = (
    monthly_analysis["total_value"]
    .pct_change() * 100
)

print("\n===== MONTHLY GROWTH =====")
print(monthly_analysis)


# =========================================================
# 10. DIGITAL TRANSACTION SHARE
# =========================================================

digital_channels = [
    "UPI",
    "IMPS",
    "NEFT",
    "RTGS",
    "NETBANKING"
]

digital_transactions = df[
    df["channel"].isin(digital_channels)
]

digital_share = (
    len(digital_transactions) / len(df) * 100
)

print("\n===== DIGITAL BANKING =====")

print(
    "Digital Transaction Share: {:.2f}%".format(
        digital_share
    )
)