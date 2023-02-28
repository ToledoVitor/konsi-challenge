from flask import Flask, jsonify, request

from crawler import CrawlerClient
from utils import valid_cpf


app = Flask(__name__)
app.debug = True


@app.route('/benefits/<cpf>', methods=['GET'])
def get_detailed_benefits(cpf):
    cpf_is_valid, cpf = valid_cpf(cpf)

    if not cpf_is_valid:
        return jsonify(error="The given cpf is not a valid cpf"), 400

    try:
        benefits = CrawlerClient().get_benefits(cpf=cpf)
        return jsonify(benefits), 200
    except Exception as error:
        return jsonify(error=error), 400


@app.route('/benefits/<cpf>/simple', methods=['GET'])
def get_simple_benefits():
    cpf = request.args.get('cpf')
    cpf_is_valid, cpf = valid_cpf(cpf)

    if not cpf_is_valid:
        return jsonify(error="The given cpf is not a valid cpf"), 400
    
    try:
        benefits = CrawlerClient().get_benefits(cpf=cpf, simple=True)
        return jsonify(benefits), 200
    except Exception as error:
        return jsonify(error=error), 400


if __name__ == '__main__':
    app.run()
