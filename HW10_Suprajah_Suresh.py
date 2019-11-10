# -*- coding: utf-8 -*-
"""
Created on Sat Nov  9 16:18:35 2019

@author: Suprajah Suresh
"""
import os
from collections import defaultdict
from prettytable import PrettyTable
from HW08_Suprajah_Suresh import file_reading_gen

class Repository:
    def __init__(self, dir_path):
        ''' Holds all of the data for a specific organization '''
        self.dir_path = dir_path
        self.student_data = {}
        self.instructor_data = {}
        self.majors_data = {}
        self.read_student_data()
        self.read_instructor_data()
        self.read_grades_data()
        self.read_majors_data()
        self.print_student_table()
        self.print_instructor_table()
        self.print_majors_table()

    def read_student_data(self):
        ''' Reads student.txt file and initilizes the values '''
        file_path =  os.path.join(self.dir_path,'students.txt')
        student_entry = list(file_reading_gen(file_path, 3, sep = ';', header = True))
        for entry in student_entry:
            self.student_data[entry[0]] = Student(entry[0], entry[1], entry[2])
    
    def read_instructor_data(self):
        ''' Reads instructor.txt file and initilizes the values '''
        file_path =  os.path.join(self.dir_path,'instructors.txt')
        instructor_entry = list(file_reading_gen(file_path, 3, sep='|', header = True))
        for entry in instructor_entry:
            self.instructor_data[entry[0]] = Instructor(entry[0], entry[1], entry[2])

    def read_grades_data(self):
        ''' Reads grades.txt file and updates containers in student and instructor class '''
        file_path =  os.path.join(self.dir_path,'grades.txt')
        grade_entry = list(file_reading_gen(file_path, 4, sep='|', header = True))
        for entry in grade_entry:
            scwid, course, grade, icwid = entry
            self.student_data[scwid].add_course_grades(course, grade)
            self.instructor_data[icwid].add_student_count(course)
    
    def read_majors_data(self):
        '''Reads majors.txt and creates the appropriate table'''
        file_path =  os.path.join(self.dir_path,'majors.txt')
        majors_entry = list(file_reading_gen(file_path, 3, sep='\t', header = True))
        for entry in majors_entry:
            if entry[0] not in self.majors_data.keys():
                self.majors_data[entry[0]] = Majors(entry[0])
            self.majors_data[entry[0]].add_course_for_major(entry[1], entry[2])

    def print_student_table(self):
        ''' Prints the student data using pretty table'''
        student_table = PrettyTable()
        student_table.field_names = ['CWID', 'Name', 'Major', 'Completed Courses','Required Courses', 'Required Electives']
        for k, v in self.student_data.items():
            cwid, name, major, course_grades = v.return_student_row()
            required = self.majors_data[major].remaining_required(course_grades)
            elective = self.majors_data[major].remaining_electives(course_grades)
            student_table.add_row([cwid, name, major, sorted(course_grades.keys()), required, elective])
        print(student_table)

    def print_instructor_table(self):
        ''' Prints the instructor data using pretty table'''
        instructor_table = PrettyTable()
        instructor_table.field_names = ['CWID', 'Name', 'Dept', 'Course', 'Students']
        for k, v in self.instructor_data.items():
            cwid, name, dept, course_dict = v.return_instructor_row()
            if course_dict:
                for course, count in course_dict.items():
                    instructor_table.add_row([cwid, name, dept, course, count])
        print(instructor_table)

    def print_majors_table(self):
        ''' Prints the majors data using pretty table'''
        majors_table = PrettyTable()
        majors_table.field_names = ['Dept', 'Required', 'Elective']
        for k,v in self.majors_data.items():
            majors_table.add_row(v.return_majors_row())
        print(majors_table)

      
class Student:
    ''' Stores information about a single student'''
    def __init__(self, cwid, name, major):
        self.cwid = cwid
        self.name = name
        self.major = major
        self.course_grades = defaultdict(str)

    def return_student_row(self):
        ''' Returns a row to the pretty table for students''' 
        return [self.cwid, self.name, self.major, self.course_grades]

    def add_course_grades(self, course, grade):
        ''' Add an entry to the course_grades container'''
        self.course_grades[course] = grade


class Instructor:
    ''' Stores information about a single professor'''
    def __init__(self, icwid, iname, dept):
        self.icwid = icwid
        self.iname = iname
        self.dept = dept
        self.course_student_count = defaultdict(int)

    def add_student_count(self, course):
        ''' Increment the student count by 1'''
        self.course_student_count[course] += 1 
    
    def return_instructor_row(self):
        ''' Returns a row to the pretty table for instructors'''
        return [self.icwid, self.iname, self.dept, self.course_student_count]


class Majors:
    '''Stores information about the majors and updates student table'''
    def __init__(self, major):
        self.major = major
        self.required = set()
        self.elective = set()

    def add_course_for_major(self, typec, course):
        '''Creates the required courses and elective courses set'''
        if typec == 'R':
            self.required.add(course)
        elif typec == 'E':
            self.elective.add(course)
        else:
            raise ValueError("Invalid Flag!!!")
    
    def return_majors_row(self):
        ''' Returns a row for the majors table'''
        return [self.major, list(self.required), list(self.elective)]
    
    def remaining_required(self, course_grades):
        ''' Computes the required courses remaining'''
        required_set = self.required - set([key for key,value in course_grades.items() if self.check_passing_status(value)])
        return required_set
    
    def remaining_electives(self, course_grades):
        ''' Computes the elective courses remaining'''
        return self.elective - set([key for key,value in course_grades.items() if self.check_passing_status(value)])
    
    def check_passing_status(self, grade):
        ''' Checks if a student has passed'''
        accepted_grades = {'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C'}
        if grade in accepted_grades:
            return True
        else:
            return False


if __name__ == "__main__":
    stevens = Repository('C:\\Users\\Suprajah Suresh\\Downloads\\Projects\\.vscode\\')