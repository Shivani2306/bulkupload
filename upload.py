from flask import Flask, request, render_template, redirect, url_for, flash, send_file
from flask_sqlalchemy import SQLAlchemy
import io
import os

app = Flask(__name__)

# Use a writable path for the SQLite database
if os.getenv("RENDER"):
    db_path = '/tmp/employees.db'  # Use Render's writable /tmp directory
else:
    basedir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(basedir, "employees.db")

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "secret_key"

db = SQLAlchemy(app)

# Employee model with BLOB for profile_image
class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    profile_image = db.Column(db.LargeBinary, nullable=False)  # Store image as binary data

@app.route('/')
def index():
    return render_template('upload_form.html')

@app.route('/upload', methods=['POST'])
def upload():
    files = request.files.getlist('profile_images')  # Get all uploaded files
    names = request.form.getlist('names')  # Get all names

    if not files or not names or len(files) != len(names):
        flash("Ensure all fields are filled and number of names matches the number of images!", "error")
        return redirect(url_for('index'))

    # Insert multiple employee records
    for name, file in zip(names, files):
        if file:
            # Read binary data from the file
            binary_data = file.read()
            # Add to database
            employee = Employee(name=name, profile_image=binary_data)
            db.session.add(employee)

    db.session.commit()
    flash("Employees added successfully!", "success")
    return redirect(url_for('view_employees'))

# Route to view employees
@app.route('/employees')
def view_employees():
    employees = Employee.query.all()
    return render_template('employees.html', employees=employees)

# Route to serve image from database
@app.route('/employee/image/<int:id>')
def employee_image(id):
    employee = Employee.query.get_or_404(id)
    return send_file(io.BytesIO(employee.profile_image), mimetype='image/jpeg')

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)










# from flask import Flask, request, render_template, redirect, url_for, flash, send_file
# from flask_sqlalchemy import SQLAlchemy
# import io
# import os

# app = Flask(__name__)

# # Get the absolute path of the current file
# basedir = os.path.abspath(os.path.dirname(__file__))
# # Set the database URI to use an absolute path
# app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "employees.db")}'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.secret_key = "secret_key"


# # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///employees.db'
# # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# # app.secret_key = "secret_key"

# db = SQLAlchemy(app)

# # Employee model with BLOB for profile_image
# class Employee(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     profile_image = db.Column(db.LargeBinary, nullable=False)  # Store image as binary data

# @app.route('/')
# def index():
#     return render_template('upload_form.html')

# @app.route('/upload', methods=['POST'])
# def upload():
#     files = request.files.getlist('profile_images')  # Get all uploaded files
#     names = request.form.getlist('names')  # Get all names

#     if not files or not names or len(files) != len(names):
#         flash("Ensure all fields are filled and number of names matches the number of images!", "error")
#         return redirect(url_for('index'))

#     # Insert multiple employee records
#     for name, file in zip(names, files):
#         if file:
#             # Read binary data from the file
#             binary_data = file.read()
#             # Add to database
#             employee = Employee(name=name, profile_image=binary_data)
#             db.session.add(employee)

#     db.session.commit()
#     flash("Employees added successfully!", "success")
#     return redirect(url_for('view_employees'))

# # Route to view employees
# @app.route('/employees')
# def view_employees():
#     employees = Employee.query.all()
#     return render_template('employees.html', employees=employees)

# # Route to serve image from database
# @app.route('/employee/image/<int:id>')
# def employee_image(id):
#     employee = Employee.query.get_or_404(id)
#     return send_file(io.BytesIO(employee.profile_image), mimetype='image/jpeg')

# if __name__ == "__main__":
#     with app.app_context():
#         db.create_all()
#     app.run(debug=True, port=9088)
