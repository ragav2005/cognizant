**Task 1 – Automation Decision and Test Case Selection**

### 5 Automation‑Eligibility Criteria
| # | Criterion | How it applies to the POST /api/courses/ scenario |
|---|---|---|
| 1 | **Repetitiveness** – The test will be executed frequently (e.g., on every build or nightly regression). | The endpoint is exercised on every CI run to ensure new changes do not break course creation.
| 2 | **High Business Risk** – Failure would block a core business function (students cannot enroll). | A 500 or 400 response prevents enrolment, causing revenue loss and user frustration.
| 3 | **Deterministic Outcome** – Expected result is well‑defined (status 201 and correct JSON). | The API contract is stable; the expected payload can be asserted programmatically.
| 4 | **Data‑driven Capability** – The same test can run with many valid payload variations. | Different valid course payloads (name, code, credits) can be supplied from a data file, widening coverage without extra code.
| 5 | **Low Maintenance Cost** – The endpoint is unlikely to change frequently once stable. | The request/response schema is already stable; future changes would be limited to field additions, which are easy to extend in the data set.

### Manual vs Automate Decision for Listed Test Cases
| Test Case | Decision | Rationale |
|---|---|---|
| (a) Regression test for all CRUD endpoints after every code change | **Automate** | Regression is run on every commit; automation eliminates repetitive manual effort and provides fast feedback.
| (b) Exploratory testing of a new search feature | **Manual** | Exploratory testing relies on human intuition to discover unknown issues; automation cannot capture ad‑hoc insights.
| (c) Performance test: 100 concurrent users calling GET /api/courses/ | **Automate** (using a load‑testing tool) | Performance testing must be repeatable and measurable; automation with JMeter/Locust provides consistent load generation.
| (d) UI test for the login form | **Automate** (if login UI is stable) – **Manual** (if UI changes frequently). *Assume UI is stable*; automation gives quick regression coverage for login flow.
| (e) Verify the API documentation (Swagger) is accurate | **Automate** (schema validation) | Swagger can be validated automatically against the live contract; a script can compare specs to implementation.
| (f) Smoke test: verify the API is reachable after deployment | **Automate** | Smoke checks are simple, run on every deployment, and are ideal for automation to catch early failures.

### Test Automation ROI
- **Definition** – Test Automation ROI measures the cost‑benefit ratio of automating a test, comparing the time (or monetary) investment to the time saved over repeated executions.
- **Given:** Development of one automated regression test = **4 h**; manual execution = **0.5 h** per run.
- **Initial break‑even:** 4 h / (0.5 h saved per run) = **8 runs**.
- **Maintenance overhead:** After the 10th run, each automated execution incurs **20 %** extra effort (0.8 h) for maintenance on top of the 4 h initial cost.
- **Total automation cost for *n* runs:**
  - *n* ≤ 10 → 4 h (development) + 0 h maintenance.
  - *n* > 10 → 4 h + 0.8 h × (*n* − 10).
- **Break‑even equation for *n* > 10:**
  `0.5 n ≥ 4 + 0.8 (n − 10)` → `n ≤ 13.33`.
- **Interpretation:** The automation pays off after **8 runs** (ignoring maintenance). Even with the 20 % overhead after the 10th run, the ROI remains positive up to about **13 runs**. Beyond that the marginal cost outweighs the saved manual effort, so maintaining the test would need to be justified by other benefits (e.g., faster feedback, defect detection).

### Flaky Tests
- **Definition:** A flaky test is one that nondeterministically passes or fails without any code change, often due to timing, environment, or external dependencies.
- **Example:** An Selenium test that checks a success toast after form submission sometimes fails because the toast animation takes longer on a slow CI machine, causing the element‑lookup to time out.
- **Prevention / Fix Strategies:**
  1. **Stabilize Synchronisation** – Use explicit waits for UI elements instead of fixed sleeps.
  2. **Isolate External Dependencies** – Mock network calls or use a local test server to avoid variability from remote services.
  3. **Run in a Controlled Environment** – Execute tests in a container with fixed browser version, screen resolution, and resource limits.

---

**Task 2 – Automation Framework Types Comparison**

