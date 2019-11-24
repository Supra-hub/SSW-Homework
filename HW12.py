from flask import Flask, render_template
import sqlite3

app = Flask(__name__)


@app.route("/instructors")
def print_instructor_db():
    db_path = r"C:\Users\Suprajah Suresh\HW12\810_homework.db"
    try:
        db = sqlite3.connect(db_path)
    except sqlite3.OperationalError:
        print("Error establishing a connection!")
    else:
        query = """select instructors.CWID,instructors.Name,instructors.Dept,grades.Course,count(grades.StudentCWID) as number_of_students from instructors inner join grades on instructors.CWID=grades.InstructorCWID group by Course,CWID;"""
        table = db.execute(query)
        instructors = [{'cwid': cwid, 'name': name, 'dept': dept, 'course': course, 'student_cnt': student_cnt} for
                       cwid, name, dept, course, student_cnt in table]
        db.close()
        return render_template('instructors.html', title='Stevens Repository', table_header='Courses and students counts', table_res=instructors)


app.run(debug=True)
