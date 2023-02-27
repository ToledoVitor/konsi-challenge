from flask import Flask, jsonify

app = Flask(__name__)
app.debug = True


@app.route('/', methods=['GET'])
def get_data():
    return jsonify(message='Hello'), 200


if __name__ == '__main__':
    app.run()