| Framework Type | Description (≈1 para) | Advantage | Disadvantage | When to Use for Course Management System |
|---|---|---|---|---|
| **Linear** | A single, sequential script executes all test steps from start to finish. No modularization or reuse; the script is written top‑to‑bottom. | Simple to create for a very small suite; low learning curve. | Poor maintainability; any change forces the whole script to be edited; hard to scale. | Quick proof‑of‑concept for a one‑off sanity check of the API (e.g., a single end‑to‑end script for demo). |
| **Modular** | Test logic is split into reusable modules or functions (e.g., login(), createCourse()). Test cases call these modules, promoting DRY principles. | High reusability; easier to update shared steps. | Requires disciplined design; test data is still hard‑coded unless combined with another pattern. | When many test cases share common operations like authentication, navigation, or CRUD utilities. |
| **Data‑Driven** | Test logic is separated from test data; a single test script iterates over rows in CSV/JSON/Excel files, feeding different inputs. | Enables massive coverage with minimal code; easy for non‑technical testers to add data. | Logic can become tangled if data files grow; still needs a base script for each test flow. | Validating the POST /api/courses/ endpoint with dozens of valid/invalid payloads without duplicating test code. |
| **Keyword‑Driven** | An abstraction layer maps readable keywords (e.g., *Login*, *CreateCourse*) to underlying code. Test cases are written as sequences of keywords, often in spreadsheets. | Enables non‑programmers to author tests; separates business language from implementation. | Additional maintenance of keyword libraries; can become opaque if keywords are too granular. | When business analysts need to contribute test scenarios for business rules (e.g., “EnrollStudent”, “PublishCourse”) without writing code. |
| **Hybrid** | Combines modular, data‑driven, and optionally keyword‑driven components. Test scripts are modular, data is externalized, and a keyword layer may sit on top for readability. | Offers the best of all worlds: reuse, scalability, and accessibility for diverse team members. | More initial setup effort; higher architectural complexity. | For the full Course Management UI suite: login reuse, many data‑driven API calls, and readable business‑level test cases for both developers and QA analysts. |

### Recommended Framework for the Login‑with‑50‑Credentials Scenario
**Hybrid (Modular + Data‑Driven + Keyword‑Driven)**
- **Why:**
  1. **Modular** – a `login` function/page‑object can be called from 20 different tests.
  2. **Data‑Driven** – the 50 username/password pairs live in a CSV/JSON file; the same login test iterates over them.
  3. **Keyword‑Driven** – expose a high‑level keyword like `LoginWithCredentials` that business users can invoke from a spreadsheet without code.
- This combination maximizes reusability, keeps the test data separate, and allows both technical (engineers) and non‑technical (QA analysts) contributors to write or extend tests.

### Hybrid Framework Folder Structure (Course Management Front‑end Tests)
```
automation/
├─ config/                     # global configuration files (e.g., env vars, browser caps)
│   └─ config.yaml
├─ data/                       # external test data sources
│   ├─ login_credentials.csv   # 50 user/password rows
│   └─ courses.json            # payloads for POST /api/courses/
├─ keywords/                   # optional keyword‑layer mappings
│   └─ login_keywords.py
├─ pages/                      # Page Object Model files
│   ├─ base_page.py
│   ├─ login_page.py
│   └─ dashboard_page.py
├─ utils/                      # helper utilities (waits, logger, API client)
│   ├─ logger.py
│   └─ api_client.py
├─ tests/                      # test case files (pytest or unittest style)
│   ├─ test_login.py          # uses data‑driven parametrisation
│   ├─ test_course_creation.py
│   └─ test_course_crud.py
└─ requirements.txt            # Python dependencies (selenium, pytest, pandas, etc.)
```
- **config/** – stores environment‑specific settings (base URL, headless mode).
- **data/** – CSV/JSON files that feed parametrised tests.
- **keywords/** – thin wrappers that map business‑language steps to page‑object calls.
- **pages/** – encapsulate UI interactions for each screen (login, dashboard, course form).
- **utils/** – common helpers such as a robust explicit‑wait wrapper, logging, and a thin API client for backend verification.
- **tests/** – individual test modules; each uses `@pytest.mark.parametrize` (or equivalent) to pull data from **data/**.

---
