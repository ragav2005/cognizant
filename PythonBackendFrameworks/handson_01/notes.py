# ----------------------------------------------------------------
# 1. GET /api/courses/ request through Django
# ----------------------------------------------------------------

"""

Client (Browser/Postman)
        |
        |  HTTP GET /api/courses/
        V
+----------------------+
|      Web Server      |
| (Gunicorn/uWSGI etc.)|
+----------------------+
        |
        V
+----------------------+
|   WSGI / ASGI Server |
+----------------------+
        |
        V
+----------------------+
|      Middleware      |
| (Request Processing) |
+----------------------+
        |
        V
+----------------------+
|     URL Router       |
+----------------------+
        |
        V
+----------------------+
|       View           |
+----------------------+
        |
        V
+----------------------+
|       Model          |
+----------------------+
        |
        | Executes SQL query
        V
+----------------------+
|      Database        |
+----------------------+
        |
        | Query results
        V
+----------------------+
|       View           |
| Creates JSON/HTML    |
+----------------------+
        |
        V
+----------------------+
|      Middleware      |
| (Response Processing)|
+----------------------+
        |
        V
+----------------------+
| HTTP Response (200)  |
+----------------------+
        |
        V
Client (Browser/Postman)


"""

# ----------------------------------------------------------------
# 2. Middleware
# ----------------------------------------------------------------

"""
Middleware sits between the web server and Django views.

It processes every incoming request before it reaches the view,
and every outgoing response before it reaches the client.

Request Flow:

Client
   ↓
Middleware
   ↓
URL Router
   ↓
View
   ↓
Response
   ↓
Middleware
   ↓
Client

"""

# ----------------------------------------------------------------
# 3. WSGI vs ASGI
# ----------------------------------------------------------------

"""
WSGI = Web Server Gateway Interface

- Standard interface for synchronous Python web applications.
- Handles one request per worker.
- Suitable for traditional Django applications.
- Does not support WebSockets.

Examples:
- Gunicorn
- uWSGI


ASGI = Asynchronous Server Gateway Interface

- Successor to WSGI.
- Supports asynchronous programming.
- Can handle many simultaneous connections efficiently.
- Supports:
    * WebSockets
    * HTTP/2
    * Long-lived connections
    * Real-time chat
    * Live notifications

Examples:
- Daphne
- Uvicorn
- Hypercorn



"""

# ----------------------------------------------------------------
# 4. MVC vs Django's MVT
# ----------------------------------------------------------------

"""
MVC = Model View Controller

Model
    Handles data and database operations.

View
    Displays the user interface.

Controller
    Receives requests, processes business logic,
    and communicates with the model.


Django uses MVT (Model View Template)

Model
    - models.py
    - Represents database tables.
    - Handles database queries.

View
    - views.py
    - Contains business logic.
    - Receives requests.
    - Interacts with models.
    - Returns responses.

Template
    - HTML files
    - Displays data to the user.


MVC → Django MVT Mapping

MVC Component          Django Equivalent

Model           --->   Model

View            --->   Template

Controller      --->   View


"""
