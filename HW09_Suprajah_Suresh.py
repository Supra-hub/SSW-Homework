# -*- coding: utf-8 -*-
"""
Created on Sun Nov  3 17:50:00 2019

@author: Suprajah Suresh
"""
import os
from collections import defaultdict
from prettytable import PrettyTable
from HW08_Suprajah_Suresh import file_reading_gen

class Repository:
    def __init__(self, dir_path):
        '''Holds all of the data for a specific organization'''
        self.dir_path = dir_path
        self.student_data = {}
        self.instructor_data = {}
        self.read_student_data()
        self.read_instructor_data()
        self.read_grades_data()
        self.print_student_table()
        self.print_instructor_table()

    def read_student_data(self):
        ''' Reads student.txt file and initilizes the values'''
        file_path =  os.path.join(self.dir_path,'students.txt')
        student_entry = list(file_reading_gen(file_path, 3, sep = '\t'))
        for entry in student_entry:
            self.student_data[entry[0]] = Student(entry[0], entry[1], entry[2])
    
    def read_instructor_data(self):
        ''' Reads instructor.txt file and initilizes the values'''
        file_path =  os.path.join(self.dir_path,'instructors.txt')
        instructor_entry = list(file_reading_gen(file_path, 3, sep='\t'))
        for entry in instructor_entry:
            self.instructor_data[entry[0]] = Instructor(entry[0], entry[1], entry[2])

    def read_grades_data(self):
        ''' Reads grades.txt file and updates containers in student and instructor class'''
        file_path =  os.path.join(self.dir_path,'grades.txt')
        grade_entry = list(file_reading_gen(file_path, 4, sep='\t'))
        for entry in grade_entry:
            scwid, course, grade, icwid = entry
            self.student_data[scwid].add_course_grades(course, grade)
            self.instructor_data[icwid].add_student_count(course)
    
    def print_student_table(self):
        student_table = PrettyTable()
        student_table.field_names = ['CWID', 'Name', 'Major', 'Completed Courses']
        for k, v in self.student_data.items():
            student_table.add_row(v.return_student_row())
        print(student_table)

    def print_instructor_table(self):
        instructor_table = PrettyTable()
        instructor_table.field_names = ['CWID', 'Name', 'Dept', 'Course', 'Students']
        for k, v in self.instructor_data.items():
            cwid, name, dept, course_dict = v.return_instructor_row()
            if course_dict:
                for course, count in course_dict.items():
                    instructor_table.add_row([cwid, name, dept, course, count])
        print(instructor_table)
      

class Student:
    ''' Stores information about a single student'''
    def __init__(self, cwid, name, major):
        self.cwid = cwid
        self.name = name
        self.major = major
        self.course_grades = defaultdict(str)
    
    def return_student_row(self): 
        return [self.cwid, self.name, self.major, sorted(self.course_grades.keys())]

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
        return [self.icwid, self.iname, self.dept, self.course_student_count]

if __name__ == "__main__":
    stevens = Repository('C:\\Users\\Suprajah Suresh\\Downloads\\Projects\\.vscode\\')