from flask import Flask, jsonify, request
from sqlalchemy.exc import IntegrityError
import requests

from config import Config
from models import Enrollment, Student, db

COURSE_SERVICE_URL = "http://localhost:5001"

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)


with app.app_context():
    db.create_all()


@app.get("/api/students/")
def list_students():
    students = Student.query.all()
    return jsonify([student.to_dict() for student in students]), 200


@app.get("/api/students/<int:student_id>")
def get_student(student_id):
    student = Student.query.get(student_id)
    if not student:
        return jsonify({"error": "Student not found"}), 404
    return jsonify(student.to_dict()), 200


@app.post("/api/students/")
def create_student():
    data = request.get_json(silent=True) or {}

    required_fields = ["name", "email"]
    missing = [field for field in required_fields if field not in data]
    if missing:
        return jsonify({"error": f"Missing required fields: {', '.join(missing)}"}), 400

    student = Student(name=data["name"], email=data["email"])
    db.session.add(student)

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Email already exists"}), 400

    return jsonify(student.to_dict()), 201


@app.put("/api/students/<int:student_id>")
def update_student(student_id):
    student = Student.query.get(student_id)
    if not student:
        return jsonify({"error": "Student not found"}), 404

    data = request.get_json(silent=True) or {}
    required_fields = ["name", "email"]
    missing = [field for field in required_fields if field not in data]
    if missing:
        return jsonify({"error": f"Missing required fields: {', '.join(missing)}"}), 400

    student.name = data["name"]
    student.email = data["email"]

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Email already exists"}), 400

    return jsonify(student.to_dict()), 200


@app.delete("/api/students/<int:student_id>")
def delete_student(student_id):
    student = Student.query.get(student_id)
    if not student:
        return jsonify({"error": "Student not found"}), 404

    # Delete dependent enrollments for this student to keep data clean.
    Enrollment.query.filter_by(student_id=student_id).delete()
    db.session.delete(student)
    db.session.commit()

    return jsonify({"message": "Student deleted successfully"}), 200


@app.post("/api/students/<int:student_id>/enroll")
def enroll_student(student_id):
    student = Student.query.get(student_id)
    if not student:
        return jsonify({"error": "Student not found"}), 404

    data = request.get_json(silent=True) or {}
    course_id = data.get("course_id")
    if course_id is None:
        return jsonify({"error": "course_id is required"}), 400

    try:
        course_response = requests.get(
            f"{COURSE_SERVICE_URL}/api/courses/{course_id}",
            timeout=5,
        )
    except requests.ConnectionError:
        return jsonify({"error": "Course Service unavailable"}), 503
    except requests.RequestException:
        return jsonify({"error": "Failed to validate course"}), 502

    if course_response.status_code == 404:
        return jsonify({"error": "Course not found"}), 404

    if course_response.status_code >= 500:
        return jsonify({"error": "Course Service error"}), 502

    existing = Enrollment.query.filter_by(student_id=student_id, course_id=course_id).first()
    if existing:
        return jsonify({"error": "Student already enrolled in this course"}), 400

    enrollment = Enrollment(student_id=student_id, course_id=course_id)
    db.session.add(enrollment)
    db.session.commit()

    return jsonify(enrollment.to_dict()), 201


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5002, debug=True)
