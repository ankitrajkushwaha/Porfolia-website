from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from email.message import EmailMessage
import smtplib

app = Flask(__name__)

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hire.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Model
class Hire(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Full_Name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    project_type = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)

# Create Database
with app.app_context():
    db.create_all()

# Routes
@app.route('/')
@app.route('/index')
def index():
    return render_template("index.htm")

@app.route('/project')
def project():
    return render_template("project.htm")

@app.route('/skill')
def skill():
    return render_template("skill.htm")

@app.route('/about')
def about():
    return render_template("about.htm")

@app.route('/contact', methods=['GET', 'POST'])
def contact():

    if request.method == 'POST':

        Full_Name = request.form['Full_Name']
        email = request.form['email']
        subject = request.form['subject']
        Project_type = request.form['Project_type']
        message = request.form['message']

        # Save to Database
        new_hire = Hire(
            Full_Name=Full_Name,
            email=email,
            subject=subject,
            project_type=Project_type,
            message=message
        )
        
        print(Full_Name,email,subject,Project_type,message)

        db.session.add(new_hire)
        db.session.commit()
        print("Data Saved Sucessfully")

        # Send Email
        msg = EmailMessage()
        msg['Subject'] = f'New Hire Message: {subject}'
        msg['From'] = 'ankitrajkushwaha456@gmail.com'
        msg['To'] = 'ankitrajkushwaha456@gmail.com'

        msg.set_content(f"""
Name: {Full_Name}
Email: {email}
Subject: {subject}
Project Type: {Project_type}

Message:
{message}
""")

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()

        server.login(
            'ankitrajkushwaha456@gmail.com',
            'tkyz zomf hrsm lfqn'
        )

        server.send_message(msg)
        server.quit()

        return render_template("sucess.htm")

    return render_template("contact.htm")

if __name__ == "__main__":
    app.run(debug=True, port=8000)