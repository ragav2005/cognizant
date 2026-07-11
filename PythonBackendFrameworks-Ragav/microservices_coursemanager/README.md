# Microservices Course Manager (Hands-On 10)

This project demonstrates a **simple microservices architecture** using Flask.

## Service decomposition

| Service Name | Responsibility | Endpoints | Database |
|---|---|---|---|
| Course Service | Owns courses and departments (for this exercise, course CRUD is implemented) | `/api/courses/`, `/api/courses/<id>` | `course.db` |
| Student Service | Owns students and enrollments; validates courses via Course Service HTTP call before enrollment | `/api/students/`, `/api/students/<id>`, `/api/students/<student_id>/enroll` | `student.db` |
| Auth Service (Concept only) | User registration, login, JWT validation | `/api/v1/auth/register`, `/api/v1/auth/login`, token verification endpoint | Own auth database (e.g., `auth.db`) |
| Notification Service (Concept only) | Sends email/SMS confirmations after events like enrollment | `/notifications/send` (internal/event-driven) | Own notification database/queue state |

## Why each service owns its own database

Each service owning its own database preserves **loose coupling** and **independent deployment**. If one service changes schema, other services are unaffected. Services communicate through APIs/events, not direct table access. This avoids hidden dependencies and supports scaling each service independently.

## Monolith vs Microservices

- **Monolith**: One deployable unit, shared codebase, often shared database.
  - Pros: simple to start, easier local debugging, fewer distributed-system concerns.
  - Cons: hard to scale parts independently, slower deployments over time, tight coupling.
- **Microservices**: Multiple small services, each with clear business ownership.
  - Pros: independent scaling/deployment, better team autonomy, fault isolation.
  - Cons: higher operational complexity (networking, observability, retries, tracing).

## Inter-service communication

### Synchronous communication (HTTP)

- Request/response between services in real time (used here with `requests`).
- **Pros**: simple mental model, immediate response, easy to implement.
- **Cons**: temporal coupling (both services must be up now), latency chaining, retry/time-out handling complexity.

### Asynchronous communication (Message Queue / Event Streaming)

- Producer emits messages/events; consumer processes later.
- **Pros**: decoupling, resilience, better burst handling, eventual delivery.
- **Cons**: eventual consistency, more moving parts, harder debugging/ordering concerns.

### When to use RabbitMQ

Use RabbitMQ for **task/work queues**, request-reply patterns, and complex routing (fanout, topic, dead-letter queues) where reliable brokered messaging is needed.

### When to use Kafka

Use Kafka for **high-throughput event streaming**, append-only logs, replayable events, analytics pipelines, and long-term event retention.

### Why synchronous HTTP creates tight coupling

With synchronous calls, the caller waits for the callee. If Course Service is down, Student Service enrollment cannot complete. This run-time dependency creates tight coupling in availability and latency.

## Project structure

```text
microservices_coursemanager/
│
├── README.md
│
├── course_service/
│   ├── app.py
│   ├── config.py
│   ├── models.py
│   ├── requirements.txt
│   ├── instance/
│   └── course.db
│
├── student_service/
│   ├── app.py
│   ├── config.py
│   ├── models.py
│   ├── requirements.txt
│   ├── instance/
│   └── student.db
│
└── gateway/
    ├── app.py
    └── requirements.txt
```

## Setup

Use Python 3.12 and install dependencies in each service folder.

### 1) Course Service

```bash
cd course_service
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

Runs on: `http://localhost:5001`

### 2) Student Service

```bash
cd student_service
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

Runs on: `http://localhost:5002`

### 3) API Gateway

```bash
cd gateway
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

Runs on: `http://localhost:5000`

## Expected flow (via gateway)

```text
POST http://localhost:5000/api/students/1/enroll
↓
Gateway
↓
Student Service
↓
Course Service (GET /api/courses/<course_id>)
↓
Course exists
↓
Enrollment created
```

If Course Service is down, enrollment returns:

- HTTP `503 Service Unavailable`
- Body: `{"error":"Course Service unavailable"}`
