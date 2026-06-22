-- TASK 1: SUBQUERIES


-- SELECT e.student_id , s.first_name || ' ' || s.last_name AS student_name, COUNT(e.course_id) FROM enrollments e JOIN students s ON e.student_id = s.student_id GROUP BY e.student_id, s.first_name, s.last_name HAVING COUNT(course_id) > ( SELECT AVG(count) FROM ( SELECT student_id , COUNT(course_id) FROM enrollments GROUP BY student_id ) ) ORDER BY e.student_id;
SELECT e.student_id , s.first_name || ' ' || s.last_name AS student_name, COUNT(e.course_id) FROM enrollments e
    JOIN students s ON e.student_id = s.student_id
    GROUP BY e.student_id, s.first_name, s.last_name HAVING COUNT(course_id) > (
        SELECT AVG(count) FROM (
            SELECT student_id , COUNT(course_id) FROM enrollments GROUP BY student_id
            )
        )
    ORDER BY e.student_id;


SELECT c.course_id,
           c.course_name
    FROM courses c
    WHERE EXISTS
    (
        SELECT 1
        FROM enrollments e
        WHERE e.course_id = c.course_id
    )
    AND NOT EXISTS
    (
        SELECT 1
        FROM enrollments e
        WHERE e.course_id = c.course_id
          AND e.grade <> 'A'
    );


SELECT * FROM professors p WHERE p.salary = (
    SELECT MAX(p2.salary)
    FROM professors p2
    WHERE p2.department_id = p.department_id
);


SELECT avg.department_id,avg.avg_salary FROM
(
    SELECT department_id,
           AVG(salary) AS avg_salary
    FROM professors
    GROUP BY department_id
) AS avg
WHERE avg.avg_salary > 85000;

-- TASK 2: CREATING AND USING VIEWS

CREATE VIEW vw_student_enrollment_summary AS SELECT
s.student_id,
s.first_name || ' ' || s.last_name AS full_name,
d.dept_name,
    COUNT(e.course_id) AS total_courses,
    ROUND(
    AVG(
    CASE
    WHEN e.grade = 'A' THEN 4
    WHEN e.grade = 'B' THEN 3
    WHEN e.grade = 'C' THEN 2
    WHEN e.grade = 'D' THEN 1
    WHEN e.grade = 'F' THEN 0
    END
    ),
    2
    ) AS gpa
FROM students s
JOIN departments d
    ON s.department_id = d.department_id
LEFT JOIN enrollments e
    ON s.student_id = e.student_id
GROUP BY s.student_id, s.first_name, s.last_name, d.dept_name ;

CREATE VIEW vw_course_stats AS SELECT
c.course_name,
c.course_code,
    COUNT(e.enrollment_id) AS total_enrollments,
    ROUND(
    AVG(
    CASE
    WHEN e.grade = 'A' THEN 4
    WHEN e.grade = 'B' THEN 3
    WHEN e.grade = 'C' THEN 2
    WHEN e.grade = 'D' THEN 1
    WHEN e.grade = 'F' THEN 0
    END
    ),
    2
    ) AS avg_gpa
FROM courses c
LEFT JOIN enrollments e
    ON c.course_id = e.course_id
GROUP BY c.course_id, c.course_name, c.course_code;

SELECT * FROM vw_student_enrollment_summary WHERE gpa > 3.0;

UPDATE vw_student_enrollment_summary SET full_name = 'Test Student' WHERE student_id = 1;
-- generally not automatically updatable.


DROP VIEW IF EXISTS vw_course_stats;

DROP VIEW IF EXISTS vw_student_enrollment_summary;

CREATE VIEW vw_student_enrollment_summary AS
SELECT student_id, first_name, last_name, email, enrollment_year FROM students
WHERE enrollment_year >= 2023 WITH CHECK OPTION;


-- Task 3: PROCEDURES AND TRANSACTIONS

CREATE OR REPLACE FUNCTION fn_enroll_student(
p_student_id INT,
p_course_id INT,
p_enrollment_date DATE
)
RETURNS TEXT
LANGUAGE plpgsql
AS $$
BEGIN

IF EXISTS (
    SELECT 1
    FROM enrollments
    WHERE student_id = p_student_id
      AND course_id = p_course_id
) THEN
    RAISE EXCEPTION
    'Student % is already enrolled in course %',
    p_student_id,
    p_course_id;
END IF;

INSERT INTO enrollments(
    student_id,
    course_id,
    enrollment_date
)
VALUES(
    p_student_id,
    p_course_id,
    p_enrollment_date
);

RETURN 'Enrollment successful';

END;
$$;

CREATE TABLE department_transfer_log
(
log_id SERIAL PRIMARY KEY,
student_id INT,
old_department_id INT,
new_department_id INT,
transfer_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE OR REPLACE FUNCTION fn_transfer_student(
p_student_id INT,
p_new_department_id INT
)
RETURNS TEXT
LANGUAGE plpgsql
AS $$
DECLARE
v_old_department INT;
BEGIN

SELECT department_id
INTO v_old_department
FROM students
WHERE student_id = p_student_id;

UPDATE students
SET department_id = p_new_department_id
WHERE student_id = p_student_id;

INSERT INTO department_transfer_log(
    student_id,
    old_department_id,
    new_department_id
)
VALUES(
    p_student_id,
    v_old_department,
    p_new_department_id
);

RETURN 'Transfer successful';

EXCEPTION
WHEN OTHERS THEN
RAISE;
END;
$$;

BEGIN;

UPDATE students
SET department_id = 2
WHERE student_id = 1;

INSERT INTO department_transfer_log(
student_id,
old_department_id,
new_department_id
)
VALUES(
1,
2,
9999
);

COMMIT;


BEGIN;

INSERT INTO enrollments(
student_id,
course_id,
enrollment_date
)
VALUES(
1,
1,
CURRENT_DATE
);

SAVEPOINT first_enrollment;

INSERT INTO enrollments(
student_id,
course_id,
enrollment_date
)
VALUES(
9999,
2,
CURRENT_DATE
);

ROLLBACK TO SAVEPOINT first_enrollment;

COMMIT;
