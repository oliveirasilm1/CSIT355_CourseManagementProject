drop table if exists Enrolled;
drop table if exists Students;
drop table if exists Courses;

CREATE TABLE Students(
  id int(10) NOT NULL AUTO_INCREMENT,
  username varchar(50) NOT NULL,
  password varchar(255) NOT NULL,
  email varchar(100) NOT NULL,
  admin bool NOT NULL,
  name varchar(100) NOT NULL,
  age int,
  gpa real,
  totalcredits int,
  PRIMARY KEY(id));

CREATE TABLE Courses(
  cid varchar(10) NOT NULL,
  cname varchar(50) NOT NULL,
  credits int NOT NULL,
  description varchar(500),
  enrolled int NOT NULL,
  PRIMARY KEY(cid)
);

CREATE TABLE Enrolled(
  id int NOT NULL,
  cid varchar(10) NOT NULL,
  grade real,
  PRIMARY KEY (id, cid),
  FOREIGN KEY (id) REFERENCES Students(id),
  FOREIGN KEY (cid) REFERENCES Courses(cid)
);

delete from Students;
INSERT INTO Students (username, password, email, admin, name, age, gpa, totalcredits) VALUES
  ('default', 'default', 'default', 0, 'default', NULL, NULL, NULL),
  ('jacobsa1', 'abc123', 'jacobsa1@montclair.edu', 0, 'Alice Jacobs', 19, 3.1, 21),
  ('nealj4', 'def456', 'nealj1@montclair.edu', 0, 'Julian Neal', 21, 3.5, 3),
  ('pateld', 'ghi789', 'pateld@montclair.edu', 1, 'Dev Patel', 26, NULL, NULL),
  ('perreiram7', 'jkl012', 'perreiram1@montclair.edu', 0, 'Melissa Perreira', 22, 3.6, 15),
  ('leem2', 'mno345', 'leem1@montclair.edu', 0, 'Martin Lee', 20, 3.3, 108),
  ('silvam5', 'pqr890', 'silvam5@montclair.edu', 0, 'Mariana Silva', 24, 3.3, 93),
  ('haoliu', 'csit355password', 'haoliu@montclair.edu', 1, 'Hao Liu', NULL, NULL, NULL),
  ('smithj4', 'mormonfig1', 'smithj4@montclair.edu', 0, 'Joseph Smith', 35, 2.4, 48),
  ('jordano2', 'swishkp18', 'jordano2@montclair.edu', 0, 'Olivia Jordan', 22, 2.8, 64),
  ('harrism9', 'dorynemo45', 'harrism9@montclair.edu', 0, 'Miles Harris', 18, 2.7, 81),
  ('pattons3', 'dimension20', 'pattons3@montclair.edu', 0, 'Siobhan Patton', 19, 3.9, 7),
  ('heathr6', '10things90s', 'heathr6@montclair.edu', 0, 'Rhea Heath', 20, 2.8, 8);

delete from Courses;
INSERT INTO Courses (cid, cname, credits, description, enrolled) VALUES
  ('CSIT270', 'Discrete Mathematics', 3, 'The structures include sets, graphs, digraphs, trees,
    networks, lattices, matrices, semigroups and groups. Many practical
    business and scientific problems can be posed and solved by the use of
    these structures.', 0),
  ('CSIT230', 'Computer Systems', 3, 'This course aims to introduce
the fundamental aspects of computer systems from the hardware and
software point of view. Students will be exposed to the principles of
computer architecture and organization within the framework of digital
design and Assembly language', 0),
  ('CSIT355', 'Database Systems', 3, 'A comprehensive collection of database organizations and design
tools: file organizations and evaluations, database structures, schemata
and implementations. Database security, operations and management.', 0),
  ('CSIT379', 'Computer Science Theory', 3, 'Formal languages, theory, automata, Turing Machines. computability, the
Church-Turing thesis, decidability, time and space complexity, and NP-completeness', 0),
  ('CSIT213', 'Data Structures and Algorithms', 3, 'This course will
teach the creation and manipulation of in-memory data structures
including lists, queues, trees, stacks, heaps, hash tables, graphs, search
trees, etc.', 0),
  ('CSIT503','Data Structures', 4, 'A continuation of CSIT501. Design and analysis of data structures, pointers, linked
representations, linear lists, trees, storage systems and structures,
database design.', 0),
  ('CSIT357', 'Artificial Intelligence', 3, 'A general, comprehensive coverage of the main areas constituting the field
of artificial intelligence, introduction of computer vision, natural language processing (NLP), pattern recognition and neural networks.', 0),
  ('CSIT345', 'Operating Systems', 3, 'Process Management. Process synchronization and deadlock prevention.
Memory Management. Interrupts processing. I/O Control.', 0),
  ('CSIT340', 'Computer Networks', 3, 'An introduction to principles and practice of computer networking, with emphasis on the Internet.', 0),
  ('CSIT231', 'Systems Programming', 3, 'This course covers in detail the core principles and foundations of computer systems programming.', 0);

delete from Enrolled;
INSERT INTO Enrolled (id, cid, grade) VALUES
  (3, 'CSIT231', 89.3),
  (3, 'CSIT340', 78.8),
  (3, 'CSIT503', 90.1),
  (2, 'CSIT503', 81.6),
  (2, 'CSIT270', 81.4),
  (2, 'CSIT355', 83.2),
  (10, 'CSIT340', 94.7),
  (10, 'CSIT270', 89.3),
  (10, 'CSIT355', 78.8),
  (7, 'CSIT503', 90.1),
  (7, 'CSIT231', 81.6),
  (7, 'CSIT213', 81.4),
  (5, 'CSIT357', 83.2),
  (5, 'CSIT230', 94.7),
  (5, 'CSIT213', 89.3),
  (6, 'CSIT230', 78.8),
  (6, 'CSIT340', 90.1),
  (6, 'CSIT345', 81.6),
  (11, 'CSIT231', 81.4),
  (11, 'CSIT357', 83.2),
  (11, 'CSIT355', 94.7),
  (13, 'CSIT379', 89.3),
  (13, 'CSIT340', 78.8),
  (13, 'CSIT355', 90.1),
  (9, 'CSIT213', 81.6),
  (9, 'CSIT231', 81.4),
  (9, 'CSIT270', 83.2),
  (12, 'CSIT503', 94.7),
  (12, 'CSIT345', 89.3),
  (12, 'CSIT231', 78.8),
  (7, 'CSIT230', 90.1),
  (13, 'CSIT213', 81.6),
  (3, 'CSIT355', 81.4),
  (10, 'CSIT357', 83.2),
  (5, 'CSIT355', 94.7);

UPDATE Courses C
SET enrolled = (SELECT COUNT(*)
                FROM Enrolled E
                WHERE C.cid = E.cid and not (E.id = 0))
