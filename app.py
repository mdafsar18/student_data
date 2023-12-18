from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import psycopg2

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Shah9606@localhost:5432/flask1_database'

db = SQLAlchemy(app)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    roll_no = db.Column(db.Integer, unique=True, nullable=False)
    class_no = db.Column(db.Integer, nullable=False)
    mob_no = db.Column(db.String(15), nullable=False)

with app.app_context():
    db.create_all()


@app.route('/students', methods=['GET'])
def get_students():
    with app.app_context():
        students = Student.query.all()
        student_list = [{'id': student.id, 'name': student.name, 'roll_no': student.roll_no,
                         'class_no': student.class_no, 'mob_no': student.mob_no} for student in students]
        return jsonify({'students': student_list})


@app.route('/students', methods=['POST'])
def create_student():
    #print("hello")
    data = request.get_json()
    #print(data)
    new_student = Student(name=data['name'], roll_no=data['roll_no'], class_no=data['class_no'], mob_no=data['mob_no'])
    #print(new_student)
    db.session.add(new_student)
    #print("hello1")
    db.session.commit()
    #print("hello2")
    return jsonify({'message': 'Student created successfully', 'student_id': new_student.id}), 201


@app.route('/students/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    student = Student.query.get(student_id)
    if student:
        data = request.get_json()
        student.name = data.get('name', student.name)
        student.roll_no = data.get('roll_no', student.roll_no)
        student.class_no = data.get('class_no', student.class_no)
        student.mob_no = data.get('mob_no', student.mob_no)
        db.session.commit()
        return jsonify({'message': 'Student updated successfully', 'student_id': student.id})
    else:
        return jsonify({'message': 'Student not found'}), 404


@app.route('/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    student = Student.query.get(student_id)
    if student:
        db.session.delete(student)
        db.session.commit()
        return jsonify({'message': 'Student deleted successfully'})
    else:
        return jsonify({'message': 'Student not found'}), 404


if __name__ == '__main__':
    app.run(debug=True)
