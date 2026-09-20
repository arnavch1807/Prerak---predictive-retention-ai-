# PRERAK — Predictive Retention AI

> Early warning system for student dropout risk  
> **Problem Statement CX0701**: *"The Dropout Nobody Predicted"*  
> Hackathon MVP Prototype

---

## 1. Problem

Higher education institutions struggle with student attrition that often goes unnoticed until it is too late. Conventional tracking systems flag students only after catastrophic academic failures—such as failing end-semester exams, accumulating multiple backlogs, or completely discontinuing attendance.

In reality, student dropout is rarely an abrupt event; it is the culmination of gradual, compounding warning signals across attendance velocity, coursework engagement, internal assessments, and administrative hurdles. By identifying these early warning signals in real time, academic advisors and institutions can deliver targeted, proactive interventions before academic withdrawal becomes irreversible.

---

## 2. Solution

**PRERAK** is an explainable, predictive student-retention dashboard designed to surface early dropout indicators and formulate timely action plans. 

PRERAK:
* **Analyzes multidimensional student risk signals** across attendance, academics, engagement, and financial indicators.
* **Generates a transparent 0–100 Risk Score** reflecting cumulative risk factors without black-box complexity.
* **Classifies students into actionable tiers**: HIGH, MEDIUM, and LOW risk.
* **Itemizes detected signals** to explain the root causes behind each student's evaluation.
* **Recommends targeted interventions** tailored to address the student's specific warning indicators.
* **Provides an Intervention Simulator** for evaluating what-if retention scenarios.

> **Note:** The current prototype uses a representative in-memory dataset of 6 student profiles to demonstrate the end-to-end early warning and intervention workflow.

---

## 3. Core Workflow

```text
Student Signals
      ↓
 Risk Engine
      ↓
Risk Score + Risk Level
      ↓
Detected Signals
      ↓
Recommended Intervention
      ↓
Intervention Simulator
```

1. **Student Signals**: Raw academic, attendance, LMS engagement, backlog, and financial data are ingested.
2. **Risk Engine**: The heuristic evaluation engine processes signals against established threshold rules.
3. **Risk Score + Risk Level**: The student is assigned a quantified 0–100 Risk Score and categorized as HIGH, MEDIUM, or LOW risk.
4. **Detected Signals**: The primary warning indicators triggering the risk score are itemized and explained.
5. **Recommended Intervention**: Targeted retention strategies (e.g., Attendance Recovery Plans, Peer Mentorship, Academic Counseling) are formulated.
6. **Intervention Simulator**: Advisors model hypothetical parameter improvements (e.g., raising attendance or clearing backlogs) and project the resulting score reduction in real time.

---

## 4. Key Features

* **Cohort Risk Intelligence**: Executive overview cards displaying total analyzed students, high-risk cohort size, mean cohort risk score, and count of students requiring active intervention.
* **Student Risk Dashboard**: Clean, scannable student directory table featuring dynamic 0–100 progress meters, department metadata, and primary warning indicators.
* **Transparent Risk Scoring**: Explainable point-based heuristic model from 0 to 100 with clear categorization into HIGH, MEDIUM, and LOW tiers.
* **Detected Signals**: Granular breakdown of individual risk drivers including attendance drop velocity, CGPA trajectory, LMS engagement shifts, backlog counts, and financial hold flags.
* **Recommended Intervention**: Action-oriented intervention plans mapped directly to detected warning signals.
* **Intervention Simulator**: Interactive what-if modeling sliders allowing advisors to adjust target attendance, engagement, backlogs, and assessment scores.
* **Non-Destructive Simulation**: What-if projections are evaluated through a dedicated backend endpoint that preserves actual in-memory student records without mutation.
* **Responsive Dark Dashboard**: Professional, high-contrast dark aesthetic built with pure vanilla HTML, CSS, and modern typography optimized for demo presentations.

---

## 5. Architecture

```text
Frontend
├── frontend/index.html
├── frontend/style.css
└── JavaScript using Fetch API
         ↓  (HTTP REST JSON)
Backend
├── backend/app.py
└── Flask REST API
         ↓  (Internal Evaluation)
Risk Engine
└── backend/risk_engine.py
```

* **Frontend**: Vanilla HTML5, modern CSS, and lightweight JavaScript using the native Fetch API. Asynchronously queries backend REST endpoints to populate metrics, render cohort tables, open modal deep-dives, and submit what-if simulations.
* **Backend**: Python Flask application (`backend/app.py`) providing a lightweight REST API that handles cohort queries, student profile lookups, and simulation requests with strict input validation.
* **Risk Engine**: Modular Python evaluation logic (`backend/risk_engine.py`) containing the in-memory cohort dataset and deterministic scoring rules applied consistently to both actual and simulated student signals.

---

## 6. Project Structure

```text
PRERAK/
├── backend/
│   ├── app.py              # Flask application & JSON REST API routes
│   ├── risk_engine.py      # Explainable scoring heuristics & mock cohort data
│   └── requirements.txt    # Python dependencies (Flask)
├── frontend/
│   ├── index.html          # Dashboard, modal workflow & simulator UI
│   └── style.css           # Styling, design tokens, progress bars & animations
└── README.md               # Project documentation & run guide
```

---

## 7. Risk Scoring

The prototype evaluates each student across five observable dimensions:

1. **Attendance & Attendance Trend**: Current attendance level (<60% critical, <75% warning) and cross-term rate of decline.
2. **Academic & Backlog Indicators**: Active course backlogs and cumulative GPA levels / drops.
3. **Engagement**: Digital LMS activity level and recent engagement drops.
4. **Assessment Performance**: Scores on internal continuous assessments (<45 passing standard).
5. **Financial Indicators**: Administrative flags such as overdue tuition fee installments.

### Risk Classification Thresholds

| Risk Score | Risk Level | Meaning & Action |
| :---: | :---: | :--- |
| **70 – 100** | **HIGH** | Severe multi-signal attrition risk; immediate retention intervention advised. |
| **40 – 69** | **MEDIUM** | Emerging warning indicators; proactive academic mentorship check-in advised. |
| **0 – 39** | **LOW** | Stable progression within healthy benchmark parameters. |

> **Terminology Note:** The 0–100 metric is defined strictly as a **Risk Score** reflecting heuristic penalty points, NOT a statistical probability.

---

## 8. API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/` | Serves the main PRERAK frontend dashboard (`frontend/index.html`). |
| `GET` | `/api/students` | Returns JSON array of all students with evaluated risk scores, levels, signals, and interventions. |
| `GET` | `/api/stats` | Returns cohort summary statistics (`high`, `medium`, `low`, and `total` counts). |
| `GET` | `/api/students/<student_id>` | Returns processed profile, trend metrics, itemized signals, and action plans for a specific student (`404` if not found). |
| `POST` | `/api/students/<student_id>/simulate` | Accepts simulated parameters (`attendance`, `engagement`, `backlogs`, `assessment_score`) and returns projected risk score, projected tier, and delta without mutating stored data. |

---

## 9. Quickstart & How to Run

### Prerequisites
* Python 3.10 or higher
* `pip` package manager

### 1. Install Dependencies
```bash
pip install -r backend/requirements.txt
```

### 2. Start Flask Application
```bash
cd backend
python app.py
```

### 3. Open in Browser
Navigate to:
```
http://127.0.0.1:5000/
```
