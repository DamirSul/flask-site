from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    image = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<Car {self.name}>'
