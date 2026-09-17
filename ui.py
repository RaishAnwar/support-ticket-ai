import streamlit as st
import requests
import pandas as pd

API_URL = "https://support-ticket-ai-mkye.onrender.com"


st.set_page_config(
    page_title="Support Ticket AI",
    page_icon="🎫",
    layout="wide"
)


st.title("🎫 Support Ticket AI")
st.caption("AI-powered customer support ticket analysis")


#
# Natural Language Query


st.header("Ask Questions")

st.write(
    "Ask questions about support tickets using natural language. "
    "The AI converts your question into SQL and retrieves the answer from the database."
)

question = st.text_input(
    "Enter your question",
    placeholder="Example: How many tickets are currently open?"
)


if st.button("Ask Question", type="primary"):

    if not question:
        st.warning("Please enter a question.")

    else:
        try:
            response = requests.post(
                f"{API_URL}/query",
                json={"question": question}
            )

            response.raise_for_status()

            result = response.json()

            st.subheader("Answer")
            df = pd.DataFrame(
             result["rows"],
             columns=result["columns"]
        )

            st.dataframe(
            df,
            use_container_width=True
     )
            with st.expander("View Generated SQL"):
                st.code(
                    result["sql"],
                    language="sql"
                )

        except requests.exceptions.RequestException:
            st.error(
                "Unable to connect to the API. "
                "Make sure the FastAPI server is running."
            )


# -----------------------------
# Example Queries
# -----------------------------

st.subheader("Example Questions")

st.write("Try questions like:")

st.markdown(
    """
- How many tickets are currently open?
- Which agent resolved the most tickets this month?
- Show me all Critical tickets not resolved within 12 hours.
- What is the average customer rating for Technical category tickets?
"""
)


# -----------------------------
# Anomaly Detection
# -----------------------------

st.divider()

st.header("Anomaly Detection")

st.write(
    "The system checks the support ticket data for abnormal or potentially risky tickets."
)

col1, col2 = st.columns(2)

with col1:
    st.info(
        "**Long Resolution Times**\n\n"
        "Identifies tickets whose resolution time is unusually high "
        "compared with the other resolved tickets."
    )

with col2:
    st.warning(
        "**Critical Unresolved Tickets**\n\n"
        "Identifies high-priority unresolved tickets that have remained "
        "open for more than 24 hours."
    )


if st.button("Run Anomaly Detection"):

    try:
        response = requests.get(
            f"{API_URL}/anomalies"
        )

        response.raise_for_status()

        result = response.json()

        long_resolution = result["long_resolution_anomalies"]
        critical_unresolved = result["critical_unresolved_over_24h"]

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Long Resolution Anomalies",
                len(long_resolution)
            )

        with col2:
            st.metric(
                "Critical Unresolved > 24h",
                len(critical_unresolved)
            )

        st.subheader("Long Resolution Anomalies")

        if long_resolution:
            st.dataframe(
                long_resolution,
                use_container_width=True
            )
        else:
            st.success("No long-resolution anomalies found.")

        st.subheader(
            "Critical Unresolved Tickets Older Than 24 Hours"
        )

        if critical_unresolved:
            st.dataframe(
                critical_unresolved,
                use_container_width=True
            )
        else:
            st.success(
                "No critical unresolved tickets older than 24 hours found."
            )

    except requests.exceptions.RequestException:
        st.error(
            "Unable to connect to the API. "
            "Make sure the FastAPI server is running."
        )


# -----------------------------
# Health Status
# -----------------------------

st.divider()

st.header("System Status")

if st.button("Check API Health"):

    try:
        response = requests.get(
            f"{API_URL}/health"
        )

        response.raise_for_status()

        result = response.json()

        if result["status"] == "healthy":
            st.success("API is healthy and running.")
        else:
            st.error("API is not healthy.")

    except requests.exceptions.RequestException:
        st.error("API is not reachable.")