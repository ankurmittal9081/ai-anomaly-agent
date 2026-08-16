import streamlit as st

from src.data_loader import load_data
from src.anomaly_detector import detect_anomalies
from src.business_summary import (
    detect_incidents,
    get_alert_priority
)
from src.ai_explainer import generate_ai_explanation


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="AI Anomaly Monitoring Agent",
    page_icon="🚨",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* Main page */

    .main {
        padding-top: 1rem;
    }


    /* Main title */

    .hero-title {
        font-size: 42px;
        font-weight: 800;
        margin-bottom: 4px;
    }


    .hero-subtitle {
        font-size: 17px;
        color: #9ca3af;
        margin-bottom: 25px;
    }


    /* KPI cards */

    .kpi-card {
        padding: 20px;
        border-radius: 14px;
        background: linear-gradient(
            135deg,
            rgba(30, 41, 59, 0.95),
            rgba(15, 23, 42, 0.95)
        );
        border: 1px solid rgba(148, 163, 184, 0.15);
        min-height: 125px;
    }


    .kpi-title {
        font-size: 14px;
        color: #94a3b8;
        margin-bottom: 8px;
    }


    .kpi-value {
        font-size: 34px;
        font-weight: 700;
    }


    .section-title {
        font-size: 26px;
        font-weight: 700;
        margin-top: 15px;
        margin-bottom: 15px;
    }


    /* Status */

    .status-online {
        color: #22c55e;
        font-weight: 700;
    }


    /* Footer */

    .footer {
        text-align: center;
        color: #64748b;
        padding: 30px 0;
        font-size: 13px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        "## 🚨 AI Anomaly Agent"
    )

    st.markdown("---")

    st.markdown(
        "### 📡 Monitoring Status"
    )

    st.markdown(
        '<p class="status-online">🟢 System Online</p>',
        unsafe_allow_html=True
    )

    st.markdown("---")

    st.markdown(
        "### 📁 Dataset"
    )

    st.write(
        "Business Performance Data"
    )

    st.write(
        "📅 60 Days"
    )

    st.write(
        "📊 7 Metrics"
    )

    st.markdown("---")

    st.markdown(
        "### 🤖 AI Engine"
    )

    st.write(
        "Google Gemini"
    )

    st.markdown("---")

    st.markdown(
        "### 🔧 Pipeline"
    )

    st.write(
        "Data → Detection → Incidents → AI Analysis"
    )

    st.markdown("---")

    st.caption(
        "AI Anomaly Monitoring Agent"
    )


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="hero-title">🚨 AI Anomaly Monitoring Agent</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="hero-subtitle">'
    'Automated business monitoring, anomaly detection '
    'and AI-powered incident analysis.'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# LOAD DATA
# ============================================================

df = load_data(
    "data/business_data.xlsx"
)

anomalies = detect_anomalies(
    df
)

incidents = detect_incidents(
    anomalies
)


# ============================================================
# KPI CALCULATIONS
# ============================================================

critical_anomalies = len(
    anomalies[
        anomalies["Severity"] == "Critical"
    ]
)

high_anomalies = len(
    anomalies[
        anomalies["Severity"] == "High"
    ]
)

moderate_anomalies = len(
    anomalies[
        anomalies["Severity"] == "Moderate"
    ]
)

total_anomalies = len(
    anomalies
)


critical_incident_count = sum(
    1
    for incident in incidents
    if get_alert_priority(
        incident["Anomalies"]
    ) == "CRITICAL ALERT"
)


alerts_generated = sum(
    1
    for incident in incidents
    if get_alert_priority(
        incident["Anomalies"]
    ) != "NO EMAIL"
)


# ============================================================
# KPI SECTION
# ============================================================

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">
                🚨 Critical Incidents
            </div>
            <div class="kpi-value">
                {critical_incident_count}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


with col2:

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">
                ⚠️ High Anomalies
            </div>
            <div class="kpi-value">
                {high_anomalies}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


with col3:

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">
                📊 Total Anomalies
            </div>
            <div class="kpi-value">
                {total_anomalies}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


