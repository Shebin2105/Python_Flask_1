from flask import Flask,render_template,request,flash,redirect,url_for
import re 
from datetime import datetime
import mysql.connector

app = Flask(__name__)
app.secret_key = 'super secret key'  
@app.route('/',methods=['GET', 'POST'])

def validation():
    if request.method=="POST":
        name=request.form.get('name')
        dob=request.form.get('dob')
        course=request.form.get('course')
        marks=request.form.get("HSC-MARKS")
        hostel=request.form.get('hostel')
        address=request.form.get('Address')
        contact=request.form.get('contact-no')
        email=request.form.get('email')
        field_errors={}
        global_errors=[]
        if not name or not re.match(r'^[A-Za-z\s]+$',name) or len(name)<3:
            field_errors['name']="Invalid Name"
        if not dob:
            field_errors['dob']="Date of birth is required"
        else:
            try:
                dob_time=datetime.strptime(dob,'%Y-%m-%d')
                today = datetime.today()
                if dob_time>today:
                    field_errors['dob']="Wrong Date of birth entered"
                age=(today-dob_time).days//365
                if age<18:
                    field_errors['dob']="Age should be greater than 18"
            except ValueError:
                field_errors['dob']="Invalid Date of birth format, should be YYYY-MM-DD"
        if not course:
            field_errors['course']="Course is required"
        if not marks or not marks.isdigit() or not (300<= int(marks)<=600):
            field_errors['marks']="Invalid HSC Marks, should be between 300 and 600"
        if not hostel:
            field_errors['hostel']="Hostel is required"
        if not address or not address.strip():
            field_errors['address']="Address is required"
        if not contact or not re.match(r'^\d{10}$',contact):
            field_errors['contact']="Invalid contact number,should be 10 digits"
        if not email or not re.match(r'^[a-zA-Z0-9_.]+@[a-zA-Z0-9]+\.[a-zA-z]{2,3}$',email):
            field_errors['email']="Invalid email format"
        if field_errors:
            return render_template('student.html',field_errors=field_errors,form_data=request.form)
        
        try:
            db=mysql.connector.connect(
            host="localhost",
            user="root",
            password="Shebin@21102005",
            database="flask"
            )
            cur=db.cursor()
            sql="Insert into Students(StudentName,DOB,Course,HSCMarks,HostelRequired,Address,ContactNumber,MailId) values(%s,%s,%s,%s,%s,%s,%s,%s)"
            values=(name,dob,course,marks,hostel,address,contact,email)
            cur.execute(sql,values)
            db.commit()
            cur.close()
            db.close()
            print("---- Form Submission ----")
            print(f"Name      : {name}")
            print(f"DOB       : {dob}")
            print(f"Course    : {course}")
            print(f"HSC Marks : {marks}")
            print(f"Hostel    : {hostel}")
            print(f"Address   : {address}")
            print(f"Contact   : {contact}")
            print(f"Email     : {email}")
            print("-------------------------")
            flash("Application submitted successfully","success")
            return redirect(url_for('validation'))
        except mysql.connector.Error as err:
            if err.errno == 1062:
                flash("Duplicate entry: this student already exists.", "error")
            else:
                flash(f"Database Error: {err}", "error")
            
    return render_template('student.html', form_data={}, field_errors={})

if __name__ == '__main__':
    app.run(debug=True)
