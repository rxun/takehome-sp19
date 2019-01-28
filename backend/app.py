from typing import Tuple

from flask import Flask, jsonify, request, Response
import mockdb.mockdb_interface as db

app = Flask(__name__)


def create_response(
    data: dict = None, status: int = 200, message: str = ""
) -> Tuple[Response, int]:
    """Wraps response in a consistent format throughout the API.

    Format inspired by https://medium.com/@shazow/how-i-design-json-api-responses-71900f00f2db
    Modifications included:
    - make success a boolean since there's only 2 values
    - make message a single string since we will only use one message per response
    IMPORTANT: data must be a dictionary where:
    - the key is the name of the type of data
    - the value is the data itself
    :param data <str> optional data
    :param status <int> optional status code, defaults to 200
    :param message <str> optional message
    :returns tuple of Flask Response and int, which is what flask expects for a response
    """
    if type(data) is not dict and data is not None:
        raise TypeError("Data should be a dictionary 😞")

    response = {
        "code": status,
        "success": 200 <= status < 300,
        "message": message,
        "result": data,
    }
    return jsonify(response), status


"""
~~~~~~~~~~~~ API ~~~~~~~~~~~~
"""


@app.route("/")
def hello_world():
    return create_response({"content": "hello world!"})


@app.route("/mirror/<name>")
def mirror(name):
    data = {"name": name}
    return create_response(data)

@app.route("/shows", methods=['GET'])
def get_all_shows():
    team = request.args.get("team")
    if not team:
        data = {"users": db.get("users")}
        return create_response(data)

    shows = db.get("shows")
    team_shows = [u for u in shows if u["team"] == team]
    data = {"shows": team_shows}

    return create_response(data)

@app.route("/shows", methods=['POST'])
def post_show():
    id = request.args.get("id")
    name = request.args.get("name")
    episodes_seen = request.args.get("episodes_seen")

    if id is None or name is None or episodes_seen is None:
        return create_response(None, 422, "You are missing necessary parameters")
    else:
        payload = {
            "id": id,
            "name": name,
            "episodes_seen": episodes_seen
        }

        newShow = db.create("shows", payload)
        return create_response(newShow, 201)

@app.route("/shows/<id>", methods=['DELETE'])
def delete_show(id):
    if db.getById('shows', int(id)) is None:
        return create_response(status=404, message="No show with this id exists")
    db.deleteById('shows', int(id))
    return create_response(message="Show deleted")

@app.route("/shows/<id>", methods=['GET'])
def get_show(id):
    if db.getById('shows', int(id)) is None:
        return create_response(status=404, message="No show with this id exists")
    return create_response({"show": db.getById('shows', int(id))})

@app.route("/shows/<id>", methods=['PUT'])
def put_show(id):
    id = request.args.get("id")
    if db.getById('shows', int(id)) is None:
        return create_response(status=404, message="No show with this id exists")

    name = request.args.get("name")
    episodes_seen = request.args.get("episodes_seen")
    update_values = {
        "name": name,
        "episodes_seen": episodes_seen
    }

    newShow = db.update_values('shows', int(id), update_values)
    return create_response(newShow)


# TODO: Implement the rest of the API here!

"""
~~~~~~~~~~~~ END API ~~~~~~~~~~~~
"""
if __name__ == "__main__":
    app.run(port=8080, debug=True)
