from flask import request
from flask_restx import Resource, fields, Namespace

from models.Employment import EmploymentModel
from schemas.employment import EmploymentSchema

EMPLOYMENT_NOT_FOUND = "Employment info not found."
EMPLOYMENT_ALREADY_EXISTS = "Employment '{}' Already exists."

employment_ns = Namespace('employment', description='Employment related operations')
employments_ns = Namespace('employments', description='Employments related operations')

employment_schema = EmploymentSchema()
employment_list_schema = EmploymentSchema(many=True)

# Model required by flask_restx for expect
employment = employments_ns.model('Employment', {
    'msa_id': fields.String('MSA ID info for employment'),
    'metro_area': fields.String('Location info for employment'),
    'occ_code': fields.String('Corresponds to the job and location'),
    'job_group': fields.String('Specifies type of job'),
    'total_employment': fields.String('Employment info on size of each sector')
})


class Employment(Resource):
    def get(self, id):
        employment_data = EmploymentModel.find_by_id(id)
        if employment_data:
            return employment_schema.dump(employment_data)
        return {'message': EMPLOYMENT_NOT_FOUND}, 404

    @employment_ns.expect(employment)
    def put(self, id):
        employment_data = EmploymentModel.find_by_id(id)
        employment_json = request.get_json();

        if employment_data:
            employment_data.msa_id = employment_json['msa_id']
            employment_data.metro_area = employment_json['metro_area']
            employment_data.occ_code = employment_json['occ_code']
            employment_data.job_group = employment_json['job_group']
            employment_data.total_employment = employment_json['total_employment']
        else:
            employment_data = employment_schema.load(employment_json)

        employment_data.save_to_db()
        return employment_schema.dump(employment_data), 200

    def delete(self, id):
        employment_data = EmploymentModel.find_by_id(id)
        if employment_data:
            employment_data.delete_from_db()
            return {'message': "Employment Info Deleted successfully"}, 200
        return {'message': EMPLOYMENT_NOT_FOUND}, 404


class EmploymentList(Resource):
    @employments_ns.doc('Get all the Employment info')
    def get(self):
        return employment_list_schema.dump(EmploymentModel.find_all()), 200

    @employments_ns.expect(employment)
    @employments_ns.doc('Create more employment info')
    def post(self):
        employment_json = request.get_json()
        job_group = employment_json['job_group']
        if EmploymentModel.find_by_name(job_group):
            return {'message': EMPLOYMENT_ALREADY_EXISTS.format(job_group)}, 400

        employment_data = employment_schema.load(employment_json)
        employment_data.save_to_db()

        return employment_schema.dump(employment_data), 201
