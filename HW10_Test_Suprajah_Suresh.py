import unittest
from HW10 import Repository

class Test_Repository(unittest.TestCase):
        def test_instructor_data(self):
            stevens = Repository('C:\\Users\\Suprajah Suresh\\Downloads\\Projects\\.vscode\\')
            instructor_rows=[]
            for instruc in stevens.instructor_data.values():
                cwid, name, dept, course_dict = instruc.return_instructor_row()
                if course_dict:
                    for course, count in course_dict.items():
                        instructor_rows.append([cwid, name, dept, course, count])
            self.assertEqual(instructor_rows,[['98765', 'Einstein, A', 'SFEN', 'SSW 567', 4], ['98765', 'Einstein, A', 'SFEN', 'SSW 540', 3], ['98764', 'Feynman, R', 'SFEN', 'SSW 564', 3], ['98764', 'Feynman, R', 'SFEN', 'SSW 687', 3], ['98764', 'Feynman, R', 'SFEN', 'CS 501', 1], ['98764', 'Feynman, R', 'SFEN', 'CS 545', 1], ['98763', 'Newton, I', 'SFEN', 'SSW 555', 1], ['98763', 'Newton, I', 'SFEN', 'SSW 689', 1], ['98760', 'Darwin, C', 'SYEN', 'SYS 800', 1], ['98760', 'Darwin, C', 'SYEN', 'SYS 750', 1], ['98760', 'Darwin, C', 'SYEN', 'SYS 611', 2], ['98760', 'Darwin, C', 'SYEN', 'SYS 645', 1]])

        def test_majors_data(self):
            result = [['SFEN', ['SSW 555', 'SSW 567', 'SSW 564'], ['CS 545', 'CS 513', 'CS 501']],['SYEN', ['SYS 612', 'SYS 671', 'SYS 800'], ['SSW 565', 'SSW 810', 'SSW 540']]]
            stevens = Repository('C:\\Users\\Suprajah Suresh\\Downloads\\Projects\\.vscode\\')
            majors_rows = []
            for row in stevens.majors_data.values():
                majors_rows.append(row.return_majors_row())
            self.assertEqual(majors_rows, result)

        def test_students_data(self):
            result = [['10103', 'Baldwin, C', 'SFEN', ['CS 501', 'SSW 564', 'SSW 567', 'SSW 687'], {'SSW 555'}, {'CS 545', 'CS 513'}], ['10115', 'Wyatt, X', 'SFEN', ['CS 545', 'SSW 564', 'SSW 567', 'SSW 687'], {'SSW 555'}, {'CS 513', 'CS 501'}], ['10172', 'Forbes, I', 'SFEN', ['SSW 555', 'SSW 567'], {'SSW 564'}, {'CS 545', 'CS 513', 'CS 501'}], ['10175', 'Erickson, D', 'SFEN', ['SSW 564', 'SSW 567', 'SSW 687'], {'SSW 555'}, {'CS 545', 'CS 513', 'CS 501'}], ['10183', 'Chapman, O', 'SFEN', ['SSW 689'], {'SSW 555', 'SSW 567', 'SSW 564'}, {'CS 545', 'CS 513', 'CS 501'}], ['11399', 'Cordova, I', 'SYEN', ['SSW 540'], {'SYS 612', 'SYS 671', 'SYS 800'}, {'SSW 565', 'SSW 810'}], ['11461', 'Wright, U', 'SYEN', ['SYS 611', 'SYS 750', 'SYS 800'], {'SYS 612', 'SYS 671'}, {'SSW 565', 'SSW 810', 'SSW 540'}], ['11658', 'Kelly, P', 'SYEN', ['SSW 540'], {'SYS 612', 'SYS 671', 'SYS 800'}, {'SSW 565', 'SSW 810', 'SSW 540'}], ['11714', 'Morton, A', 'SYEN', ['SYS 611', 'SYS 645'], {'SYS 612', 'SYS 671', 'SYS 800'}, {'SSW 565', 'SSW 810', 'SSW 540'}], ['11788', 'Fuller, E', 'SYEN', ['SSW 540'], {'SYS 612', 'SYS 671', 'SYS 800'}, {'SSW 565', 'SSW 810'}]]
            stevens = Repository('C:\\Users\\Suprajah Suresh\\Downloads\\Projects\\.vscode\\')
            students_rows = []
            for k,v in stevens.student_data.items():
                cwid, name, major, course_grades = v.return_student_row()
                required = stevens.majors_data[major].remaining_required(course_grades)
                elective = stevens.majors_data[major].remaining_electives(course_grades)
                students_rows.append([cwid, name, major, sorted(course_grades.keys()), required, elective])
            self.assertEqual(students_rows, result)


if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)