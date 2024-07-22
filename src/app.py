"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

first_members = [
     {"first_name": "Jhon", "age": 33, "lucky_numbers": [7, 13, 22]},
     {"first_name": "Jane", "age": 35, "lucky_numbers": [10, 14, 33]},
     {"first_name": "Jimmy", "age": 5, "lucky_numbers": [1]}
]

for member in first_members:
     jackson_family.add_member(member)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

#endpoints
@app.route('/members', methods=['GET'])
def get_all_members():
    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    return jsonify(members), 200

@app.route('/member/<int:member_id>', methods=['GET'])
def get_member(member_id):
     member = jackson_family.get_member(member_id)
     if member:
          return jsonify(member), 200
     else:
          return jsonify({"message" : "Miembro no encontrado"}), 400

@app.route('/member', methods=['POST'])
def add_member():
        body = request.get_json()
        if not body:
            return jsonify({"message": "Invalido"}), 400
        jackson_family.add_member(body)
        return jsonify({"message": "Miembro añadido"}), 200

@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    member = jackson_family.get_member(member_id)
    if member:
      jackson_family.delete_member(member_id)
      return jsonify({"done": True }), 200
    else:
      return jsonify({"message" : "Miembro no encontrado"}), 404






# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
