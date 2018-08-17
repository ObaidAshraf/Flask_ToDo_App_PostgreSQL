from flask import Flask, request, url_for, render_template, jsonify, json, abort
import db_controls as dbc

app = Flask(__name__)

@app.route("/todo/api/v1.0/tasks", methods = ['GET'])
def index():
    data = {}
    tasks = dbc.get_all_tasks()
    if (tasks[0] == 0):
        data["tasks"] = "No task found"
    else:
        for task in tasks[1]:
            data[task[0]] = {
                "id": task[0],
                "title": task[1],
                "description": task[2],
                "done": bool(task[3])
            }
    return (jsonify(data))


@app.route("/todo/api/v1.0/tasks/<int:task_id>", methods = ['GET'])
def get_task(task_id):
    data = {}
    task = dbc.get_task(task_id)
    if (task[0] == 0):
        abort(500)
    else:

        data[task[0]] = {
            "id": task[1][0],
            "title": task[1][1],
            "description": task[1][2],
            "done": bool(task[1][3])
        }
    return (jsonify(data))

@app.route("/todo/api/v1.0/tasks", methods = ['POST'])
def add_tasks():
    max_id = dbc.get_max_id()
    id = max_id[0] + 1
    title = request.json["title"]
    if not title:
        abort(500)
    description = request.json.get('description', '')
    done = bool(request.json["done"])
    dbc.insert_task(id, str(title), str(description), done)
    return jsonify({
        "id": id,
        "title": title,
        "description": description,
        "done": done
    })

@app.route("/todo/api/v1.0/tasks/<int:task_id>", methods = ['PUT'])
def update_task(task_id):
    data = {}
    title = request.json.get("title", '')
    description = request.json.get('description','')
    done = bool(request.json.get("done", ''))
    res = dbc.update_task(task_id, title=title, description=description, done=done)
    if (res == 500):
        abort(500)
    return "Task updated succesfully"

@app.route("/todo/api/v1.0/tasks/<int:task_id>", methods = ['DELETE'])
def delete_task(task_id):
    data = {}
    dbc.delete_task(task_id)
    return ("Task with ID " + str(task_id) + " is successfully deleted.")

@app.errorhandler(404)
def not_found_error(e):
    return "URL doesn't exist", 404

@app.errorhandler(500)
def not_found_error(e):
    return "Task not found", 500

if __name__ == '__main__':
    app.run(debug = True, port = 8080)