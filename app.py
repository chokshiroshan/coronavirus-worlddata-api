from flask import Flask, jsonify
from flask_restful import Api, Resource
from fast import d

app = Flask(__name__)
api = Api(app)

class UserAPI(Resource):
    def get(self):
        return jsonify(d)

api.add_resource(UserAPI, '/')

if __name__ == '__main__':
    app.run()
