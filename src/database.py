
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class Image(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(),unique=False, nullable=False)
    explanation = db.Column(db.String(),nullable=False)
    url = db.Column(db.Text(),unique=True,nullable=False)
    hdurl = db.Column(db.Text(),unique=True,nullable=True)

    def __repr__(self) -> str: 
        return "Image>>> {self.url}"