with col4:

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">
                📧 Alerts Generated
            </div>
            <div class="kpi-value">
                {alerts_generated}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


st.divider()


# ============================================================
# ANOMALY OVERVIEW
# ============================================================

st.markdown(
    '<div class="section-title">📊 Anomaly Overview</div>',
    unsafe_allow_html=True
)


col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "🔴 Critical",
        critical_anomalies
    )


with col2:

    st.metric(
        "🟠 High",
        high_anomalies
    )


with col3:

    st.metric(
        "🟡 Moderate",
        moderate_anomalies
    )


st.divider()


# ============================================================
# CRITICAL INCIDENTS
# ============================================================

critical_incidents = []

for incident in incidents:

    priority = get_alert_priority(
        incident["Anomalies"]
    )

    if priority == "CRITICAL ALERT":

        critical_incidents.append(
            incident
        )


st.markdown(
    '<div class="section-title">🚨 Critical Alerts</div>',
    unsafe_allow_html=True
)


if not critical_incidents:

    st.success(
        "✅ No critical business incidents detected."
    )

else:

    for incident in critical_incidents:

        st.error(
            f"🚨 CRITICAL ALERT — "
            f"{incident['Date'].date()}"
        )

        st.write(
            f"**Business Issue:** "
            f"{incident['Description']}"
        )

        st.markdown(
            "#### 📌 Detected Metrics"
        )

        for _, row in incident[
            "Anomalies"
        ].iterrows():

            direction_icon = (
                "🔺"
                if row["Direction"] == "UP"
                else "🔻"
            )

            st.write(
                f"{direction_icon} "
                f"**{row['Metric']}** — "
                f"{row['Change_Percentage']:.1f}% "
                f"{row['Direction']} "
                f"({row['Severity']})"
            )


        # ====================================================
        # AI ANALYSIS
        # ====================================================

        with st.expander(
            "🤖 View AI Business Analysis"
        ):

            # Session cache key
            cache_key = (
                str(incident["Date"].date())
                + "_"
                + incident["Description"]
            )


            # Check whether AI result already exists
            if (
                "ai_results"
                not in st.session_state
            ):

                st.session_state[
                    "ai_results"
                ] = {}


            if (
                cache_key
                not in st.session_state[
                    "ai_results"
                ]
            ):

                try:

                    anomaly_data = []

                    for _, row in incident[
                        "Anomalies"
                    ].iterrows():

                        anomaly_data.append(
                            {
                                "Metric": row["Metric"],

                                "Actual_Value":
                                    float(
                                        row[
                                            "Actual_Value"
                                        ]
                                    ),

                                "Baseline":
                                    float(
                                        row[
                                            "Baseline"
                                        ]
                                    ),

                                "Change_Percentage":
                                    float(
                                        row[
                                            "Change_Percentage"
                                        ]
                                    ),

                                "Direction":
                                    row[
                                        "Direction"
                                    ],

                                "Severity":
                                    row[
                                        "Severity"
                                    ]
                            }
                        )


                    with st.spinner(
                        "🤖 AI is analyzing the incident..."
                    ):

                        result = generate_ai_explanation(
                            str(
                                incident[
                                    "Date"
                                ].date()
                            ),

                            incident[
                                "Description"
                            ],

                            anomaly_data
                        )


                    st.session_state[
                        "ai_results"
                    ][cache_key] = result


                except Exception as e:

                    st.error(
                        f"AI analysis failed: {e}"
                    )

                    continue


            # Get cached result

            ai_explanation = (
                st.session_state[
                    "ai_results"
                ][cache_key]
            )


            # =================================================
            # AI RESULT LAYOUT
            # =================================================

            col1, col2 = st.columns(2)


            with col1:

                st.markdown(
                    "### 🧠 What happened"
                )

                st.write(
                    ai_explanation[
                        "what_happened"
                    ]
                )


                st.markdown(
                    "### 🔍 Possible cause"
                )

                st.write(
                    ai_explanation[
                        "possible_cause"
                    ]
                )


            with col2:

                st.markdown(
                    "### 📉 Business impact"
                )

                st.write(
                    ai_explanation[
                        "business_impact"
                    ]
                )


                st.markdown(
                    "### 🎯 Recommended action"
                )

                st.write(
                    ai_explanation[
                        "recommended_action"
                    ]
                )


        st.divider()


