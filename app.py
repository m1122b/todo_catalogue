
from flask import Flask, request, render_template, redirect, url_for, jsonify, abort, make_response
from forms import TodoForm
from models import todos


app = Flask(__name__)
app.config.update(
    SECRET_KEY = "nininini"
)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found', 'status_code': 404}), 404)


@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request', 'status_code': 400}), 400)


@app.route("/todos/", methods=["GET", "POST"])
def todos_list():
    form = TodoForm()
    error = ""
    if request.method == "POST":
        if form.validate_on_submit():
            print(form.data)
            todos.create(form.data)
        return redirect(url_for("todos_list"))
    return render_template("todos.html", form=form, todos=todos.all(), error=error)


@app.route("/todos/<int:todo_id>/", methods=["GET", "POST"])
def todo_details(todo_id):
    todo = todos.get(todo_id)[0]
    todo1 = ('id' , 'title' , 'author' , 'description' , 'done')
    todo_dict = dict(zip(todo1, todo))
    print(todo_dict)
    form = TodoForm(data=todo_dict)
    print(form.data)
    if request.method == "POST":
        if form.validate_on_submit():
            todos.update(todo_id, form.data)
        return redirect(url_for("todos_list"))
    return render_template("todo.html", form=form, todo_id=todo_id)


# !!!!!!!!!!!!!!!!!!!!! API !!!!!!!!!!!!!!!!!!!!!!!!!


@app.route("/api/v1/todos/", methods=["GET"])
def todos_list_api_v1():
    return jsonify(todos.all())


@app.route("/api/v1/todos/<int:todo_id>", methods=["GET"])
def get_todo(todo_id):
    todo = todos.get(todo_id - 1)
    if not todo:
        abort(404)
    return jsonify({"todo": todo})


@app.route("/api/v1/todos/", methods=["POST"])
def create_todo():
    if not request.json or not 'title' in request.json:
        abort(400)
    todo = {
        'title': request.json['title'],
        'author': request.json.get('author', ""),
        'description': request.json.get('description', ""),
        'done': False,
        'csrf_token': request.json.get('csrf_token', "")
    }
    todos.create(todo)
    return jsonify({'todo': todo}), 201


@app.route("/api/v1/todos/<int:todo_id>", methods=['DELETE'])
def delete_todo(todo_id):
    result = todos.delete(todo_id - 1)
    if not result:
        abort(404)
    return jsonify({'result': result})


@app.route("/api/v1/todos/<int:todo_id>", methods=["PUT"])
def update_todo(todo_id):
    todo = todos.get(todo_id - 1)
    if not todo:
        abort(404)
    if not request.json:
        abort(400)
    data = request.json
    if any([
        'title' in data and not isinstance(data.get('title'), str),
        'author' in data and not isinstance(data.get('author'), str),
        'description' in data and not isinstance(data.get('description'), str),
        'done' in data and not isinstance(data.get('done'), bool)
    ]):
        abort(400)
    todo = {
        'title': data.get('title', todo['title']),
        'author': data.get('author', todo['author']),
        'description': data.get('description', todo['description']),
        'done': data.get('done', todo['done'])
    }
    todos.update(todo_id, todo)
    return jsonify({'todo': todo})


if __name__ == "__main__":
    
    app.run(debug=True)



