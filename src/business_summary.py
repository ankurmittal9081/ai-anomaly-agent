def explain_anomaly(row):

    metric = row["Metric"]
    change = row["Change_Percentage"]
    direction = row["Direction"]
    severity = row["Severity"]

    if metric == "Traffic" and direction == "UP":
        return (
            f"Traffic increased by {change:.1f}% compared with the recent baseline. "
            "This may indicate a campaign change or a sudden increase in visitors."
        )

    elif metric == "Conversion_Rate" and direction == "DOWN":
        return (
            f"Conversion rate decreased by {abs(change):.1f}% compared with the recent baseline. "
            "This may indicate lower-quality traffic or a problem in the customer conversion process."
        )

    elif metric == "Refunds" and direction == "UP":
        return (
            f"Refunds increased by {change:.1f}% compared with the recent baseline. "
            "This may indicate a product, payment, or customer-experience issue."
        )

    elif metric == "Cost" and direction == "UP":
        return (
            f"Cost increased by {change:.1f}% compared with the recent baseline. "
            "This may indicate increased operational or marketing expenses."
        )

    elif metric == "Revenue" and direction == "DOWN":
        return (
            f"Revenue decreased by {abs(change):.1f}% compared with the recent baseline. "
            "This may indicate weaker sales performance."
        )

    elif metric == "Orders" and direction == "DOWN":
        return (
            f"Orders decreased by {abs(change):.1f}% compared with the recent baseline. "
            "This may indicate reduced customer demand."
        )

    return (
        f"{metric} changed {abs(change):.1f}% {direction.lower()} "
        f"compared with the recent baseline."
    )


def generate_summary(anomalies):

    if anomalies.empty:
        return "No significant anomalies were detected."

    critical = anomalies[anomalies["Severity"] == "Critical"]
    high = anomalies[anomalies["Severity"] == "High"]

    summary = []

    summary.append(
        f"{len(critical)} critical anomalies were detected."
    )

    summary.append(
        f"{len(high)} high-severity anomalies were detected."
    )

    return " ".join(summary)

def detect_incidents(anomalies):

    incidents = []

    dates = anomalies["Date"].unique()

    for date in dates:

        daily = anomalies[anomalies["Date"] == date]

        metrics = set(daily["Metric"])

        incident = None

        # Rule 1: Traffic UP + Conversion Rate DOWN
        if "Traffic" in metrics and "Conversion_Rate" in metrics:

            traffic = daily[daily["Metric"] == "Traffic"].iloc[0]
            conversion = daily[daily["Metric"] == "Conversion_Rate"].iloc[0]

            if (
                traffic["Direction"] == "UP"
                and conversion["Direction"] == "DOWN"
            ):
                incident = (
                    "Traffic increased while conversion rate decreased. "
                    "Possible traffic-quality or campaign-targeting issue."
                )

        # Rule 2: Revenue DOWN + Orders DOWN
        if "Revenue" in metrics and "Orders" in metrics:

            revenue = daily[daily["Metric"] == "Revenue"].iloc[0]
            orders = daily[daily["Metric"] == "Orders"].iloc[0]

            if (
                revenue["Direction"] == "DOWN"
                and orders["Direction"] == "DOWN"
            ):
                incident = (
                    "Revenue and orders both decreased. "
                    "Possible demand or sales-performance issue."
                )

        # Rule 3: Cost UP + Revenue DOWN
        if "Cost" in metrics and "Revenue" in metrics:

            cost = daily[daily["Metric"] == "Cost"].iloc[0]
            revenue = daily[daily["Metric"] == "Revenue"].iloc[0]

            if (
                cost["Direction"] == "UP"
                and revenue["Direction"] == "DOWN"
            ):
                incident = (
                    "Costs increased while revenue decreased. "
                    "This may indicate a profitability risk."
                )

        # Rule 4: Refunds UP
        if "Refunds" in metrics:

            refunds = daily[daily["Metric"] == "Refunds"].iloc[0]

            if refunds["Direction"] == "UP":
                incident = (
                    "Refunds increased significantly. "
                    "Possible product, payment, or customer-experience issue."
                )

        # Add incident only when a meaningful rule matched
        if incident:

            incidents.append({
                "Date": date,
                "Description": incident,
                "Anomalies": daily
            })

    return incidents

def get_alert_priority(anomalies):

    if anomalies.empty:
        return "No Alert"

    max_severity = anomalies["Severity"].map({
        "Critical": 3,
        "High": 2,
        "Moderate": 1
    }).max()

    if max_severity == 3:
        return "CRITICAL ALERT"

    elif max_severity == 2:
        return "HIGH ALERT"

    else:
        return "NO EMAIL"