from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///./database.sqlite3"
db = SQLAlchemy()
db.init_app(app)
app.app_context().push()


class student(db.Model):
    __tablename__ = 'student'
    student_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    roll_number = db.Column(db.String, unique=True, nullable=False)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String)
    subs = db.relationship("course", secondary="enrollments", cascade="all, delete")


class course(db.Model):
    __tablename__ = 'course'
    course_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    course_code = db.Column(db.String, unique=True, nullable=False)
    course_name = db.Column(db.String, nullable=False)
    course_description = db.Column(db.String)


class enrollments(db.Model):
    __tablename__ = 'enrollments'
    enrollment_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    estudent_id = db.Column(db.Integer, db.ForeignKey(
        "student.student_id"), primary_key=True, nullable=False)
    ecourse_id = db.Column(db.Integer, db.ForeignKey(
        "course.course_id"), primary_key=True, nullable=False)

@app.route('/api/course', methods=['GET', 'POST'])
def test():
    getcourse = course.query.all()
    return render_template('try.html', getcourse=getcourse)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "GET":
        getstudent = student.query.order_by(student.roll_number).all()
        if getstudent != []:
            return render_template('index.html', getstudent=getstudent)
        else:
            return "<h1>Student list</h1><p>No student found. Add the student now!</p><a href='/student/create'>+Add student</a>"

@app.route('/student/create', methods=['GET', 'POST'])
def create():
    if request.method == 'GET':
        return render_template('create.html')
    elif request.method == 'POST':
        roll = request.form['roll']
        f = request.form['f_name']
        l = request.form['l_name']
        ea = request.form.getlist('courses')
        print(ea)
        ok = student.query.filter_by(roll_number = request.form['roll']).first()
        print(ok)
        if not ok:
            add_student = student(roll_number = roll, first_name=f, last_name=l)
            db.session.add(add_student)
            db.session.commit()
            lad = student.query.filter_by(roll_number = roll).first()
            x = lad.student_id
            for n in ea:    
                add_enroll = enrollments(estudent_id=x, ecourse_id=n[7])
                db.session.add(add_enroll)
                db.session.commit()
            return redirect('/')
            
        else:
            return render_template('exist.html')

@app.route('/student/<studid>/update', methods = ['GET', 'POST'])
def update(studid):
    if request.method =='GET':
        y = student.query.filter_by(student_id=studid).first()
        #return render_template('try.html', y=y)
        #ok = y.student_id
        #rollno = y.roll_number
        return render_template('update.html', y=y)
    elif request.method == 'POST':
        #try:    
            roll = request.form['roll']
            f = request.form['f_name']
            l = request.form['l_name']
            ea = request.form.getlist('courses')
            student.query.filter(student.student_id==studid).update({'first_name':f,'last_name':l})
            enrollments.query.filter_by(estudent_id = studid).delete()
            for n in ea:    
                add_enroll = enrollments(estudent_id=studid, ecourse_id=n[7])
                db.session.add(add_enroll)
                db.session.commit()
            return redirect('/')
        #except:
            #db.session.rollback()
            #return ("error in updating")


@app.route('/student/<studid>/delete', methods = ['GET', 'POST'])
def delete(studid):
    y = student.query.filter_by(student_id=studid).first()
    ok = y.student_id
    student.query.filter_by(student_id=studid).delete()
    enrollments.query.filter_by(estudent_id = ok).delete()
    db.session.commit()
    return redirect('/')


@app.route('/student/<studid>', methods = ['GET', 'POST'])
def each_student(studid):
    socks = student.query.filter_by(student_id=studid).first()
    #lad = socks.student_id
    shirt = enrollments.query.filter_by(estudent_id=studid).all()
    tshirt = []
    jacket = []
    for n in shirt:
        tshirt.append(n.ecourse_id)
    for n in tshirt:
        jacket.append(course.query.filter_by(course_id=n).all())
    return render_template("detail.html", sock=socks, jacket=jacket, lad=tshirt)


if __name__ == "__main__":
    # run the flask app
    app.run(host='0.0.0.0', debug=True, port=5000)
