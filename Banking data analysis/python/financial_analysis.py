import pandas as pd

# Load cleaned data
df = pd.read_csv("/Users/aakasha/Documents/New project/Banking data analysis/Data/cleaned_data/bank_data_cleaned.csv")

# Convert date
df["transaction_date"] = pd.to_datetime(
    df["transaction_date"],
    errors="coerce"
)


# =========================================================
# 1. CREDIT VS DEBIT ANALYSIS
# =========================================================

credit = df[df["transaction_type"] == "Credit"]

debit = df[df["transaction_type"] == "Debit"]

total_credit = credit["amount_inr"].sum()
total_debit = debit["amount_inr"].sum()

net_cash_flow = total_credit - total_debit

print("\n===== CASH FLOW ANALYSIS =====")

print("Total Credit: ₹{:,.2f}".format(total_credit))

print("Total Debit: ₹{:,.2f}".format(total_debit))

print("Net Cash Flow: ₹{:,.2f}".format(net_cash_flow))


# =========================================================
# 2. BANK PERFORMANCE
# =========================================================

bank_performance = (
    df.groupby("bank_name")
    .agg(
        transactions=("transaction_id", "count"),
        transaction_value=("amount_inr", "sum"),
        average_transaction=("amount_inr", "mean")
    )
    .sort_values(
        "transaction_value",
        ascending=False
    )
)

print("\n===== BANK PERFORMANCE =====")
print(bank_performance)


# Highest transaction-value bank
top_bank = bank_performance.index[0]

print(
    "\nHighest transaction-value bank:",
    top_bank
)


# =========================================================
# 3. CHANNEL FAILURE ANALYSIS
# =========================================================

channel_performance = (
    df.groupby("channel")
    .agg(
        total_transactions=("transaction_id", "count"),
        failed_transactions=(
            "status",
            lambda x: (x == "FAILED").sum()
        ),
        successful_transactions=(
            "status",
            lambda x: (x == "SUCCESS").sum()
        )
    )
)

channel_performance["failure_rate_%"] = (
    channel_performance["failed_transactions"]
    / channel_performance["total_transactions"]
    * 100
)

channel_performance["success_rate_%"] = (
    channel_performance["successful_transactions"]
    / channel_performance["total_transactions"]
    * 100
)

channel_performance = channel_performance.sort_values(
    "failure_rate_%",
    ascending=False
)

print("\n===== CHANNEL FAILURE ANALYSIS =====")
print(channel_performance)


# =========================================================
# 4. CATEGORY ANALYSIS
# =========================================================

category_performance = (
    df.groupby("category")
    .agg(
        transactions=("transaction_id", "count"),
        total_value=("amount_inr", "sum"),
        average_value=("amount_inr", "mean")
    )
    .sort_values(
        "total_value",
        ascending=False
    )
)

print("\n===== CATEGORY ANALYSIS =====")
print(category_performance)


# =========================================================
# 5. CITY ANALYSIS
# =========================================================

city_performance = (
    df.groupby("city")
    .agg(
        transactions=("transaction_id", "count"),
        total_value=("amount_inr", "sum"),
        average_value=("amount_inr", "mean")
    )
    .sort_values(
        "total_value",
        ascending=False
    )
)

print("\n===== CITY ANALYSIS =====")
print(city_performance)


# =========================================================
# 6. MONTHLY TREND
# =========================================================

df["month"] = df["transaction_date"].dt.to_period("M")

monthly = (
    df.groupby("month")
    .agg(
        transactions=("transaction_id", "count"),
        total_value=("amount_inr", "sum")
    )
    .reset_index()
)

monthly["mom_growth_%"] = (
    monthly["total_value"]
    .pct_change()
    * 100
)

print("\n===== MONTHLY TREND =====")
print(monthly)


# =========================================================
# 7. TOP 10 TRANSACTIONS
# =========================================================

top_transactions = (
    df.sort_values(
        "amount_inr",
        ascending=False
    )
    [
        [
            "transaction_id",
            "customer_id",
            "bank_name",
            "transaction_type",
            "amount_inr",
            "channel",
            "category",
            "status"
        ]
    ]
    .head(10)
)

print("\n===== TOP 10 TRANSACTIONS =====")
print(top_transactions)


# =========================================================
# 8. FAILED TRANSACTION ANALYSIS
# =========================================================

failed = df[df["status"] == "FAILED"]

failed_by_bank = (
    failed.groupby("bank_name")
    .size()
    .sort_values(ascending=False)
)

print("\n===== FAILED TRANSACTIONS BY BANK =====")
print(failed_by_bank)


# =========================================================
# 9. REVERSED TRANSACTION ANALYSIS
# =========================================================

reversed_txns = df[
    df["status"] == "REVERSED"
]

reversed_value = reversed_txns[
    "amount_inr"
].sum()

print("\n===== REVERSAL ANALYSIS =====")

print(
    "Reversed Transactions:",
    len(reversed_txns)
)

print(
    "Reversed Transaction Value: ₹{:,.2f}".format(
        reversed_value
    )
)


# =========================================================
# 10. HIGH VALUE TRANSACTION ANALYSIS
# =========================================================

high_value_threshold = 100000

high_value = df[
    df["amount_inr"] >= high_value_threshold
]

print("\n===== HIGH VALUE TRANSACTIONS =====")

print(
    "Transactions >= ₹1,00,000:",
    len(high_value)
)

print(
    "High-value transaction amount: ₹{:,.2f}".format(
        high_value["amount_inr"].sum()
    )
)