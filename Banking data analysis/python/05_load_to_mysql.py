import pandas as pd
import mysql.connector
from getpass import getpass

# 1. Load cleaned CSV
csv_path = "/Users/aakasha/Documents/New project/Banking data analysis/Data/cleaned_data/bank_data_cleaned.csv"

df = pd.read_csv(csv_path)

print("CSV loaded successfully")
print("Rows:", len(df))
print("Columns:", df.columns.tolist())

# 2. Convert date
df["transaction_date"] = pd.to_datetime(
    df["transaction_date"],
    errors="coerce"
)

# 3. Replace NaN with None for MySQL
df = df.where(pd.notna(df), None)

# 4. Ask for MySQL password
password = getpass("Enter MySQL banking_user password: ")

# 5. Connect to MySQL
conn = mysql.connector.connect(
    host="127.0.0.1",
    user="banking_user",
    password=password,
    database="banking_finance"
)

cursor = conn.cursor()

# 6. Insert data
sql = """
INSERT INTO banking_transactions (
    transaction_id,
    customer_id,
    account_id,
    transaction_date,
    bank_name,
    city,
    transaction_type,
    amount_inr,
    channel,
    category,
    status,
    description,
    balance_after_txn
)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

columns = [
    "transaction_id",
    "customer_id",
    "account_id",
    "transaction_date",
    "bank_name",
    "city",
    "transaction_type",
    "amount_inr",
    "channel",
    "category",
    "status",
    "description",
    "balance_after_txn"
]

rows = list(
    df[columns].itertuples(index=False, name=None)
)

cursor.executemany(sql, rows)
conn.commit()

print("Data imported successfully!")
print("Rows inserted:", cursor.rowcount)

query = "SELECT * FROM banking_transactions"

df = pd.read_sql(query, conn)

df.to_csv("/Users/aakasha/Documents/New project/Banking data analysis/Data/cleaned_data/bank_data_cleaned_tableau.csv", index=False)



cursor.close()
conn.close()
