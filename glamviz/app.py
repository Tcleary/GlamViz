from flask import Flask
from flask_restplus import Api

from apis.admin import api as admin_ns
from apis.harvest import api as harvest_ns
from apis.transform import api as transform_ns

api = Api(
    title='glamviz',
    version='1.0',
    description='glamviz Data API'
)
api.add_namespace(admin_ns)
api.add_namespace(harvest_ns)
api.add_namespace(transform_ns)

app = Flask(__name__)
app.config.from_object(__name__)
api.init_app(app)

if __name__ == '__main__':
    app.run(debug=True)


