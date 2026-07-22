**Task 1 – V‑Model Mapping**

**V‑Model Diagram** (ASCII art)

```
Requirements ──► System Design ──► Architecture Design ──► Module Design ──► Coding
      ▲                                                                    ▼
      │                                                                    │
Acceptance ◄── System ◄── Integration ◄── Unit Testing ◄───
Testing        Testing          Testing
```

**SDLC ↔ TDLC Phase – Test Artifact Produced**

| SDLC Phase (Left) | Corresponding TDLC Phase (Right) | Test Artifact Produced During Development |
|---|---|---|
| Requirements | Acceptance Testing | Acceptance Test Plan / High‑level Acceptance Test Cases |
| System Design | System Testing | System Test Specification (test scenarios, environment setup) |
| Architecture Design | Integration Testing | Integration Test Plan (interface contracts, data flow tests) |
| Module Design | Unit Testing | Unit Test Cases (per class/function) and test scripts |
| Coding (implementation) | Unit Testing (bottom vertex) | Automated unit test code (e.g., pytest) |

**Entry / Exit Criteria for TDLC Phases**

| Testing Phase | Entry Criteria | Exit Criteria |
|---|---|---|
| Unit Testing | Code module completed; unit test cases defined; test framework ready | All unit tests passed; coverage ≥ 80 %; no blocking defects |
| Integration Testing | All modules unit‑tested; build integrated; integration test plan approved; test environment configured | All integration test cases passed; critical defects resolved; integration test report signed |
| System Testing | Integrated system ready; system test plan approved; test data prepared; performance baseline established | All system test cases executed; defect count for critical/high ≤ threshold; performance criteria met; stakeholder sign‑off |
| Acceptance Testing | Acceptance test plan approved; environment mirrors production; all lower‑level testing completed; business stakeholders available | All acceptance test cases executed; no critical/high defects; business sign‑off obtained |

**Early QA Engagement Points in the Course Management API Project**

1. **Requirements Review** – QA participates in reviewing functional and non‑functional requirements, ensuring they are clear, testable, and include acceptance criteria.
2. **Architecture / API Design Review** – QA validates the API contract (endpoint definitions, request/response schemas) and checks for testability, security concerns, and proper error handling before implementation.

---

**Task 2 – Agile QA & Shift‑Left Testing**

**Waterfall Problems (Testing after Development)**
1. Defects are discovered late, raising fix cost and schedule impact.
2. Lack of early stakeholder feedback leads to rework when the built API does not meet business needs.
3. Integration failures surface only after full implementation, causing cascading delays and difficult debugging.

**QA Role in Agile Ceremonies**
1. **Sprint Planning** – Define acceptance criteria for backlog items, estimate testing effort, and refine user stories.
2. **Daily Stand‑up** – Report testing blockers, share test progress, and coordinate with developers on defect resolution.
3. **Sprint Review** – Demonstrate completed features, verify they meet acceptance criteria, and capture stakeholder feedback.
4. **Retrospective** – Discuss testing process effectiveness, identify improvement actions, and adjust QA practices for the next sprint.

**Shift‑Left Practices Applied to the Course Management API**
- **(a) Review requirements for testability** – QA checks each endpoint requirement for clarity, defines edge cases, and ensures acceptance criteria are measurable before any code is written.
- **(b) Write test cases before code (TDD/BDD)** – Create unit test scripts (e.g., `pytest`) and BDD scenarios (Gherkin) for `POST /api/courses/` prior to implementing the endpoint.
- **(c) Static code analysis** – Run linters (flake8), security scanners (bandit), and type checkers (mypy) on each commit to catch issues early.
- **(d) API contract testing before integration** – Validate the OpenAPI/Swagger specification against mock servers (e.g., using Prism) to ensure the contract is correct before the service is integrated with other components.

**Acceptance Criteria – User Story (Gherkin)**

```
Feature: Create Course
  As a college admin
  I want to create a new course
  So that students can enroll in it

  Scenario: Successful course creation
    Given the admin is authenticated
    And no existing course has code "CS301"
    When the admin sends a POST request to "/api/courses/" with body:
      """
      {
        "name": "Algorithms",
        "code": "CS301",
        "credits": 4
      }
      """
    Then the response status is 201
    And the response body contains the created course with an "id"
    And the course is persisted in the database

  Scenario: Duplicate course code
    Given the admin is authenticated
    And a course with code "CS101" already exists
    When the admin sends a POST request to "/api/courses/" with body:
      """
      {
        "name": "Intro to CS",
        "code": "CS101",
        "credits": 3
      }
      """
    Then the response status is 400
    And the response body contains error "Course code already exists"

  Scenario: Missing required fields
    Given the admin is authenticated
    When the admin sends a POST request to "/api/courses/" with body:
      """
      {
        "name": "Data Science",
        "credits": 3
      }
      """
    Then the response status is 400
    And the response body contains error "Missing required fields: code"
```

---
