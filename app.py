import pandas as pd
import numpy as np

from src.data_loader import load_data
from src.anomaly_detector import detect_anomalies
from src.ai_explainer import generate_ai_explanation
from src.email_alert import send_email_alert
from src.business_summary import (
    generate_summary,
    explain_anomaly,
    detect_incidents,
    get_alert_priority
)


# ==========================================
# 1. CREATE SAMPLE BUSINESS DATA
# ==========================================

np.random.seed(42)

dates = pd.date_range(start="2026-06-18", periods=60)

traffic = np.random.randint(9000, 12000, 60)
conversion_rate = np.random.uniform(3.8, 4.8, 60)

orders = (traffic * conversion_rate / 100).astype(int)

revenue = orders * np.random.randint(250, 350, 60)

cost = revenue * np.random.uniform(0.30, 0.40, 60)

refunds = np.random.randint(800, 1500, 60)


# Intentional anomalies

traffic[45] = 18000
conversion_rate[45] = 2.1

orders[45] = int(
    traffic[45] * conversion_rate[45] / 100
)

revenue[45] = orders[45] * 280

cost[50] = revenue[50] * 0.75

refunds[55] = 5000


data = pd.DataFrame({
    "Date": dates,
    "Revenue": revenue,
    "Orders": orders,
    "Conversion_Rate": conversion_rate,
    "Traffic": traffic,
    "Cost": cost,
    "Refunds": refunds
})


file_path = "data/business_data.xlsx"

data.to_excel(
    file_path,
    index=False
)

print("Dataset created successfully!")

print(data.head())


# ==========================================
# 2. LOAD DATA
# ==========================================

df = load_data(file_path)

print("\nData loaded successfully!")

print(df.head())

print("\nShape:", df.shape)


# ==========================================
# 3. DETECT ANOMALIES
# ==========================================

anomalies = detect_anomalies(df)

print("\nAnomalies Detected:")

print(anomalies)


# ==========================================
# 4. BUSINESS SUMMARY
# ==========================================

summary = generate_summary(anomalies)

print("\nBusiness Summary:")

print(summary)


# ==========================================
# 5. DETAILED EXPLANATIONS
# ==========================================

print("\nDetailed Business Explanations:")

for _, row in anomalies.iterrows():

    explanation = explain_anomaly(row)

    print(
        f"\n[{row['Severity']}] "
        f"{row['Date'].date()} - "
        f"{row['Metric']}"
    )

    print(explanation)


# ==========================================
# 6. DETECT BUSINESS INCIDENTS
# ==========================================

incidents = detect_incidents(anomalies)

print("\nBusiness Incidents:")


for incident in incidents:

    print(
        f"\nDate: "
        f"{incident['Date'].date()}"
    )

    priority = get_alert_priority(
        incident["Anomalies"]
    )

    print(
        f"Alert Priority: {priority}"
    )

    print(
        f"Description: "
        f"{incident['Description']}"
    )

    for _, row in incident["Anomalies"].iterrows():

        print(
            f"- {row['Metric']}: "
            f"{row['Change_Percentage']:.1f}% "
            f"{row['Direction']} "
            f"({row['Severity']})"
        )

    # AI analysis only for important incidents
    if priority != "NO EMAIL":

        ai_explanation = generate_ai_explanation(incident)

print("\n🤖 AI Business Analysis:")

print(
    "What happened:",
    ai_explanation["what_happened"]
)

print(
    "Possible cause:",
    ai_explanation["possible_cause"]
)

print(
    "Business impact:",
    ai_explanation["business_impact"]
)

print(
    "Recommended action:",
    ai_explanation["recommended_action"]
)
if priority != "NO EMAIL":

    ai_explanation = generate_ai_explanation(
        incident
    )

    print("\n🤖 AI Business Analysis:")

    print(
        "What happened:",
        ai_explanation["what_happened"]
    )

    print(
        "Possible cause:",
        ai_explanation["possible_cause"]
    )

    print(
        "Business impact:",
        ai_explanation["business_impact"]
    )

    print(
        "Recommended action:",
        ai_explanation["recommended_action"]
    )

    send_email_alert(
        incident,
        ai_explanation,
        priority
    )