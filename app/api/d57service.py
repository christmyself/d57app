from . import api
from flask import jsonify

@api.route('/d57service/',methods=['GET'])
def d57service():
    print('Test')
    return jsonify(name='christ')