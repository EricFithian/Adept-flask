from db import db
from typing import List

class EmploymentModel(db.Model):
    __tablename__ = "employments"

    id = db.Column(db.Integer, primary_key=True)
    msa_id = db.Column(db.Integer, nullable=False)
    metro_area = db.Column(db.String(250), nullable=False)
    occ_code = db.Column(db.String(7), nullable=False)
    job_group = db.Column(db.String(130), nullable=False)
    total_employment = db.Column(db.Integer, nullable=True)

    def __init__(self, msa_id, metro_area, occ_code, job_group, total_employment):
        self.msa_id = msa_id
        self.metro_area = metro_area
        self.occ_code = occ_code
        self.job_group = job_group
        self.total_employment = total_employment

    def __repr__(self):
        return 'EmploymentModel(msa_id=%s, metro_area=%s, occ_code,=%s, job_group,=%s, total_employment,=%s)' % (self.msa_id, self.metro_area, self.occ_code, self.job_group, self.total_employment)

    def json(self):
        return {'msa_id': self.msa_id, 'metro_area': self.metro_area, 'occ_code': self.occ_code, 'job_group': self.job_group, 'total_employment': self.total_employment}

    @classmethod
    def find_by_name(cls, job_group) -> "EmploymentModel":
        return cls.query.filter_by(job_group=job_group).first()

    @classmethod
    def find_by_id(cls, _id) -> "EmploymentModel":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_all(cls) -> List["EmploymentModel"]:
        return cls.query.all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
