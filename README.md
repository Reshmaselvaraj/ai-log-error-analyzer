# Ai-log-error-analyzer
## AI-assisted log analysis for enterprise application logs using FastAPI and Streamlit

## Live Demo:

**Frontend (Streamlit)**: https://ai-log-error-analyzer-wzfms6tmadswxkwp7fke5d.streamlit.app/

**Backend (FastAPI)**: https://ai-log-error-analyzer.onrender.com

![Animation 1](https://github.com/user-attachments/assets/24d3fad6-daff-4f70-a0dc-b1100eee0ff2)

![Animation 2](https://github.com/user-attachments/assets/270197e7-54ef-459a-a4c6-fe7e60d6ebff)

![Animation 3](https://github.com/user-attachments/assets/5e80bbda-7000-43af-9d6e-f2b0dd741f94)

**📌Project Summary**

AI Log Error Analyzer is an AI-assisted system designed to help support and platform engineers analyze real-world enterprise application logs efficiently.
The project combines deterministic logic, machine learning, and large language models (LLMs) in a responsible, production-safe way.

The application is fully deployed using FastAPI (backend) and Streamlit (frontend) on free cloud platforms, making it publicly accessible for demonstration and evaluation.

**🎯Problem Statement**

In large enterprise systems, application logs are:

- Extremely verbose  
- Difficult to scan manually  
- Filled with startup noise and INFO logs  
- Hard to summarize during incidents  
- Often contain unknown or previously unseen errors  

- Support engineers typically spend hours:
  - Searching for ERROR/WARN messages  
  - Grouping similar failures  
  - Determining severity  
  - Writing incident summaries  

- This project aims to reduce manual triage effort by building an intelligent assistant that:
  - Structures raw logs  
  - Prioritizes critical issues  
  - Discovers unknown error patterns  
  - Generates clear incident summaries  


🧠 Design Philosophy

- The system follows a **production-first AI philosophy**:
  - Rules before AI → Predictability and trust  
  - ML only where labels don’t exist → Pattern discovery  
  - LLMs only for summarization → Low-risk, high-value usage  
  - Graceful degradation → Works even without AI APIs  
  - Enterprise realism → Handles real WildFly/JBoss logs  

- This avoids the common **“AI everywhere” anti-pattern**

### 🏗️ Architecture Overview 

- **Streamlit Frontend**
  - Provides a simple and interactive UI for uploading logs and viewing results.

- **FastAPI Backend**
  - Acts as the core processing engine and API layer.
  - Handles request validation, processing, and response generation.

- **Log Processing & Intelligence Layer**
  - **Log Parsing:** Extracts structured information using regex and preprocessing.
  - **Rule-based Classification:** Identifies known error patterns.
  - **Severity Assignment:** Assigns severity levels based on predefined rules.
  - **ML Clustering:** Uses TF-IDF + KMeans to group similar log events.
  - **LLM / Fallback Summary:** Generates human-readable incident summaries when rules or ML confidence is low.

- **Structured Results**
  - Outputs normalized, categorized, and summarized incident data for analysis and reporting.

## 🔍 Step-by-Step Implementation

### 1️⃣ Real Enterprise Log Parsing

Instead of simplified demo logs, the system supports **WildFly / JBoss–style enterprise logs**, which typically contain:

- Embedded log levels  
- Component and module names  
- ANSI color codes  
- Noisy startup and system messages  

A **custom log parser** was implemented to:

- Strip ANSI escape characters  
- Extract **timestamp, log level, component, and message**  
- Ignore irrelevant or noisy lines  
- Safely process **large log files** without memory issues  

This ensures the system works reliably on **real production logs**, not synthetic samples.

---

### 2️⃣ Deterministic Error Classification

A **rule-based classifier** maps log messages into well-defined categories:

- `DATABASE`
- `TIMEOUT`
- `MEMORY`
- `API`
- `UNKNOWN`

This approach mirrors how **L2/L3 support engineers** triage incidents and ensures:

- Full explainability  
- Predictable behavior  
- Zero dependency on probabilistic models  

---

### 3️⃣ Severity Assignment

Severity is assigned **deterministically** based on log level:

| Log Level | Severity |
|----------|----------|
| ERROR    | HIGH     |
| WARN     | MEDIUM   |
| INFO    | LOW      |

This guarantees **consistent prioritization** without relying on AI-driven inference.

---

### 4️⃣ ML-Based Unknown Error Grouping

Some errors cannot be classified using rules alone.  
For these cases, **unsupervised machine learning** is applied:

- **TF-IDF** for text vectorization  
- **KMeans** for clustering `UNKNOWN` and `ERROR` messages  

This helps uncover **recurring hidden patterns** in production logs.

#### Production Challenge Addressed
- NumPy data types are **not JSON-serializable**
- Cluster IDs were explicitly converted to **JSON-safe types** before returning API responses  

---

### 5️⃣ LLM-Based Incident Summarization (Optional)

An **LLM is used only for summarization**, not decision-making.

The system:
- Generates human-readable incident summaries  
- Suggests possible next actions  
- Limits prompt size for safety and cost control  

#### Critical Design Choice
If the LLM API is unavailable (missing key, quota exceeded, or network failure), the system **falls back to a deterministic summary** instead of crashing.

This enables:
- Free-tier hosting  
- Stable deployments  
- Responsible AI usage  

---

### 6️⃣ Backend: FastAPI

**FastAPI** was chosen for its:

- High performance  
- Clean API design  
- Production readiness  

The backend:
- Accepts multipart file uploads  
- Safely processes logs with size limits  
- Returns structured JSON responses  
- Never fails due to optional AI components  

---

### 7️⃣ Frontend: Streamlit

**Streamlit** provides a lightweight UI for:

- Uploading log files  
- Viewing structured log tables  
- Inspecting ML clusters  
- Reading incident summaries  

Several real-world integration issues were resolved during development, including:
- Multipart upload handling  
- API endpoint mismatches  
- Frontend–backend connectivity  

---

## 🧪 Debugging & Production Challenges Solved

During development and deployment, multiple real-world issues were identified and fixed:

- Python and `pip` PATH issues on Windows  
- Missing dependencies in cloud environments  
- JSON serialization errors from ML outputs  
- FastAPI multipart file upload handling  
- API endpoint mismatches (`/analyze` vs `/analyzer`)  
- Environment variable configuration for secrets  
- Optional AI dependencies causing startup crashes  

These fixes significantly improved **system robustness and reliability**.

---

## ☁️ Deployment (100% Free)

### Backend
- Hosted on **Render (Free Tier)**  
- Secrets managed using environment variables  
- Handles cold starts gracefully  

### Frontend
- Hosted on **Streamlit Cloud**  
- Automatically redeploys on GitHub updates  
- Communicates securely with backend via HTTPS  

The entire system runs with **zero paid infrastructure**.

---

## 🧰 Tech Stack

- **Language:** Python  
- **Backend:** FastAPI  
- **Frontend:** Streamlit  
- **ML:** scikit-learn (TF-IDF, KMeans)  
- **AI:** OpenAI API (optional, with fallback)  
- **Hosting:** Render + Streamlit Cloud  
- **Version Control:** Git & GitHub  

