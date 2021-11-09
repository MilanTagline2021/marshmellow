import re
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:postgres@localhost/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db=SQLAlchemy(app)


class Student(db.Model):
    id=db.Column(db.Integer(), primary_key=True)
    name=db.Column(db.String(), nullable=False)
    info=db.Column(db.Text(), nullable=False)

    def __repr__(self):
        return self.name

    @classmethod
    def get_all(cls):
        return cls.query.all()
    
    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class StudentSchema(Schema):
    id=fields.Integer()
    name=fields.String()
    info=fields.String()


@app.route('/student', methods=['GET'])
def get_all_student():
    student_list = Student.get_all()

    serializer=StudentSchema(many=True)
    data=serializer.dump(student_list)

    return jsonify(data)

@app.route('/student', methods=['POST'])
def create_student():
    data=request.get_json()

    student=Student(
        name=data.get('name'),
        info=data.get('info')
    )

    student.save()
    serializer=StudentSchema()
    data=serializer.dump(student)

    return jsonify(data),201


@app.route('/student/<int:id>', methods=['GET'])
def get_student_by_id(id):
    student=Student.get_by_id(id)

    serializer=StudentSchema()
    data=serializer.dump(student)
    return jsonify(data),200

@app.route('/student/<int:id>', methods=['PUT'])
def update_student(id):
    student=Student.get_by_id(id)

    data=request.get_json()

    student.name=data.get('name')
    student.info=data.get('info')

    db.session.commit()
    serializer=StudentSchema()

    request_data=serializer.dump(student)
    return jsonify(request_data),201

@app.route('/student/<int:id>', methods=['DELETE'])
def delete_student(id):
    Student.get_by_id(id).delete()

    return jsonify({"messege":"Deleted Successfully."}),204


if __name__ == "__main__":
    app.run(debug=True)