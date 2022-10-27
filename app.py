from flask import Flask, Blueprint, jsonify
from flask_restx import Api
from ma import ma
from db import db

from resources.employment import Employment, EmploymentList, employment_ns, employments_ns
from resources.wage import Wage, WageList, wages_ns, wage_ns
from marshmallow import ValidationError

app = Flask(__name__)
bluePrint = Blueprint('api', __name__, url_prefix='/api')
api = Api(bluePrint, doc='/doc', title='Sample API for AdeptID')
app.register_blueprint(bluePrint)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True

api.add_namespace(wage_ns)
api.add_namespace(wages_ns)
api.add_namespace(employment_ns)
api.add_namespace(employments_ns)


@app.before_first_request
def create_tables():
    db.create_all()


@api.errorhandler(ValidationError)
def handle_validation_error(error):
    return jsonify(error.messages), 400


wage_ns.add_resource(Wage, '/<int:id>')
wages_ns.add_resource(WageList, "")
employment_ns.add_resource(Employment, '/<int:id>')
employments_ns.add_resource(EmploymentList, "")

if __name__ == '__main__':
    db.init_app(app)
    ma.init_app(app)
    app.run(port=5000, debug=True)
