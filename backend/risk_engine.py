# ponytail: In-memory student cohort and explainable retention scoring logic.
# Ceiling: Heuristic point-based evaluation without persistent database or online model training.
# Upgrade path: Replace rule points with a trained classifier (e.g. Scikit-learn Random Forest/XGBoost).

RAW_STUDENTS = [
    # 1. Aarav Sharma (HIGH - 90) - Low attendance, 2 backlogs, rapid engagement drop, failing assessment
    {
        "id": "STU-2024-01",
        "name": "Aarav Sharma",
        "department": "Computer Science",
        "attendance": 52,
        "previous_attendance": 84,
        "cgpa": 5.6,
        "previous_cgpa": 6.8,
        "backlogs": 2,
        "engagement": 38,
        "previous_engagement": 74,
        "financial_flag": False,
        "assessment_score": 41
    },
    # 2. Pooja Patel (HIGH - 85) - Declining attendance, 2 backlogs, low assessment, financial hold
    {
        "id": "STU-2024-02",
        "name": "Pooja Patel",
        "department": "Electronics & Comm.",
        "attendance": 61,
        "previous_attendance": 76,
        "cgpa": 6.1,
        "previous_cgpa": 6.9,
        "backlogs": 2,
        "engagement": 45,
        "previous_engagement": 70,
        "financial_flag": True,
        "assessment_score": 44
    },
    # 3. Rohan Deshmukh (MEDIUM - 47) - 1 backlog, declining engagement, moderate attendance
    {
        "id": "STU-2024-03",
        "name": "Rohan Deshmukh",
        "department": "Mechanical Eng.",
        "attendance": 71,
        "previous_attendance": 80,
        "cgpa": 6.7,
        "previous_cgpa": 7.2,
        "backlogs": 1,
        "engagement": 58,
        "previous_engagement": 72,
        "financial_flag": False,
        "assessment_score": 52
    },
    # 4. Ananya Iyer (MEDIUM - 64) - 1 backlog, financial hold, low engagement, moderate CGPA drop
    {
        "id": "STU-2024-04",
        "name": "Ananya Iyer",
        "department": "Information Tech.",
        "attendance": 68,
        "previous_attendance": 82,
        "cgpa": 6.8,
        "previous_cgpa": 7.4,
        "backlogs": 1,
        "engagement": 52,
        "previous_engagement": 69,
        "financial_flag": True,
        "assessment_score": 54
    },
    # 5. Vikram Singh (LOW - 0) - Exemplary student, high attendance & CGPA
    {
        "id": "STU-2024-05",
        "name": "Vikram Singh",
        "department": "Computer Science",
        "attendance": 93,
        "previous_attendance": 95,
        "cgpa": 8.8,
        "previous_cgpa": 8.7,
        "backlogs": 0,
        "engagement": 91,
        "previous_engagement": 90,
        "financial_flag": False,
        "assessment_score": 89
    },
    # 6. Sneha Kulkarni (LOW - 0) - Consistent high performer
    {
        "id": "STU-2024-06",
        "name": "Sneha Kulkarni",
        "department": "Civil Eng.",
        "attendance": 88,
        "previous_attendance": 89,
        "cgpa": 8.3,
        "previous_cgpa": 8.4,
        "backlogs": 0,
        "engagement": 82,
        "previous_engagement": 84,
        "financial_flag": False,
        "assessment_score": 82
    },
    # 7. Kabir Mehta (HIGH - 90) - Critical attendance (48%), 3 backlogs, low CGPA, weak assessment
    {
        "id": "STU-2024-07",
        "name": "Kabir Mehta",
        "department": "Mechanical Eng.",
        "attendance": 48,
        "previous_attendance": 72,
        "cgpa": 5.2,
        "previous_cgpa": 6.1,
        "backlogs": 3,
        "engagement": 36,
        "previous_engagement": 65,
        "financial_flag": False,
        "assessment_score": 39
    },
    # 8. Meera Nair (MEDIUM - 44) - Declining LMS engagement & assessment, 1 backlog
    {
        "id": "STU-2024-08",
        "name": "Meera Nair",
        "department": "Biotechnology",
        "attendance": 73,
        "previous_attendance": 80,
        "cgpa": 6.4,
        "previous_cgpa": 6.7,
        "backlogs": 1,
        "engagement": 60,
        "previous_engagement": 76,
        "financial_flag": False,
        "assessment_score": 55
    },
    # 9. Arjun Reddy (MEDIUM - 57) - Attendance drop, 1 backlog, financial flag
    {
        "id": "STU-2024-09",
        "name": "Arjun Reddy",
        "department": "Civil Eng.",
        "attendance": 66,
        "previous_attendance": 74,
        "cgpa": 6.5,
        "previous_cgpa": 7.1,
        "backlogs": 1,
        "engagement": 54,
        "previous_engagement": 65,
        "financial_flag": True,
        "assessment_score": 48
    },
    # 10. Diya Sen (MEDIUM - 42) - Attendance under 75, 1 backlog, declining trend
    {
        "id": "STU-2024-10",
        "name": "Diya Sen",
        "department": "Computer Science",
        "attendance": 72,
        "previous_attendance": 84,
        "cgpa": 6.8,
        "previous_cgpa": 7.2,
        "backlogs": 1,
        "engagement": 62,
        "previous_engagement": 72,
        "financial_flag": False,
        "assessment_score": 50
    },
    # 11. Aditya Verma (MEDIUM - 46) - Attendance 62%, CGPA drop below 6.0, 1 backlog
    {
        "id": "STU-2024-11",
        "name": "Aditya Verma",
        "department": "Electrical Eng.",
        "attendance": 62,
        "previous_attendance": 75,
        "cgpa": 5.9,
        "previous_cgpa": 6.5,
        "backlogs": 1,
        "engagement": 68,
        "previous_engagement": 75,
        "financial_flag": False,
        "assessment_score": 58
    },
    # 12. Priyanka Joshi (LOW - 27) - Financial hold, minor engagement drop, 0 backlogs
    {
        "id": "STU-2024-12",
        "name": "Priyanka Joshi",
        "department": "Electronics & Comm.",
        "attendance": 76,
        "previous_attendance": 79,
        "cgpa": 6.6,
        "previous_cgpa": 6.9,
        "backlogs": 0,
        "engagement": 65,
        "previous_engagement": 77,
        "financial_flag": True,
        "assessment_score": 54
    },
    # 13. Harish Rao (LOW - 0) - Steady academic performance and high attendance
    {
        "id": "STU-2024-13",
        "name": "Harish Rao",
        "department": "Civil Eng.",
        "attendance": 91,
        "previous_attendance": 92,
        "cgpa": 8.1,
        "previous_cgpa": 8.0,
        "backlogs": 0,
        "engagement": 88,
        "previous_engagement": 87,
        "financial_flag": False,
        "assessment_score": 85
    },
    # 14. Isha Gupta (LOW - 0) - Strong academic progress and LMS activity
    {
        "id": "STU-2024-14",
        "name": "Isha Gupta",
        "department": "Computer Science",
        "attendance": 86,
        "previous_attendance": 88,
        "cgpa": 7.8,
        "previous_cgpa": 7.9,
        "backlogs": 0,
        "engagement": 79,
        "previous_engagement": 81,
        "financial_flag": False,
        "assessment_score": 76
    },
    # 15. Karthik Subramanian (LOW - 0) - Reliable engagement and healthy coursework
    {
        "id": "STU-2024-15",
        "name": "Karthik Subramanian",
        "department": "Electrical Eng.",
        "attendance": 82,
        "previous_attendance": 83,
        "cgpa": 7.4,
        "previous_cgpa": 7.5,
        "backlogs": 0,
        "engagement": 75,
        "previous_engagement": 77,
        "financial_flag": False,
        "assessment_score": 68
    },
    # 16. Neha Choudhury (LOW - 5) - Minor attendance drop, good CGPA
    {
        "id": "STU-2024-16",
        "name": "Neha Choudhury",
        "department": "Information Tech.",
        "attendance": 77,
        "previous_attendance": 86,
        "cgpa": 7.2,
        "previous_cgpa": 7.4,
        "backlogs": 0,
        "engagement": 73,
        "previous_engagement": 76,
        "financial_flag": False,
        "assessment_score": 65
    },
    # 17. Rahul Bhatia (LOW - 11) - Average CGPA and test, but 0 backlogs and good attendance
    {
        "id": "STU-2024-17",
        "name": "Rahul Bhatia",
        "department": "Mechanical Eng.",
        "attendance": 80,
        "previous_attendance": 82,
        "cgpa": 6.7,
        "previous_cgpa": 6.9,
        "backlogs": 0,
        "engagement": 70,
        "previous_engagement": 72,
        "financial_flag": False,
        "assessment_score": 54
    },
    # 18. Tanvi Sharma (LOW - 21) - Minor drop in attendance and engagement, financial flag
    {
        "id": "STU-2024-18",
        "name": "Tanvi Sharma",
        "department": "Biotechnology",
        "attendance": 76,
        "previous_attendance": 85,
        "cgpa": 7.1,
        "previous_cgpa": 7.3,
        "backlogs": 0,
        "engagement": 66,
        "previous_engagement": 75,
        "financial_flag": True,
        "assessment_score": 62
    }
]

