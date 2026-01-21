from fastapi import FastAPI, UploadFile, File, HTTPException
import tempfile
import traceback

from log_parser import parse_logs
from error_classifier import classify_error
from severity import assign_severity
from ml_cluster import cluster_unknown_errors
from llm_summary import generate_incident_summary

app = FastAPI(title="AI Log Error Analyzer API")


@app.post("/analyze")
async def analyze_log(file: UploadFile = File(...)):
    try:
        # -----------------------------
        # Save uploaded file temporarily
        # -----------------------------
        with tempfile.NamedTemporaryFile(delete=False, suffix=".log") as temp:
            temp.write(await file.read())
            temp_path = temp.name

        # -----------------------------
        # Parse logs (WildFly/JBoss)
        # -----------------------------
        parsed_logs = parse_logs(temp_path)

        results = []
        unknown_messages = []

        # HARD LIMIT for safety with large logs
        for log in parsed_logs[:5000]:
            category = classify_error(log["message"])
            severity = assign_severity(log["level"], category)

            entry = {
                "timestamp": log["timestamp"],
                "level": log["level"],
                "component": log.get("component", "unknown"),
                "message": log["message"],
                "category": category,
                "severity": severity,
            }

            results.append(entry)

            if category == "UNKNOWN" and log["level"] == "ERROR":
                unknown_messages.append(log["message"])

        # -----------------------------
        # ML clustering (JSON-safe)
        # -----------------------------
        raw_clusters = (
            cluster_unknown_errors(unknown_messages)
            if unknown_messages
            else {}
        )

        # Convert numpy keys → JSON-safe strings
        clusters = {
            str(int(cluster_id)): messages
            for cluster_id, messages in raw_clusters.items()
        }

        # -----------------------------
        # Incident summary (LLM or fallback)
        # -----------------------------
        summary = generate_incident_summary(results)

        return {
            "logs": results,
            "clusters": clusters,
            "summary": summary,
        }

    except Exception as e:
        # Log backend error for debugging
        print("❌ Backend error:")
        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )
