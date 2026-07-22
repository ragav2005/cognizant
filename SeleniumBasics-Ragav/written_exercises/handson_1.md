**Task 1 – Testing Types**

**Unit Test**
- **Test case:** Verify that the `Course.to_dict()` method returns a dictionary with keys `id`, `name`, `code`, and `credits` and that the values match the model instance.
- **Classification:** Functional – checks that the method produces the correct output.

**Integration Test**
- **Test case:** Send a valid `POST /api/courses/` request with JSON `{ "name": "Algorithms", "code": "CS201", "credits": 3 }`. After the request completes, query the SQLite `course.db` directly to confirm the record was inserted with the correct values.
- **Classification:** Functional – validates interaction between the Flask endpoint and the SQLAlchemy persistence layer.

**System Test**
- **Test case:** Execute an end‑to‑end flow: (a) `POST /api/courses/` to create a course, (b) `GET /api/courses/<id>` to retrieve it, and (c) `GET /api/courses/` to list all courses. Verify that the created course appears in the list and that the details match the payload.
- **Classification:** Functional – ensures the complete system (API gateway, Flask app, database) works together.

**4User Acceptance Test (UAT)**
- **Test case:** As a college administrator, log into the admin UI, fill out the "Add Course" form with valid data, submit, and confirm that the new course appears in the admin dashboard’s course catalogue.
- **Classification:** Functional – validates the system from the end user’s perspective.

**Non‑Functional Example**
- **Test case:** Load‑test `GET /api/courses/` with 100 concurrent requests and measure average response time. Expected: ≤ 200 ms per request and ≤ 5 % error rate.
- **Classification:** Non‑Functional – measures performance.

**Black‑Box vs White‑Box Testing**
- **Black‑Box:** Tester has no knowledge of internal implementation; tests are based solely on specifications and expected behavior. Typical for QA testers.
- **White‑Box:** Tester knows the code structure and can design tests that exercise specific paths, branches, or conditions. Typical for developers (unit tests, code‑coverage driven tests).

---

**Formal Test Cases for `POST /api/courses/`**

| Test Case ID | Description | Preconditions | Test Steps | Expected Result | Actual Result | Pass/Fail |
|---|---|---|---|---|---|---|
| TC‑POST‑01 | Create a new course with valid data | API running, empty `course.db` | 1. Send `POST /api/courses/` with JSON `{ "name": "Data Structures", "code": "CS202", "credits": 4 }`<br>2. Observe response | `201 Created` with JSON containing the created course (including generated `id`) |  |  |
| TC‑POST‑02 | Attempt to create a course with a missing required field | API running | 1. Send `POST /api/courses/` with JSON `{ "name": "Operating Systems", "credits": 3 }` (missing `code`)<br>2. Observe response | `400 Bad Request` with error message `Missing required fields: code` |  |  |
| TC‑POST‑03 | Attempt to create a duplicate course code | API running, a course with `code` = `CS101` already exists | 1. Send `POST /api/courses/` with JSON `{ "name": "Advanced Python", "code": "CS101", "credits": 5 }`<br>2. Observe response | `400 Bad Request` with error message `Course code already exists` |  |  |

---



**Task 2 – Defect Lifecycle**

```
New → Assigned → Open → Fixed → Retest → Verified → Closed
```
- **Rejected:** After the `Open` state a defect may be marked *Rejected* if it is invalid, duplicate, or not a defect.
- **Deferred:** A defect can be *Deferred* from `Open` (or `Assigned`) when the team decides to postpone fixing it to a later release.

**Severity / Priority Classification**

| Bug | Severity | Priority | Justification |
|---|---|---|---|
| (a) `POST /api/courses/` returns **500** for all requests | **Critical** – the core functionality of creating courses is unusable for all users. | **P1** – must be fixed immediately before any further development or release. |
| (b) Course names > 150 chars are silently truncated | **Medium** – data loss occurs but the API remains operational. | **P2** – fix soon, but not an emergency. |
| (c) Swagger typo in API description | **Low** – purely cosmetic, does not affect functionality. | **P4** – low priority, can be addressed in a routine maintenance release. |
| (d) Intermittent 401 on correct login | **High** – authentication failures break access for users. | **P1** – urgent because it is flaky and impacts trust in the system. |

**Defect Report – Bug (a)**

- **Defect ID:** DEF‑001
- **Title:** `POST /api/courses/` returns 500 Internal Server Error for all requests
- **Environment:** Development (Flask app on localhost `127.0.0.1:5001`), SQLite `course.db`
- **Build Version:** v1.0.0 (current code base)
- **Severity:** Critical
- **Priority:** P1
- **Steps to Reproduce:**
  1. Start the Course Service (`python app.py`).
  2. Send a `POST` request to `http://127.0.0.1:5001/api/courses/` with any valid JSON payload.
  3. Observe the HTTP response status `500` and stack trace in the server logs.
- **Expected Result:** `201 Created` with the newly created course JSON.
- **Actual Result:** `500 Internal Server Error` – request fails, no course is created.
- **Attachments:** Screenshot of the 500 error response (see `screenshot_500_error.png`).

---

**Severity vs. Priority**
- **Severity** measures the *impact* of a defect on the system (e.g., data loss, crash). **Priority** measures *how urgently* the defect should be fixed based on business needs, release schedules, or work‑flow constraints.
- *Example:* A typo in the CEO’s dashboard label (`"Revenu"` instead of `"Revenue"`) has **Low Severity** (no functional impact) but may be assigned **High Priority** (P1) because the executive presentation is tomorrow and the typo looks unprofessional.
