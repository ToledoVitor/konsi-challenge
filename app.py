from flask import Flask, jsonify, request

from crawler import CrawlerClient
from utils import valid_cpf


app = Flask(__name__)
app.debug = True


@app.route("/benefits/", methods=["POST"])
def get_detailed_benefits():
    cpf = request.form["cpf"]
    login_user = request.form["login_user"]
    login_password = request.form["login_password"]

    cpf_is_valid = valid_cpf(cpf)
    if not cpf_is_valid:
        return jsonify(error="The given cpf is not a valid cpf"), 400

    try:
        benefit = CrawlerClient(
            login_user=login_user,
            login_password=login_password,
        ).get_benefits(cpf=cpf)
        return jsonify(numero_beneficio=benefit), 200

    except Exception as error:
        return jsonify(error=error), 400


@app.route("/benefits/complete", methods=["POST"])
def get_complete_benefits():
    cpf = request.form["cpf"]
    login_user = request.form["login_user"]
    login_password = request.form["login_password"]

    cpf_is_valid = valid_cpf(cpf)
    if not cpf_is_valid:
        return jsonify(error="The given cpf is not a valid cpf"), 400

    try:
        data = CrawlerClient(
            login_user=login_user,
            login_password=login_password,
        ).get_benefits(cpf=cpf, complete=True)
        return jsonify(data=data), 200

    except Exception as error:
        return jsonify(error=error), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
