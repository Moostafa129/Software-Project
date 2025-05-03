import bcrypt
from models.database import db
from models.student import Student
from models.course import Course
from models.grade import Grade
from models.database import db
from flask import make_response
from models.user import User, Student
from flask import Flask, render_template, request, redirect

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db.init_app(app)

with app.app_context():
    db.create_all()
    if not User.query.filter_by(email='admin@example.com').first():
        hashed_password = bcrypt.hashpw('1234'.encode('utf-8'), bcrypt.gensalt())
        admin_user = Admin(
            name='admin',
            email='admin@example.com',
            password=hashed_password.decode('utf-8'),
            department='Administration',
            access_level=5
        )
        db.session.add(admin_user)
        db.session.commit()

@app.route('/login')
def login(): 
    email = request.form.get('email')
    password = request.form.get('password')
    user = User.query.filter_by(email=email).first()

    if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        if isinstance(user, Student):
            response = make_response(redirect('/students/{}'.format(user.id)))
            response.set_cookie('student_id', str(user.id))
            return response
        else:
            return redirect('/admin')
    else:
        return "Invalid email or password", 401
    return redirect('')

## todo; isAdmin() decorator.
@app.route('/admin')
def index():
    students = Student.query.all()
    course_enrollment_counts = db.session.query(
        Course.name, 
        db.func.count(user_course.c.user_id).label('student_count')
    ).join(
        user_course
    ).group_by(
        Course.name
    ).all() 

    courses = Course.query.all()
    ## should see student and course list
    ## should see form to add student 
    ## should see form to add course
    return render_template('admin.html', students=students,course_enrollment_counts=course_enrollment_counts,courses=courses)
    
@app.route('/add-student', methods=['POST'])
def add_student():
    name = request.form['name']
    email = request.form['email']
    password = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    course_ids = request.form.getlist('course_ids')

    new_student = Student(name=name, email=email, password=password)
    db.session.add(new_student)
    db.session.commit()

    for course_id in course_ids:
        course = Course.query.get(course_id)
        if course:
            new_student.courses.append(course)

    db.session.commit()
    return redirect('/admin')

@app.route('/add-course', methods=['POST'])
def add_student():
    new_course = Course(name=request.form['name'])
    db.session.add(new_course)
    db.session.commit()
    return redirect('/admin')

@app.route('/add-grade',methods=['POST'])
def add_grade():
    course_id = request.form['course_id']
    student_id = request.form['student_id']
    grade_value = request.form['grade']

    new_grade = Grade(
        course_id=course_id,
        student_id=student_id,
        grade=grade_value
    )

    db.session.add(new_grade)
    db.session.commit()
    return redirect('/admin')

@app.route('/students/<int:student_id>/profile')
def show_student_profile(student_id):
    grades = db.session.query(
        Course.name,
        Grade.grade
    ).join(
        Grade, Grade.course_id == Course.id
    ).filter(
        Grade.student_id == student_id
    ).all() # {course_name,grade}[]

    ## should see option to enroll student [dropdown and enrolled in]
    ## should see option to add a grade next to the course in the grade list
    ## should see a grade list
    return render_template('profile.html',grades=grades)


@app.route('/courses/search', methods=['GET'])
def course_search():
    search_query = request.args.get('q', '')
    courses = Course.query.filter(Course.name.ilike(f'%{search_query}%')).all()

    ## should see a list for search
    return render_template('course_search.html',courses=courses)

if __name__ == '__main__':
    app.run(debug=True)