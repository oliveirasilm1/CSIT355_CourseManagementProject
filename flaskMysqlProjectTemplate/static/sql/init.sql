drop table if exists Enrolled;
drop table if exists Students;
drop table if exists Courses;

CREATE TABLE Students(
  id int(10) NOT NULL AUTO_INCREMENT,
  username varchar(50) NOT NULL,
  password varchar(255) NOT NULL,
  email varchar(100) NOT NULL,
  admin bool,
  firstname varchar(50),
  lastname varchar(50),
  age int,
  gpa real,
  PRIMARY KEY(id));

CREATE TABLE Courses(
  cid varchar(4),
  cname varchar(50),
  credits int,
  description varchar(255),
  filledslots int,
  totalslots int,
  PRIMARY KEY(cid)
);

CREATE TABLE Enrolled(
  id int,
  cid varchar(4),
  grade real,
  PRIMARY KEY (id, cid),
  FOREIGN KEY (id) REFERENCES Students(id),
  FOREIGN KEY (cid) REFERENCES Courses(cid)
);

delete from Students;
INSERT INTO Students (id, username, password, email, admin, firstname, lastname, age, gpa) VALUES
  (1, 'jacobsa1', 'abc123', 'jacobsa1@north.edu', 0, 'Alice', 'Jacobs', 19, 3.1),
  (2, 'nealj1', 'def456', 'nealj1@north.edu', 0, 'Julian', 'Neal', 21, 3.2),
  (3, 'pateld1', 'ghi789', 'pateld1@north.edu', 1, 'Dev', 'Patel', 26, NULL),
  (4, 'perreiram1', 'jkl012', 'perreiram1@north.edu', 0, 'Melissa', 'Perreira', 22, 3.4),
  (5, 'jacobsa1', 'mno345', 'jacobsa1@north.edu', 0, 'Alice', 'Jacobs', 19, 3.1);

delete from Courses;
INSERT INTO Courses (cid, cname, credits, description, filledslots, totalslots) VALUES
  ('C001', 'Calculus', 4, '...', 1, 24),
  ('C002', 'Biology', 3, '...', 2, 25),
  ('C003', 'Linear Algebra', 3, '...', 3, 20),
  ('C004', 'Chemisty', 4, '...', 1, 30);

delete from Enrolled;
INSERT INTO Enrolled (id, cid, grade) VALUES
  (1, 'C001', 89.3),
  (5, 'C002', 78.8),
  (2, 'C003', 90.1),
  (2, 'C004', 81.6),
  (1, 'C002', 81.4),
  (5, 'C003', 83.2),
  (4, 'C003', 94.7);