# ============================================================
# BUSINESS METRICS
# ============================================================

st.markdown(
    '<div class="section-title">📈 Business Metrics</div>',
    unsafe_allow_html=True
)


tab1, tab2, tab3 = st.tabs(
    [
        "💰 Revenue",
        "👥 Traffic & Orders",
        "💸 Cost & Refunds"
    ]
)


# ============================================================
# REVENUE
# ============================================================

with tab1:

    st.line_chart(
        df.set_index("Date")[
            [
                "Revenue"
            ]
        ],
        width="stretch"
    )


# ============================================================
# TRAFFIC & ORDERS
# ============================================================

with tab2:

    st.line_chart(
        df.set_index("Date")[
            [
                "Traffic",
                "Orders"
            ]
        ],
        width="stretch"
    )


# ============================================================
# COST & REFUNDS
# ============================================================

with tab3:

    st.line_chart(
        df.set_index("Date")[
            [
                "Cost",
                "Refunds"
            ]
        ],
        width="stretch"
    )


st.divider()


# ============================================================
# ANOMALY EXPLORER
# ============================================================

st.markdown(
    '<div class="section-title">🔍 Anomaly Explorer</div>',
    unsafe_allow_html=True
)


filter_col1, filter_col2 = st.columns(2)


# ============================================================
# SEVERITY FILTER
# ============================================================

with filter_col1:

    severity_options = [
        "All",
        "Critical",
        "High",
        "Moderate"
    ]

    selected_severity = st.selectbox(
        "Filter by Severity",
        severity_options
    )


# ============================================================
# METRIC FILTER
# ============================================================

with filter_col2:

    metric_options = [
        "All"
    ] + sorted(
        anomalies[
            "Metric"
        ].unique().tolist()
    )

    selected_metric = st.selectbox(
        "Filter by Metric",
        metric_options
    )


# ============================================================
# APPLY FILTERS
# ============================================================

filtered_anomalies = anomalies.copy()


if selected_severity != "All":

    filtered_anomalies = (
        filtered_anomalies[
            filtered_anomalies[
                "Severity"
            ] == selected_severity
        ]
    )


if selected_metric != "All":

    filtered_anomalies = (
        filtered_anomalies[
            filtered_anomalies[
                "Metric"
            ] == selected_metric
        ]
    )


# ============================================================
# ANOMALY TABLE
# ============================================================

st.dataframe(
    filtered_anomalies[
        [
            "Date",
            "Metric",
            "Actual_Value",
            "Baseline",
            "Change_Percentage",
            "Direction",
            "Severity"
        ]
    ],
    width="stretch",
    hide_index=True
)


st.caption(
    f"Showing {len(filtered_anomalies)} "
    f"of {len(anomalies)} detected anomalies"
)


st.divider()


# ============================================================
# BUSINESS INCIDENT SUMMARY
# ============================================================

st.markdown(
    '<div class="section-title">📋 Business Incident Summary</div>',
    unsafe_allow_html=True
)


for incident in incidents:

    priority = get_alert_priority(
        incident["Anomalies"]
    )


    if priority == "CRITICAL ALERT":

        icon = "🚨"

    elif priority == "HIGH ALERT":

        icon = "⚠️"

    else:

        icon = "ℹ️"


    with st.expander(
        f"{icon} "
        f"{incident['Date'].date()} — "
        f"{priority}"
    ):

        st.write(
            f"**Business Issue:** "
            f"{incident['Description']}"
        )


        st.markdown(
            "#### Detected Metrics"
        )


        for _, row in incident[
            "Anomalies"
        ].iterrows():

            st.write(
                f"- **{row['Metric']}**: "
                f"{row['Change_Percentage']:.1f}% "
                f"{row['Direction']} "
                f"({row['Severity']})"
            )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        AI Anomaly Monitoring Agent
        <br>
        Automated Monitoring • Anomaly Detection •
        AI Business Analysis
    </div>
    """,
    unsafe_allow_html=True
)