from ma import ma
from models.Wage import WageModel


class WageSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = WageModel
        load_instance = True
