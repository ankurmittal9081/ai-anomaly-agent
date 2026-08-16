import os
import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from dotenv import load_dotenv


load_dotenv()


def send_email_alert(incident, ai_explanation, priority):

    sender = os.getenv("EMAIL_SENDER")
    password = os.getenv("EMAIL_PASSWORD")
    receiver = os.getenv("EMAIL_RECEIVER")

    if not sender or not password or not receiver:
        raise ValueError(
            "Email credentials are missing from .env"
        )

    date = incident["Date"].date()

    subject = f"🚨 AI Anomaly Alert - {priority} - {date}"

    body = f"""
AI ANOMALY ALERT

Date:
{date}

Priority:
{priority}

Business Incident:
{incident["Description"]}

Detected Metrics:
"""

    for _, row in incident["Anomalies"].iterrows():

        body += (
            f"\n- {row['Metric']}: "
            f"{row['Change_Percentage']:.1f}% "
            f"{row['Direction']} "
            f"({row['Severity']})"
        )

    body += f"""

AI BUSINESS ANALYSIS

What happened:
{ai_explanation["what_happened"]}

Possible cause:
{ai_explanation["possible_cause"]}

Business impact:
{ai_explanation["business_impact"]}

Recommended action:
{ai_explanation["recommended_action"]}
"""

    message = MIMEMultipart()

    message["From"] = sender
    message["To"] = receiver
    message["Subject"] = subject

    message.attach(
        MIMEText(body, "plain")
    )

    with smtplib.SMTP(
        "smtp.gmail.com",
        587
    ) as server:

        server.starttls()

        server.login(
            sender,
            password
        )

        server.sendmail(
            sender,
            receiver,
            message.as_string()
        )

    print(
        f"\n📧 Email alert sent to {receiver}"
    )