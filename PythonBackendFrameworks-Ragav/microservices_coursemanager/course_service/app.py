from flask import Flask, jsonify, request
from sqlalchemy.exc import IntegrityError

from config import Config
from models import Course, db

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)


with app.app_context():
    db.create_all()

    if Course.query.count() == 0:
        db.session.add_all(
            [
                Course(name="Python Basics", code="CS101", credits=4),
                Course(name="Database Systems", code="CS102", credits=3),
            ]
        )
        db.session.commit()


@app.get("/api/courses/")
def list_courses():
    courses = Course.query.all()
    return jsonify([course.to_dict() for course in courses]), 200


@app.get("/api/courses/<int:course_id>")
def get_course(course_id):
    course = Course.query.get(course_id)
    if not course:
        return jsonify({"error": "Course not found"}), 404
    return jsonify(course.to_dict()), 200


@app.post("/api/courses/")
def create_course():
    data = request.get_json(silent=True) or {}

    required_fields = ["name", "code", "credits"]
    missing = [field for field in required_fields if field not in data]
    if missing:
        return jsonify({"error": f"Missing required fields: {', '.join(missing)}"}), 400

    course = Course(name=data["name"], code=data["code"], credits=data["credits"])
    db.session.add(course)

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Course code already exists"}), 400

    return jsonify(course.to_dict()), 201


@app.put("/api/courses/<int:course_id>")
def update_course(course_id):
    course = Course.query.get(course_id)
    if not course:
        return jsonify({"error": "Course not found"}), 404

    data = request.get_json(silent=True) or {}
    required_fields = ["name", "code", "credits"]
    missing = [field for field in required_fields if field not in data]
    if missing:
        return jsonify({"error": f"Missing required fields: {', '.join(missing)}"}), 400

    course.name = data["name"]
    course.code = data["code"]
    course.credits = data["credits"]

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Course code already exists"}), 400

    return jsonify(course.to_dict()), 200


@app.delete("/api/courses/<int:course_id>")
def delete_course(course_id):
    course = Course.query.get(course_id)
    if not course:
        return jsonify({"error": "Course not found"}), 404

    db.session.delete(course)
    db.session.commit()
    return jsonify({"message": "Course deleted successfully"}), 200


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001, debug=True)
