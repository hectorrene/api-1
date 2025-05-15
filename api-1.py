from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

escuela = {
    1: {'subject': 'Mathematics', 'teacher': 'Mr. Smith'},
    2: {'subject': 'Science', 'teacher': 'Ms. Johnson'},
    3: {'subject': 'History', 'teacher': 'Mr. Brown'},
    4: {'subject': 'English', 'teacher': 'Ms. Davis'},
    5: {'subject': 'Physical Education', 'teacher': 'Mr. Wilson'},
    6: {'subject': 'Art', 'teacher': 'Ms. Garcia'},
    7: {'subject': 'Music', 'teacher': 'Mr. Martinez'},
    8: {'subject': 'Computer Science', 'teacher': 'Ms. Rodriguez'},
    9: {'subject': 'Geography', 'teacher': 'Mr. Lee'},  
    10: {'subject': 'Biology', 'teacher': 'Ms. Taylor'},
}

class allSubjects(Resource):
    def get(self):
        return [info['subject'] for info in escuela.values()]

class allTeachers(Resource):
    def get(self):
        return [info['teacher'] for info in escuela.values()]
    
class AllClasses (Resource):
    def get(self):
        return escuela
    
class createClass (Resource):
    def post(self):
        new_class = request.get_json()
        new_id = max(escuela.keys()) + 1
        escuela[new_id] = new_class
        return {new_id: new_class}, 201
    
class deleteClass (Resource):
    def delete(self, class_id):
        if class_id in escuela:
            del escuela[class_id]
            return '', 204
        return {'message': 'Class not found'}, 404
    
class updateClass (Resource):
    def put(self, class_id):
        if class_id in escuela:
            updated_class = request.get_json()
            escuela[class_id] = updated_class
            return {class_id: updated_class}, 200
        return {'message': 'Class not found'}, 404
    
# Rutas
api.add_resource(AllClasses, '/')
api.add_resource(allSubjects, '/subjects')
api.add_resource(allTeachers, '/teachers')
api.add_resource(createClass, '/classes/create')
api.add_resource(deleteClass, '/classes/delete/<int:class_id>')
api.add_resource(updateClass, '/classes/update/<int:class_id>')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)