from db import db
from typing import List

class WageModel(db.Model):
    __tablename__ = "wages"

    id = db.Column(db.Integer, primary_key=True)
    occ_code = db.Column(db.String(7), nullable=False)
    job_title = db.Column(db.String(70), nullable=False)
    annual_mean_wage = db.Column(db.Integer, nullable=True)
    annual_wage_10_percent = db.Column(db.Integer, nullable=True)
    annual_wage_25_percent = db.Column(db.Integer, nullable=True)
    annual_wage_75_percent = db.Column(db.Integer, nullable=True)
    annual_wage_90_percent = db.Column(db.Integer, nullable=True)

    def __init__(self, occ_code, job_title, annual_mean_wage, annual_wage_10_percent, annual_wage_25_percent, annual_wage_75_percent, annual_wage_90_percent):
        self.occ_code = occ_code
        self.job_title = job_title
        self.annual_mean_wage = annual_mean_wage
        self.annual_wage_10_percent = annual_wage_10_percent
        self.annual_wage_25_percent = annual_wage_25_percent
        self.annual_wage_75_percent = annual_wage_75_percent
        self.annual_wage_90_percent = annual_wage_90_percent

    def __repr__(self):
        return 'WageModel(occ_code=%s, job_title=%s,annual_mean_wage,=%s, annual_wage_10_percent,=%s, annual_wage_25_percent,=%s, annual_wage_75_percent,=%s, annual_wage_90_percent,=%s)' % (self.occ_code, self.job_title, self.annual_mean_wage, self.annual_wage_10_percent, self.annual_wage_25_percent, self.annual_wage_75_percent, self.annual_wage_90_percent)

    def json(self):
        return {'occ_code': self.occ_code, 'job_title': self.job_title, 'annual_mean_wage': self.annual_mean_wage, 'annual_wage_10_percent': self.annual_wage_10_percent, 'annual_wage_25_percent': self.annual_wage_25_percent, 'annual_wage_75_percent': self.annual_wage_75_percent, 'annual_wage_90_percent': self.annual_wage_90_percent}

    @classmethod
    def find_by_name(cls, job_title) -> "WageModel":
        return cls.query.filter_by(job_title=job_title).first()

    @classmethod
    def find_by_id(cls, _id) -> "WageModel":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_all(cls) -> List["WageModel"]:
        return cls.query.all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
