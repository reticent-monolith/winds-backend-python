from flask import Flask, request, jsonify, make_response
from repo import DispatchRepo, Dispatch

CONN_STR = "mongodb://localhost:27017"

app = Flask(__name__)
db = DispatchRepo(CONN_STR)

# TODO this raises IndexError when list returning from db is empty, handle this!
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

@app.route('/add', methods=['POST'])
def add():
    """
    Add a dispatch to the database.
    """
    body = request.json
    dispatch = Dispatch.from_dict(body)
    print(f"Added to db: {dispatch._id}")
    db.add(dispatch)
    return make_response('200')

@app.route('/delete', methods=['POST'])
def delete():
    body = request.json
    dispatch = Dispatch.from_dict(body)
    db.delete(dispatch)
    return make_response('200')

@app.route('/update', methods=['POST'])
def update():
    body = request.json
    dispatch = Dispatch.from_dict(body)
    db.update(dispatch)
    return make_response('200')
