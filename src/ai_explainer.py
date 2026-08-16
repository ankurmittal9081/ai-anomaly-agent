import os
import json
import time

import streamlit as st
from dotenv import load_dotenv
from google import genai


# =========================================================
# LOAD ENVIRONMENT
# =========================================================

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "GEMINI_API_KEY is missing from .env file"
    )


# =========================================================
# GEMINI CLIENT
# =========================================================

client = genai.Client(
    api_key=api_key
)


# =========================================================
# AI EXPLANATION
# =========================================================

@st.cache_data(
    ttl=3600,
    show_spinner=False
)
def generate_ai_explanation(
    incident_date,
    description,
    anomaly_data
):

    # -----------------------------------------------------
    # BUILD ANOMALY TEXT
    # -----------------------------------------------------

    anomaly_lines = []

    for row in anomaly_data:

        anomaly_lines.append(
            f"""
Metric: {row['Metric']}
Actual Value: {row['Actual_Value']:.2f}
Baseline: {row['Baseline']:.2f}
Change: {row['Change_Percentage']:.2f}%
Direction: {row['Direction']}
Severity: {row['Severity']}
"""
        )

    anomaly_text = "\n".join(
        anomaly_lines
    )


    # -----------------------------------------------------
    # PROMPT
    # -----------------------------------------------------

    prompt = f"""
You are a senior business data analyst.

Analyze the following business anomaly incident.

Date:
{incident_date}

Detected Business Pattern:
{description}

Detected Metrics:
{anomaly_text}

Return ONLY valid JSON.

Use exactly this structure:

{{
  "what_happened": "...",
  "possible_cause": "...",
  "business_impact": "...",
  "recommended_action": "..."
}}

Rules:

- Do not use Markdown.
- Do not use code fences.
- Do not add text before or after the JSON.
- Use simple business English.
- Never assume a currency.
- Never invent facts.
- Never present a possible cause as a confirmed fact.
- Do not claim ROI, profit, loss, or monetary impact unless the provided data supports it.
- Base conclusions only on the provided metrics.
- Possible causes must use words such as "may", "could", or "possible".
- Keep each field concise.
"""


    # -----------------------------------------------------
    # GEMINI REQUEST
    # -----------------------------------------------------

    try:

        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt
        )


        # -------------------------------------------------
        # PARSE JSON
        # -------------------------------------------------

        result = json.loads(
            response.text
        )

        return result


    # -----------------------------------------------------
    # QUOTA ERROR
    # -----------------------------------------------------

    except Exception as e:

        error_text = str(e)

        if (
            "429" in error_text
            or "RESOURCE_EXHAUSTED" in error_text
            or "quota" in error_text.lower()
        ):

            return {
                "what_happened":
                    "AI analysis is temporarily unavailable because the Gemini API quota has been reached.",

                "possible_cause":
                    "The API request limit was exceeded. The business anomaly itself was detected successfully by the monitoring system.",

                "business_impact":
                    "Anomaly detection continues to work, but AI-generated explanations are temporarily unavailable.",

                "recommended_action":
                    "Wait for the API quota to reset or use a project with available Gemini API capacity."
            }


        # -------------------------------------------------
        # JSON ERROR
        # -------------------------------------------------

        if isinstance(
            e,
            json.JSONDecodeError
        ):

            return {
                "what_happened":
                    "The business anomaly was detected successfully, but the AI response could not be parsed.",

                "possible_cause":
                    "The AI response was not returned in the expected JSON format.",

                "business_impact":
                    "AI explanation is temporarily unavailable.",

                "recommended_action":
                    "Retry the AI analysis."
            }


        # -------------------------------------------------
        # OTHER ERROR
        # -------------------------------------------------

        return {
            "what_happened":
                "The anomaly was detected, but AI analysis could not be generated.",

            "possible_cause":
                "A temporary AI service or configuration issue may have occurred.",

            "business_impact":
                "The monitoring system continues to detect anomalies without the AI explanation.",

            "recommended_action":
                "Check the application logs and retry the analysis."
        }