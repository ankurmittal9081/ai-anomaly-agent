import pandas as pd


def get_severity(change):

    change = abs(change)

    if change >= 50:
        return "Critical"

    elif change >= 30:
        return "High"

    else:
        return "Moderate"


def detect_anomalies(data, window=7, threshold=0.20):

    metrics = [
        "Revenue",
        "Orders",
        "Conversion_Rate",
        "Traffic",
        "Cost",
        "Refunds"
    ]

    results = []

    for metric in metrics:

        rolling_average = data[metric].rolling(window).mean()

        percentage_change = (
            (data[metric] - rolling_average)
            / rolling_average
        )

        anomalies = percentage_change.abs() > threshold

        for i in range(len(data)):

            if anomalies.iloc[i]:

                change = percentage_change.iloc[i] * 100

                if change > 0:
                    direction = "UP"
                else:
                    direction = "DOWN"

                severity = get_severity(change)

                results.append({
                    "Date": data["Date"].iloc[i],
                    "Metric": metric,
                    "Actual_Value": data[metric].iloc[i],
                    "Baseline": rolling_average.iloc[i],
                    "Change_Percentage": round(change, 2),
                    "Direction": direction,
                    "Severity": severity
                })

    return pd.DataFrame(results)