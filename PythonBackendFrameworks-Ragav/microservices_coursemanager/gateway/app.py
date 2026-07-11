from flask import Flask, Response, jsonify, request
import requests

app = Flask(__name__)

COURSE_SERVICE_URL = "http://localhost:5001"
STUDENT_SERVICE_URL = "http://localhost:5002"

ALLOWED_METHODS = ["GET", "POST", "PUT", "DELETE"]


def _forward_headers(incoming_headers):
    excluded = {"host", "content-length"}
    return {k: v for k, v in incoming_headers.items() if k.lower() not in excluded}


def proxy_to_service(base_url: str, subpath: str = ""):
    target_url = f"{base_url}{request.path if subpath != '' else request.path}"

    try:
        downstream_response = requests.request(
            method=request.method,
            url=target_url,
            headers=_forward_headers(request.headers),
            params=request.args,
            data=request.get_data(),
            cookies=request.cookies,
            allow_redirects=False,
            timeout=10,
        )
    except requests.ConnectionError:
        return jsonify({"error": "Downstream service unavailable"}), 503

    excluded_headers = {"content-encoding", "transfer-encoding", "connection"}
    headers = [
        (name, value)
        for name, value in downstream_response.raw.headers.items()
        if name.lower() not in excluded_headers
    ]

    return Response(downstream_response.content, downstream_response.status_code, headers)


@app.route("/api/courses/", defaults={"path": ""}, methods=ALLOWED_METHODS)
@app.route("/api/courses/<path:path>", methods=ALLOWED_METHODS)
def proxy_courses(path):
    return proxy_to_service(COURSE_SERVICE_URL, path)


@app.route("/api/students/", defaults={"path": ""}, methods=ALLOWED_METHODS)
@app.route("/api/students/<path:path>", methods=ALLOWED_METHODS)
def proxy_students(path):
    return proxy_to_service(STUDENT_SERVICE_URL, path)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
