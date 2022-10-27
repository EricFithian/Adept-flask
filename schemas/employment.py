from ma import ma
from models.Employment import EmploymentModel


class EmploymentSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = EmploymentModel
        load_instance = True
        include_fk = True
