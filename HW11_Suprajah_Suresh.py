# -*- coding: utf-8 -*-
"""
Created on Sat Nov  9 16:18:35 2019

@author: Suprajah Suresh
"""
import os
from collections import defaultdict
from prettytable import PrettyTable
from HW08_Suprajah_Suresh import file_reading_gen
import sqlite3

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
        self.instructor_table_db("C:\\Users\\Suprajah Suresh\\Downloads\\sqlite-tools-win32-x86-3300100\\sqlite-tools-win32-x86-3300100\\810_homework.db")
        self.print_majors_table()

    def read_student_data(self):
        ''' Reads student.txt file and initilizes the values '''
        file_path =  os.path.join(self.dir_path,'students.txt')
        try:
            student_entry = list(file_reading_gen(file_path, 3, sep = '\t', header = True))
        except FileNotFoundError:
            print("Student file not found!")
        except ValueError as error_msg:
            print(error_msg)
        for cwid, name, major in student_entry:
            self.student_data[cwid] = Student(cwid, name, major)
    
    def read_instructor_data(self):
        ''' Reads instructor.txt file and initilizes the values '''
        file_path =  os.path.join(self.dir_path,'instructors.txt')
        try:
            instructor_entry = list(file_reading_gen(file_path, 3, sep = '\t', header = True))
        except FileNotFoundError:
            print("Instructor file not found!")
        except ValueError as error_msg:
            print(error_msg)
        for cwid, name, dept  in instructor_entry:
            self.instructor_data[cwid] = Instructor(cwid, name, dept)

    def read_grades_data(self):
        ''' Reads grades.txt file and updates containers in student and instructor class '''
        file_path =  os.path.join(self.dir_path,'grades.txt')
        try:
            grade_entry = list(file_reading_gen(file_path, 4, sep='\t', header = True))
        except FileNotFoundError:
            print("Grades file not found!")
        except ValueError as error_msg:
            print(error_msg)
        for scwid, course, grade, icwid in grade_entry:
            if scwid in self.student_data.keys():
                self.student_data[scwid].add_course_grades(course, grade)
            else:
                print("Student present in grades file but not in students file")
            if icwid in self.instructor_data.keys():
                self.instructor_data[icwid].add_student_count(course)
            else:
                print("Instructor present in grades file but not in instructor file")
    
    def read_majors_data(self):
        '''Reads majors.txt and creates the appropriate table'''
        file_path =  os.path.join(self.dir_path,'majors.txt')
        try:
            majors_entry = list(file_reading_gen(file_path, 3, sep='\t', header = True))
        except FileNotFoundError:
            print("Majors file not found!")
        except ValueError as error_msg:
            print(error_msg)
        for dept, type_sub, course in majors_entry:
            if dept not in self.majors_data.keys():
                self.majors_data[dept] = Majors(dept)
            try:
                self.majors_data[dept].add_course_for_major(type_sub, course)
            except ValueError as e:
                print(e)
    
    def instructor_table_db(self,db_path):
        ''' Connects to database and executes given query'''
        db = sqlite3.connect(db_path) 
        instructor_table = PrettyTable()
        instructor_table.field_names = ['CWID', 'Name', 'Dept', 'Course', 'Students']
        query = "select instructors.CWID,instructors.Name,instructors.Dept,grades.Course,count(grades.StudentCWID) as number_of_students from instructors inner join grades on instructors.CWID=grades.InstructorCWID group by Course,CWID;"
        for row in db.execute(query):
            instructor_table.add_row(row)
        db.close()
        print("instructor pretty table")
        print(instructor_table)

    def print_student_table(self):
        ''' Prints the student data using pretty table'''
        student_table = PrettyTable()
        student_table.field_names = ['CWID', 'Name', 'Major', 'Completed Courses','Required Courses', 'Required Electives']
        for k, v in self.student_data.items():
            cwid, name, major, course_grades = v.return_student_row()
            if major not in self.majors_data.keys():
                print("Major not in majors.txt file!")
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
        if self.elective.intersection(set([key for key,value in course_grades.items() if self.check_passing_status(value)])):
            return {}
        else:
            return self.elective
    
    def check_passing_status(self, grade):
        ''' Checks if a student has passed'''
        accepted_grades = {'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C'}
        if grade in accepted_grades:
            return True
        else:
            return False


if __name__ == "__main__":
    stevens = Repository('C:\\Users\\Suprajah Suresh\\Downloads\\Projects\\.vscode\\')