from flask import Flask, abort, jsonify, make_response, request, url_for
from flask_httpauth import HTTPBasicAuth


auth = HTTPBasicAuth()
app = Flask(__name__)


app.config.update({
   "DEBUG": True
})

tasks = [
   {
       'id': 1,
       'title': u'Buy groceries',
       'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
       'done': False
   },
   {
       'id': 2,
       'title': u'Learn Python',
       'description': u'Need to find a good Python tutorial on the web',
       'done': False
   }
]
users= [
        {"name": "rahul",  "password": "raj"},
        {"name": "dhannu", "password": "barman"},
        {"name": "shivam", "password": "monga"}
]
@auth.get_password
def get_passwords(username):
    new = [user for user in users if username == user['name']]
    print user
    if len(new) == 0:
        abort(404)
    return new[0]['password']

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)

@app.route('/todo/api/v1.0/tasks', methods=['GET'])
@auth.login_required
def get_taskss():
    return jsonify({'tasks': tasks})

@app.route('/todo/api/v1.0/tasks/signup', methods=['POST'])
def add_task():
    if not request.json or not 'name' in request.json:
        abort(400)
    uss = {
        "name": "ram",
        "password": "naresh"
    }
    users.append(uss)
    return jsonify({'usee': uss}), 201

@app.route('/todo/api/v1.0/tasks/sign', methods=['POST'])
def adds():
    if not request.json or not 'name' in request.json:
        abort(400)
    uss = {
        "name": request.json["name"],
        "password": request.json["password"]
    }
    users.append(uss)
    return jsonify({'usee': uss}), 201




@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['GET'])
@auth.login_required
def get_task(task_id):
   task = [task for task in tasks if task['id'] == task_id]
   if len(task) == 0:
       abort(404)
   return jsonify({'task': task[0]})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/todo/api/v1.0/tasks', methods=['POST'])
def create_task():
    if not request.json or not 'title' in request.json:
        abort(400)
    task = {
        'id': tasks[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }
    tasks.append(task)
    return jsonify({'task': task}), 201

@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    if not request.json:
        abort(404)
    if 'title' in request.json and type(request.json['title']) != unicode:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not unicode:
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)
    task[0]['title'] = request.json.get('title', task[0]['title'])
    task[0]['description'] = request.json.get('description', task[0]['description'])
    task[0]['done'] = request.json.get('done', task[0]['done'])
    return jsonify({'task': task[0]})

@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods = ['DELETE'])
def delete_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    tasks.remove(task[0])
    return jsonify({'result': True})

def make_public_task(task):
    new_task = {}
    for field in task:
        if field == 'id':
            print "dfgh"
            new_task['uri'] = url_for('get_task', task_id=task['id'], _external=True)
        else:
            new_task[field] = task[field]
    return new_task

@app.route('/todo/api/v1.0/tasks', methods=['GET'])
@auth.login_required
def get_tasks():
    return jsonify({'tasks': [make_public_task(task) for task in tasks]})

if __name__ == '__main__':
   app.run()

