import os,json

from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

notifs = []

if not os.path.exists("notifications/"):
    os.makedirs("notifications")
else:
    for f in os.listdir("notifications"):
        notifs.append(json.loads(open(f"notifications/{f}").read())) # hell

class Notification(Resource):
    def get(self):
        return {'hello': 'world'}

api.add_resource(Notification, '/')

if __name__ == '__main__':
    app.run(debug=True)