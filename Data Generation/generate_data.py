import pandas as pd
import numpy as np

np.random.seed(42)

# -----------------------------
# CONFIG
# -----------------------------
N = 6000  # number of customers

# -----------------------------
# CUSTOMER TABLE
# -----------------------------
customer_id = [f"C{str(i).zfill(6)}" for i in range(1, N + 1)]

gender = np.random.choice(["Male", "Female"], N)
age = np.random.randint(18, 65, N)

contract_type = np.random.choice(
    ["Month-to-Month", "One Year", "Two Year"],
    size=N,
    p=[0.5, 0.3, 0.2]
)

tenure_months = []
for c in contract_type:
    if c == "Month-to-Month":
        tenure_months.append(np.random.randint(1, 18))
    elif c == "One Year":
        tenure_months.append(np.random.randint(6, 36))
    else:
        tenure_months.append(np.random.randint(12, 72))

tenure_months = np.array(tenure_months)

# churn probability logic
churn_prob = (
    (tenure_months < 6) * 0.35 +
    (contract_type == "Month-to-Month") * 0.25 +
    (contract_type == "One Year") * 0.10
)

churn = np.where(np.random.rand(N) < churn_prob, "Yes", "No")

customers = pd.DataFrame({
    "customer_id": customer_id,
    "gender": gender,
    "age": age,
    "tenure_months": tenure_months,
    "contract_type": contract_type,
    "churn": churn
})

# -----------------------------
# BILLING TABLE
# -----------------------------
monthly_charges = np.round(
    np.random.normal(70, 20, N).clip(30, 150), 2
)

total_charges = np.round(monthly_charges * tenure_months, 2)

payment_method = np.random.choice(
    ["Credit Card", "Debit Card", "UPI", "Bank Transfer"],
    size=N
)

billing = pd.DataFrame({
    "customer_id": customer_id,
    "monthly_charges": monthly_charges,
    "total_charges": total_charges,
    "payment_method": payment_method
})

# -----------------------------
# USAGE TABLE
# -----------------------------
avg_monthly_usage = np.round(
    np.random.normal(250, 80, N).clip(50, 500), 1
)

support_tickets = np.random.poisson(
    lam=(customers["churn"] == "Yes") * 3 + 1
)

usage = pd.DataFrame({
    "customer_id": customer_id,
    "avg_monthly_usage": avg_monthly_usage,
    "support_tickets": support_tickets
})

# -----------------------------
# SAVE FILES
# -----------------------------
customers.to_csv("customers.csv", index=False)
billing.to_csv("billing.csv", index=False)
usage.to_csv("usage.csv", index=False)

print("✅ Generated:")
print(" - customers.csv")
print(" - billing.csv")
print(" - usage.csv")
