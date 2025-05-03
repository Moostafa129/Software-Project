import unittest
from repositories.studentsRepository import StudentsRepository

class TestStudentsRepository(unittest.TestCase):
    def setUp(self):
        self.repo = StudentsRepository()

    def test_add_student(self):
        name = "John Doe"
        student_id = 123
        course_ids = [101, 102, 103]

        student = self.repo.add(name, student_id, course_ids)
        self.assertEqual(student['name'], name)
        self.assertEqual(student['student_id'], student_id)
        self.assertEqual(student['course_ids'], course_ids)
        self.assertIn(student, self.repo.students)


    def test_multiple_students(self):
        student1 = self.repo.add("Alice", 1, [201, 202])
        student2 = self.repo.add("Bob", 2, [203])

        self.assertEqual(len(self.repo.students), 2)
        self.assertIn(student1, self.repo.students)
        self.assertIn(student2, self.repo.students)

if __name__ == "__main__":
    unittest.main()
