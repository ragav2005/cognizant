-- TASK 2: NORMALISATION VERIFICATION ANALYSIS

-- 1NF :
-- Definition: A table is in 1NF if all data values are atomic and there are no repeating groups.
-- Verification: In schema, tables like 'students' and 'departments' store single, discrete values per field
-- (e.g., first_name, email, budget).
-- Hypothetical Violation: If we stored multiple phone numbers in a single 'phone_number' field as a
-- comma-separated string (e.g., '9876543210, 9123456789'), it would violate 1NF. To fix such a violation
-- while maintaining 1NF, we would have to break those numbers out into a separate 'student_phones' table
-- with a foreign key referencing 'student_id'.

-- 2NF:
-- Definition: A table is in 2NF if it satisfies 1NF and all non-key columns are fully functionally dependent
-- on the entire primary key, meaning there are no partial dependencies on a composite primary key.
-- Verification: In the 'enrollments' table, the primary key is 'enrollment_id'. However, the
-- business logic dictates a composite candidate key composed of (student_id + course_id). The non-key
-- columns are 'enrollment_date' and 'grade'.

-- 3NF:
-- Definition: A table is in 3NF if it satisfies 2NF and contains no transitive dependencies, meaning non-key
-- columns must depend solely on the primary key, and not on other non-key columns.
-- Verification: In the 'enrollments' table, 'enrollment_date' and 'grade' depend directly on the primary key,
-- with no intermediate relationships.
-- Transitive Dependency Analysis: Storing 'dept_name' directly inside the 'students' table would strictly violate 3NF.


-- TASK 3: ALTER AND EXTEND THE SCHEMA


ALTER TABLE students
ADD COLUMN phone_number VARCHAR(15);

ALTER TABLE courses
ADD COLUMN max_seats INT DEFAULT 60;

ALTER TABLE departments
RENAME COLUMN hod_name TO head_of_dept;

ALTER TABLE students
DROP COLUMN phone_number;


SELECT column_name, data_type, column_default
FROM information_schema.columns WHERE table_name = 'courses';

SELECT column_name, data_type
FROM information_schema.columns WHERE table_name = 'departments';

SELECT constraint_name, constraint_type
FROM information_schema.table_constraints WHERE table_name = 'enrollments';