def evaluate_student(s):
    """
    Calculates a transparent Risk Score (0-100), risk classification (HIGH, MEDIUM, LOW),
    detected warning indicators, and actionable intervention recommendations.
    """
    points = 0
    signals = []
    interventions = []

    # 1. Attendance Level & Trend Signals
    att_drop = s["previous_attendance"] - s["attendance"]
    if att_drop >= 15:
        points += 10
        signals.append(f"Attendance declining rapidly (-{att_drop}% drop)")
    elif att_drop >= 8:
        points += 5
        signals.append(f"Attendance declining (-{att_drop}% drop)")

    if s["attendance"] < 60:
        points += 20
        signals.append(f"Attendance critical ({s['attendance']}%) - below 60% minimum")
        interventions.append("Attendance recovery plan")
    elif s["attendance"] < 75:
        points += 10
        signals.append(f"Attendance warning ({s['attendance']}%) - below 75% threshold")
        interventions.append("Attendance recovery plan")

    # 2. Backlogs & Academic Performance
    if s["backlogs"] >= 2:
        points += 20
        signals.append(f"Multiple backlogs ({s['backlogs']} courses active)")
        interventions.append("Backlog counselling")
    elif s["backlogs"] == 1:
        points += 10
        signals.append("1 active course backlog")
        interventions.append("Backlog counselling")

    cgpa_drop = round(s["previous_cgpa"] - s["cgpa"], 2)
    if cgpa_drop >= 0.5:
        points += 5
        signals.append(f"CGPA declining (-{cgpa_drop:.1f} semester drop)")
        interventions.append("Academic mentoring")

    if s["cgpa"] < 6.0:
        points += 10
        signals.append(f"Low CGPA ({s['cgpa']:.1f})")
        if "Academic mentoring" not in interventions:
            interventions.append("Academic mentoring")
    elif s["cgpa"] < 7.0:
        points += 5

    # 3. Engagement & Assessment Signals
    eng_drop = s["previous_engagement"] - s["engagement"]
    if eng_drop >= 15:
        points += 13
        signals.append(f"Engagement declining (-{eng_drop}% in LMS)")
        interventions.append("Faculty follow-up")
    elif eng_drop >= 8:
        points += 6
        signals.append(f"Engagement declining (-{eng_drop}%)")
    elif s["engagement"] < 50:
        points += 6
        signals.append(f"Low engagement ({s['engagement']}%)")

    if s["assessment_score"] < 45:
        points += 12
        signals.append(f"Low assessment performance ({s['assessment_score']}/100)")
        if "Faculty follow-up" not in interventions:
            interventions.append("Faculty follow-up")
    elif s["assessment_score"] < 60:
        points += 6
        signals.append(f"Marginal assessment performance ({s['assessment_score']}/100)")

    # 4. Financial Flag
    if s["financial_flag"]:
        points += 10
        signals.append("Financial flag (tuition fee overdue)")
        interventions.append("Financial support counselling")

    # Clamp Risk Score to 0-100
    risk_score = min(100, max(0, points))

    # Risk classification:
    # 70-100 = HIGH, 40-69 = MEDIUM, 0-39 = LOW
    if risk_score >= 70:
        risk_level = "HIGH"
    elif risk_score >= 40:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"

    # Fallback indicators & interventions for healthy low-risk students
    if not signals:
        signals.append("Metrics within healthy parameters")
    if not interventions:
        interventions.append("Regular academic progress tracking")

    primary_indicator = signals[0]

    att_diff = -att_drop
    cgpa_diff = round(s["cgpa"] - s["previous_cgpa"], 2)
    eng_diff = -eng_drop

    return {
        **s,
        "risk_score": risk_score,
        "risk_level": risk_level,
        "primary_indicator": primary_indicator,
        "signals": signals,
        "interventions": interventions,
        "attendance_trend": f"{s['attendance']}% (was {s['previous_attendance']}%)",
        "cgpa_trend": f"{s['cgpa']:.2f} (was {s['previous_cgpa']:.2f})",
        "engagement_trend": f"{s['engagement']}% (was {s['previous_engagement']}%)",
        "att_diff": att_diff,
        "cgpa_diff": cgpa_diff,
        "eng_diff": eng_diff
    }

def get_processed_students():
    """Returns the full cohort of students enriched with computed risk indicators."""
    return [evaluate_student(s) for s in RAW_STUDENTS]

def get_cohort_stats(students=None):
    """Calculates summary counts for High, Medium, and Low risk categories."""
    if students is None:
        students = get_processed_students()
    return {
        "high": sum(1 for s in students if s["risk_level"] == "HIGH"),
        "medium": sum(1 for s in students if s["risk_level"] == "MEDIUM"),
        "low": sum(1 for s in students if s["risk_level"] == "LOW"),
        "total": len(students)
    }
