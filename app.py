from flask import Flask, render_template, request, redirect
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client['placement_db']
companies = db['companies']
students = db['students']

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    role = request.form['role']
    if role == 'student':
        company_list = list(companies.find())
        return render_template('student.html', companies=company_list)
    else:
        student_list = list(students.find())
        return render_template('officer.html', students=student_list)

@app.route('/add_company', methods=['POST'])
def add_company():
    company = {
        "name": request.form['name'],
        "role": request.form['role'],
        "ctc": request.form['ctc'],
        "eligibility": request.form['eligibility']
    }
    companies.insert_one(company)
    return render_template('message.html', message="Company added successfully!")

@app.route('/apply', methods=['POST'])
def apply():
    student = {
        "name": request.form['name'],
        "email": request.form['email'],
        "phone": request.form['phone'],
        "pan": request.form['pan'],
        "company": request.form['company']
    }

    # Check eligibility
    company = companies.find_one({"name": student['company']})
    eligibility = company['eligibility'].lower()
    if eligibility in student['pan'].lower():  # simple check for demo
        students.insert_one(student)
        return render_template('message.html', message="You are registered!")
    else:
        return render_template('message.html', message="You are not eligible for that job.")

if __name__ == '__main__':
    app.run(debug=True)
