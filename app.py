from flask import Flask, request, jsonify, make_response
from repos.mongo import MongoDispatchRepo
from models.dispatch import Dispatch

CONN_STR = "mongodb://localhost:27017"

app = Flask(__name__)
db = MongoDispatchRepo(CONN_STR)

@app.route('/bydate/<date>')
def by_date(date):
    """
    Return all dispatches from given date.
    """
    dispatches = [d.as_dict() for d in db.by_date(date.replace('-', '/'))]
    print(dispatches)
    response = make_response(jsonify(dispatches), 200,)
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response

@app.route('/add', methods=['POST', 'OPTIONS'])
def add():
    """
    Add a dispatch to the database.
    """
    if request.method == 'POST':
        body = request.json
        dispatch = Dispatch.from_dict(body)
        try:
            db.add(dispatch)
            print(f"Added to db: {dispatch}")
        except Exception as e:
            return make_response("Something went wrong when adding Dispatch to the database", 501)
        response = make_response("", 200)
        response.headers["Access-Control-Allow-Origin"] = "*"
        return response
    elif request.method == 'OPTIONS':
        response = make_response("", 200)
        response.headers['Access-Control-Allow-Headers'] = 'content-type'
        response.headers["Access-Control-Allow-Origin"] = "*"
        return response


@app.route('/delete', methods=['POST'])
def delete():
    body = request.json
    dispatch = Dispatch.from_dict(body)
    db.delete(dispatch)
    return make_response("", 200)

@app.route('/update', methods=['POST'])
def update():
    body = request.json
    dispatch = Dispatch.from_dict(body)
    db.update(dispatch)
    return make_response("", 200)
