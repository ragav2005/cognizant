-- TASK 1 : BASELINE PERFORMANCES

EXPLAIN
SELECT s.first_name, s.last_name, c.course_name FROM enrollments e
JOIN students s
    ON s.student_id = e.student_id
JOIN courses c
    ON c.course_id = e.course_id
WHERE s.enrollment_year = 2022;

/*

    Sequential Scans Identified:
        Seq Scan on enrollments
        Seq Scan on students

    Index Usage:
        Index Scan using courses_pkey on courses

    Estimated Cost:
        Startup Cost = 12.16
        Total Cost = 42.16

    Observation:
    The query plan shows Sequential Scans on the enrollments and students tables, indicating that PostgreSQL reads all rows from these tables.
    */

-- TASK 2 : ADD INDEXES AND COMPARE

CREATE INDEX idx_students_enrollment_year ON students(enrollment_year);

ALTER TABLE enrollments ADD CONSTRAINT uq_enrollments_student_course UNIQUE (student_id, course_id);

CREATE INDEX idx_courses_course_code ON courses(course_code);

CREATE INDEX idx_enrollments_student_null_grade ON enrollments(student_id) WHERE grade IS NULL;

/*

After adding indexes, the query execution plan changed significantly.

Changes observed:
- students table:
    Seq Scan -> Index Scan using idx_students_enrollment_year

- enrollments table:
    Seq Scan may still appear if table is small,
    but join condition is more efficient due to indexed keys / primary keys.


Key Improvements:
- Reduced sequential scans on large tables
- Faster filtering on students.enrollment_year = 2022
- Join operations become more efficient due to indexed keys
- Composite UNIQUE index ensures no duplicate (student_id, course_id) entries

Overall Impact:
The query cost is expected to decrease, and at least one Seq Scan -> Index Scan
conversion is observed.
*/


-- TASK 3: N+1 PROBLEM

56:

import psycopg2
import time

conn = psycopg2.connect(
    dbname="college_db",
    user="postgres",
    password="your_password",
    host="localhost",
    port="5432"
)

cur = conn.cursor()
start_time = time.time()
cur.execute("SELECT student_id, course_id FROM enrollments")
enrollments = cur.fetchall()
query_count = 1
results = []

for student_id, course_id in enrollments:
    cur.execute("""
        SELECT s.first_name, s.last_name, c.course_name
        FROM students s
        JOIN courses c ON c.course_id = %s
        WHERE s.student_id = %s
    """, (course_id, student_id))

    results.append(cur.fetchone())
    query_count += 1

end_time = time.time()

print("Results:", results)
print("Total queries executed:", query_count)
print("Time taken:", end_time - start_time)

cur.close()
conn.close()



57:

import time
import psycopg2
conn = psycopg2.connect(
    dbname="college_db",
    user="postgres",
    password="p@ssw0rd",
    host="localhost",
    port="5432",
)
cur = conn.cursor()
start_time = time.time()
cur.execute("""
    SELECT
        s.first_name,
        s.last_name,
        c.course_name
    FROM enrollments e
    JOIN students s ON s.student_id = e.student_id
    JOIN courses c ON c.course_id = e.course_id;
""")

results = cur.fetchall()
end_time = time.time()

print("Results:", results)
print("Total queries executed: 1")
print("Time taken:", end_time - start_time)

cur.close()
conn.close()

-- Bad Approach (N+1):
-- - Queries executed: 11
-- - Time complexity increases with data size
-- - Heavy DB round-trips
-- - Slow due to repeated network calls

-- Good Approach (JOIN):
-- - Queries executed: 1
-- - All data fetched in single round-trip
-- - Much faster and scalable

/*
N+1 PROBLEM ANALYSIS:

In the N+1 approach:
- 1 query fetches all enrollments
- For each enrollment, an additional query is executed to fetch related student and course data
- Total queries = N + 1

For example:
If there are 10,000 enrollments:
- 1 query to fetch enrollments
- 10,000 additional queries for student/course lookup
- Total = 10,001 queries

This leads to:
- Massive database overhead
- Increased latency due to repeated round trips
- Poor scalability

FIX:
Using JOIN (or ORM eager loading like select_related / joinedload)
reduces this to:
- Only 1 query regardless of dataset size

*/
