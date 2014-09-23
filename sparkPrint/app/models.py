from app import db

ROLE_USER = 0
ROLE_ADMIN = 1

class Printer(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    model_name = db.Column(db.String(64), index = True, unique = True)

    def __repr__(self):
        return '<Printer %r>' % (self.model_name)