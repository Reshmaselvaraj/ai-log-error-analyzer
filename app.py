import streamlit as st
import requests

API_URL = "https://ai-log-error-analyzer.onrender.com/analyzer"

st.title("AI Log Error Analyzer")

st.write(
    "Upload an application log file to analyze errors, severity, "
    "and generate an incident summary."
)

uploaded_file = st.file_uploader(
    "Upload .log file", type=["log", "txt"]
)

if uploaded_file and st.button("Analyze Logs"):
    with st.spinner("Analyzing logs..."):
        response = requests.post(
            API_URL,
            files={
                "file": (
                    uploaded_file.name,
                    uploaded_file,
                    uploaded_file.type,
                )
            },
        )

    if response.status_code == 200:
        data = response.json()

        st.subheader("Log Analysis Results")
        st.dataframe(data["logs"])

        if data["clusters"]:
            st.subheader("AI-assisted UNKNOWN Error Grouping")
            for cluster, msgs in data["clusters"].items():
                st.write(f"**Cluster {cluster}**")
                for m in msgs:
                    st.write("-", m)

        st.subheader("Incident Summary")
        st.text(data["summary"])

    else:
        st.error(
            f"Failed to analyze logs "
            f"(status code {response.status_code})"
        )
