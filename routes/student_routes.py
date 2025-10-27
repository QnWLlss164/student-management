from flask import Blueprint, render_template, request, redirect, url_for
from models.student_model import (
    get_all_students,
    get_student_by_id,
    create_student,
    update_student,
    delete_student
)
from core.grading_strategy import GradeContext, WeightedAverageStrategy, classify_grade
from core.report_decorator import BasicReport, GPAReportDecorator, WarningReportDecorator

student_bp = Blueprint("student_bp", __name__, url_prefix="/students")

@student_bp.route("/")
def list_students():
    students = get_all_students()

    # Chuẩn bị dữ liệu bao gồm điểm tổng kết
    ctx = GradeContext(WeightedAverageStrategy())
    enriched_students = []
    for s in students:
        final_score = ctx.get_final_grade(s.midterm, s.final)
        enriched_students.append({
            "db_id": s.id,
            "student_id": s.student_id,
            "name": s.name,
            "classroom": s.classroom,
            "midterm": s.midterm,
            "final": s.final,
            "final_score": final_score,
            "rank": classify_grade(final_score)
        })

    return render_template("student_list.html", students=enriched_students)

@student_bp.route("/new", methods=["GET", "POST"])
def new_student():
    if request.method == "POST":
        create_student(
            request.form["student_id"],
            request.form["name"],
            request.form["classroom"],
            float(request.form["midterm"]),
            float(request.form["final"])
        )
        return redirect(url_for("student_bp.list_students"))
    return render_template("student_form.html", student=None)

@student_bp.route("/edit/<int:db_id>", methods=["GET", "POST"])
def edit_student(db_id):
    s = get_student_by_id(db_id)
    if not s:
        return "Not found", 404

    if request.method == "POST":
        update_student(
            db_id,
            request.form["student_id"],
            request.form["name"],
            request.form["classroom"],
            float(request.form["midterm"]),
            float(request.form["final"])
        )
        return redirect(url_for("student_bp.list_students"))

    return render_template("student_form.html", student=s)

@student_bp.route("/delete/<int:db_id>", methods=["POST"])
def remove_student(db_id):
    delete_student(db_id)
    return redirect(url_for("student_bp.list_students"))

@student_bp.route("/report/<int:db_id>")
def student_report(db_id):
    s = get_student_by_id(db_id)
    if not s:
        return "Not found", 404

    # Decorator chồng lớp: Basic -> GPA -> Warning
    report_builder = WarningReportDecorator(
        GPAReportDecorator(
            BasicReport()
        )
    )
    report_data = report_builder.build_report(s)
    return render_template("student_report.html", report=report_data)
