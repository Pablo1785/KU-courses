-- Initialize database
BEGIN;
CREATE TABLE IF NOT EXISTS course (
	course_id char(10) PRIMARY KEY,
	url text NOT NULL,
	title text NOT NULL,
	course_language text,
	description text NOT NULL,
	raw_description text NOT NULL,
	start_block block_enum,
	duration int,
	credits numeric(3, 1),
	study_level study_enum,

  pass_rate numeric(3, 1),
  avg_grade numeric(3, 1),
  median_grade numeric(3, 1)
);

CREATE INDEX IF NOT EXISTS desc_idx ON course USING GIN (raw_description gin_trgm_ops);

CREATE TABLE IF NOT EXISTS exam (
	course_id char(10) NOT NULL,
	exam_type exam_enum NOT NULL,
	minutes int
);
CREATE TABLE IF NOT EXISTS employee (
	email text PRIMARY KEY,
	full_name text NOT NULL
);
CREATE TABLE IF NOT EXISTS title (
	email text NOT NULL,
	title text NOT NULL -- Potentially enum in the future
);
CREATE TABLE IF NOT EXISTS coordinates (
	email text NOT NULL,
	course_id char(10) NOT NULL
);
CREATE TABLE IF NOT EXISTS workload (
	course_id char(10) NOT NULL,
	hours int,
	workload_type work_enum NOT NULL
);
CREATE TABLE IF NOT EXISTS schedule (
	course_id char(10) NOT NULL,
	schedule_type schedule_enum NOT NULL
);

CREATE TABLE IF NOT EXISTS department (
	course_id char(10) NOT NULL,
	department_type text NOT NULL
);

-- Add constraints
ALTER TABLE exam
ADD CONSTRAINT fk_course_id FOREIGN KEY (course_id) REFERENCES course (course_id);
ALTER TABLE title
ADD CONSTRAINT fk_email FOREIGN KEY (email) REFERENCES employee (email);
ALTER TABLE coordinates
ADD CONSTRAINT fk_email FOREIGN KEY (email) REFERENCES employee (email);
ALTER TABLE coordinates
ADD CONSTRAINT fk_course_id FOREIGN KEY (course_id) REFERENCES course (course_id);
ALTER TABLE workload
ADD CONSTRAINT fk_course_id FOREIGN KEY (course_id) REFERENCES course (course_id);
ALTER TABLE schedule
ADD CONSTRAINT fk_course_id FOREIGN KEY (course_id) REFERENCES course (course_id);
ALTER TABLE department
ADD CONSTRAINT fk_course_id FOREIGN KEY (course_id) REFERENCES course (course_id);

END;
