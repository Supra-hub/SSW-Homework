
"""
Created on Sat Oct 26 22:57:46 2019

@author: Suprajah Suresh
"""
from datetime import datetime, timedelta
import os
from collections import defaultdict
from prettytable import PrettyTable

def date_arithmetic():
    ''' Code segment demonstrating expected return values. '''
    three_days_after_02272000 = datetime.strptime("Feb 27, 2000",'%b %d, %Y') + timedelta(days = 3)
    three_days_after_02272017 = datetime.strptime("Feb 27, 2017",'%b %d, %Y') + timedelta(days = 3)
    days_passed_01012017_10312017 = datetime.strptime("Oct 31, 2017",'%b %d, %Y') - datetime.strptime("Jan1, 2017",'%b%d, %Y') 
    return three_days_after_02272000, three_days_after_02272017, days_passed_01012017_10312017

def file_reading_gen(path, fields, sep = ',', header = False):
    ''' Generate a tuple containing various fields in each line of the file '''
    try:
        fp = open(path, 'r')
    except FileNotFoundError:
        raise FileNotFoundError("Can not read the file in the path")
    else:
        line_num = 0
        with fp:
            for line in fp:
                if header:
                    header = False
                    continue
                tuple_of_words = tuple(line.strip("\n").split(sep))
                line_num += 1
                if len(tuple_of_words) != fields:
                    error_msg = str(path) + " has " + str(len(tuple_of_words)) + " on line" + str(line_num) + " but expected " + str(fields)
                    raise ValueError(error_msg)
                yield tuple_of_words
    
class FileAnalyzer:
    """ Class contains the details about the python programs in a given directory"""
    def __init__(self, directory):
        """ Initialize the class and call analyze files function"""
        self.directory = directory
        self.files_summary = dict()
        self.analyze_files() 

    def analyze_files(self):
        """ Function updates the class with the required details about .py files"""
        os.chdir(self.directory)
        final_dict = defaultdict(dict)
        for filename in os.listdir(self.directory):
            if filename.endswith(".py"):
                file_dict = defaultdict(int)
                try:
                    fp = open(os.path.join(self.directory, filename))
                except:
                    raise FileNotFoundError(" Cant read the file")
                for line in fp:
                    if line.startswith('class'):
                        file_dict['class'] += 1
                    elif line.startswith('def'):
                        file_dict['function'] += 1
                    file_dict['line'] +=1
                    file_dict['char'] += len(line)
                final_dict[filename] = file_dict
        self.files_summary = final_dict

    def pretty_print(self):
        """Converts a dictionary of dictionaries into a table """
        x = PrettyTable()
        x.field_names = ["File name", "Classes", "Functions", "Lines","Characters"]
        for k,v in self.files_summary.items():
            x.add_row([k, v['class'], v['function'], v['line'], v['char']])
        return x