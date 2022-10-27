from flask import request
from flask_restx import Resource, fields, Namespace

from models.Wage import WageModel
from schemas.wage import WageSchema

WAGE_NOT_FOUND = "Wage not found."

# Optional but helpful for adding this for organizational purposes
wage_ns = Namespace('wage', description='Wage related operations')
wages_ns = Namespace('wages', description='Wages related operations')

wage_schema = WageSchema()
wage_list_schema = WageSchema(many=True)

#Model required by flask_restx for expect
wage = wages_ns.model('Wage', {
    'occ_code': fields.String('Code containing 2 numbers, a dash, and then 4 more numbers'),
    'job_title': fields.String('Lists the general occupation for category'),
    'annual_mean_wage': fields.Integer,
    'annual_wage_10_percent': fields.Integer,
    'annual_wage_25_percent': fields.Integer,
    'annual_wage_75_percent': fields.Integer,
    'annual_wage_90_percent': fields.Integer
})


class Wage(Resource):

    def get(self, id):
        wage_data = WageModel.find_by_id(id)
        if wage_data:
            return wage_schema.dump(wage_data)
        return {'message': WAGE_NOT_FOUND}, 404

    def delete(self,id):
        wage_data = WageModel.find_by_id(id)
        if wage_data:
            wage_data.delete_from_db()
            return {'message': "Wage Deleted successfully"}, 200
        return {'message': WAGE_NOT_FOUND}, 404

    @wage_ns.expect(wage)
    def put(self, id):
        wage_data = WageModel.find_by_id(id)
        wage_json = request.get_json();

        if wage_data:
            wage_data.occ_code = wage_json['occ_code']
            wage_data.job_title = wage_json['job_title']
            wage_data.annual_mean_wage = wage_json['annual_mean_wage']
            wage_data.annual_wage_10_percent = wage_json['annual_wage_10_percent']
            wage_data.annual_wage_25_percent = wage_json['annual_wage_25_percent']
            wage_data.annual_wage_75_percent = wage_json['annual_wage_75_percent']
            wage_data.annual_wage_90_percent = wage_json['annual_wage_90_percent']
        else:
            wage_data = wage_schema.load(wage_json)

        wage_data.save_to_db()
        return wage_schema.dump(wage_data), 200


class WageList(Resource):
    @wages_ns.doc('Get all the wages')
    def get(self):
        return wage_list_schema.dump(WageModel.find_all()), 200

    @wages_ns.expect(wage)
    @wages_ns.doc('Create a new wage')
    def post(self):
        wage_json = request.get_json()
        wage_data = wage_schema.load(wage_json)
        wage_data.save_to_db()

        return wage_schema.dump(wage_data), 201
