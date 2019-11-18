# -*- coding: utf-8 -*-
"""
Created on Sun Nov 17 13:55:02 2019

@author: Suprajah Suresh
"""

import unittest
from HW11_Suprajah_Suresh import Repository
import sqlite3

class Test_Repository(unittest.TestCase):
        
        def test_instructor_table_db(self):
            result = [('98762', 'Hawking, S', 'CS', 'CS 501', 1), ('98762', 'Hawking, S', 'CS', 'CS 546', 1), ('98764', 'Cohen, R', 'SFEN', 'CS 546', 1), ('98762', 'Hawking, S', 'CS', 'CS 570', 1), ('98763', 'Rowland, J', 'SFEN', 'SSW 555', 1), ('98763', 'Rowland, J', 'SFEN', 'SSW 810', 4)]
            instructor_rows = []
            db = sqlite3.connect("C:\\Users\\Suprajah Suresh\\Downloads\\sqlite-tools-win32-x86-3300100\\sqlite-tools-win32-x86-3300100\\810_homework.db")
            query = "select instructors.CWID,instructors.Name,instructors.Dept,grades.Course,count(grades.StudentCWID) as number_of_students from instructors inner join grades on instructors.CWID=grades.InstructorCWID group by Course,CWID;"
            for row in db.execute(query):
                instructor_rows.append(row)    
            db.close()
            self.assertEqual(instructor_rows,result)
            

if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)