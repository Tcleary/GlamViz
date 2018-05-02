from flask import Flask
from flask_restplus import Api, Resource

from apis.harvest import api as harvest_ns
from apis.transform import api as transform_ns
import config

api = Api(
    title='GLAM',
    version='1.0',
    description='GLAM Data API'
)

api.add_namespace(harvest_ns)
api.add_namespace(transform_ns)

app = Flask(__name__)
api.init_app(app)


@api.route('/language')
class Lanquage(Resource):
    def get(self):
        return {'hey' : 'there'}


if __name__ == '__main__':
    app.run(debug=True)


