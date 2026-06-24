-- TASK 1: INSERT, UPDATE AND DELETE DATA

INSERT INTO students (first_name, last_name, email, date_of_birth, department_id,
enrollment_year) values
	('Ragav', 'Vignes','ragav.vignes@college.edu','2004-05-12', 1, 2023),
	('Arun', 'Karthick','arun.karthick@college.edu','2003-07-18', 1, 2023) ;

SELECT COUNT(*) from students ;

UPDATE enrollments SET grade = 'B' WHERE course_id = 1 and student_id = 5 ;

SELECT * FROM enrollments WHERE course_id = 1 and student_id = 5 ;

DELETE FROM enrollments WHERE grade is NULL ;

SELECT COUNT(*) FROM enrollments where grade is NULL ;


-- TASK 2: SINGLE TABLE QUERIES AND FILTERING

SELECT * FROM students WHERE enrollment_year = '2022' ORDER BY last_name ASC ;

SELECT * FROM courses where credits > 3 ORDER BY credits DESC ;

SELECT * FROM professors WHERE salary BETWEEN 80000 AND 95000 ;

SELECT * FROM students WHERE email LIKE '%@college.edu' ;

SELECT enrollment_year , count(*) as total_students FROM students GROUP BY enrollment_year ORDER BY enrollment_year ;

-- TASK 3: MULTI-TABLE JOINS

SELECT s.first_name || ' ' || s.last_name AS full_name , dept_name from students s
    INNER JOIN departments d on s.department_id = d.department_id ;

SELECT e.enrollment_id , s.first_name || ' ' || s.last_name AS student_name, c.course_name, e.grade, e.enrollment_date from enrollments e
    INNER JOIN students s on s.student_id = e.student_id
    INNER JOIN courses c on c.course_id = e.course_id ;

SELECT * FROM students s
    LEFT JOIN enrollments e on s.student_id = e.student_id
    WHERE e.student_id is NULL;

SELECT c.course_id, c.course_name , COUNT(*) FROM courses c
    LEFT JOIN enrollments e ON c.course_id = e.course_id
    GROUP BY c.course_id ;

SELECT d.dept_name , p.prof_name, p.salary FROM departments d
    LEFT JOIN professors p on d.department_id = p.department_id ;

--TASK 4: AGGREGATIONS AND GROUPING

SELECT c.course_name, COUNT(e.student_id) as enrollment_count FROM courses c
    LEFT JOIN enrollments e on e.course_id = c.course_id
    GROUP BY c.course_name ;

SELECT d.dept_name , ROUND(AVG(p.salary) , 2) AS avg_salary FROM departments d
    JOIN professors p ON d.department_id = p.department_id
    GROUP BY d.dept_name;

SELECT * FROM departments WHERE budget > 600000 ;

SELECT e.grade , COUNT(*) AS count FROM enrollments e
    JOIN courses c ON e.course_id = c.course_id
    GROUP BY e.grade;

SELECT d.dept_name, COUNT(DISTINCT e.student_id) AS student_count FROM departments d
    JOIN courses c ON d.department_id = c.department_id
    JOIN enrollments e ON c.course_id = e.course_id
    GROUP BY d.department_id, d.dept_name
    HAVING COUNT(DISTINCT e.student_id) > 2;
