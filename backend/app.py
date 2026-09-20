import os
from flask import Flask, render_template, jsonify, request
from risk_engine import get_processed_students, get_cohort_stats, evaluate_student, RAW_STUDENTS

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
FRONTEND_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "frontend"))

# Configure Flask to resolve templates and static assets directly from the frontend directory
app = Flask(
    __name__,
    template_folder=FRONTEND_DIR,
    static_folder=FRONTEND_DIR,
    static_url_path="/static"
)

@app.route("/")
def index():
    return render_template("index.html")

# --- PRERAK JSON API Layer ---

@app.route("/api/students", methods=["GET"])
def api_get_students():
    """Returns all processed students with risk scores, indicators, and interventions."""
    students = get_processed_students()
    return jsonify(students)

@app.route("/api/stats", methods=["GET"])
def api_get_stats():
    """Returns aggregated cohort risk statistics (counts for high, medium, low)."""
    stats = get_cohort_stats()
    return jsonify(stats)

@app.route("/api/students/<student_id>", methods=["GET"])
def api_get_student_by_id(student_id):
    """Returns full processed profile for a single student or HTTP 404 if not found."""
    students = get_processed_students()
    student = next((s for s in students if s["id"].lower() == student_id.lower()), None)
    if student is None:
        return jsonify({
            "error": "Student not found",
            "message": f"Student ID '{student_id}' does not exist in the active cohort."
        }), 404
    return jsonify(student)

@app.route("/api/students/<student_id>/simulate", methods=["POST"])
def api_simulate_intervention(student_id):
    """
    Simulates retention intervention impact on a student's risk score
    using the existing risk_engine scoring rules without persisting changes.
    """
    raw_student = next((s for s in RAW_STUDENTS if s["id"].lower() == student_id.lower()), None)
    if raw_student is None:
        return jsonify({
            "error": "Student not found",
            "message": f"Student ID '{student_id}' does not exist in the active cohort."
        }), 404

    data = request.get_json(silent=True)
    if not data or not isinstance(data, dict):
        return jsonify({
            "error": "Bad Request",
            "message": "Request body must be a valid JSON object containing simulation parameters."
        }), 400

    required_fields = ["attendance", "engagement", "backlogs", "assessment_score"]
    for field in required_fields:
        if field not in data or data[field] is None:
            return jsonify({
                "error": "Bad Request",
                "message": f"Missing required simulation parameter: '{field}'."
            }), 400

    try:
        sim_attendance = float(data["attendance"])
        sim_engagement = float(data["engagement"])
        sim_backlogs = int(data["backlogs"])
        sim_assessment = float(data["assessment_score"])
    except (ValueError, TypeError):
        return jsonify({
            "error": "Bad Request",
            "message": "Simulation parameters must be valid numeric values."
        }), 400

    # Range validations
    if not (0 <= sim_attendance <= 100):
        return jsonify({
            "error": "Bad Request",
            "message": "Attendance must be between 0 and 100."
        }), 400
    if not (0 <= sim_engagement <= 100):
        return jsonify({
            "error": "Bad Request",
            "message": "Engagement must be between 0 and 100."
        }), 400
    if not (0 <= sim_backlogs <= 20):
        return jsonify({
            "error": "Bad Request",
            "message": "Backlogs must be between 0 and 20."
        }), 400
    if not (0 <= sim_assessment <= 100):
        return jsonify({
            "error": "Bad Request",
            "message": "Assessment score must be between 0 and 100."
        }), 400

    # Evaluate current baseline using existing scoring logic
    current_eval = evaluate_student(raw_student)

    # Evaluate simulated values using the EXACT SAME scoring rules
    # Shallow copy guarantees raw_student is not modified
    simulated_student = {
        **raw_student,
        "attendance": int(round(sim_attendance)),
        "engagement": int(round(sim_engagement)),
        "backlogs": sim_backlogs,
        "assessment_score": int(round(sim_assessment))
    }
    simulated_eval = evaluate_student(simulated_student)

    score_diff = simulated_eval["risk_score"] - current_eval["risk_score"]

    return jsonify({
        "student_id": raw_student["id"],
        "student_name": raw_student["name"],
        "current_risk_score": current_eval["risk_score"],
        "current_risk_level": current_eval["risk_level"],
        "projected_risk_score": simulated_eval["risk_score"],
        "projected_risk_level": simulated_eval["risk_level"],
        "score_difference": score_diff,
        "simulated_values": {
            "attendance": sim_attendance,
            "engagement": sim_engagement,
            "backlogs": sim_backlogs,
            "assessment_score": sim_assessment
        },
        "simulated_signals": simulated_eval["signals"],
        "is_simulation": True,
        "disclaimer": "SIMULATION — NOT ACTUAL STUDENT DATA"
    }), 200

if __name__ == "__main__":
    # Allows running directly via `python app.py` from the backend directory
    app.run(debug=True, host="127.0.0.1", port=5000)
