from app import db

ROLE_USER = 0
ROLE_ADMIN = 1

class Printer(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    model_name = db.Column(db.String(64), index = True, unique = True)

    def __repr__(self):
        return '<Printer %r>' % (self.model_name)
        
class PrintJob(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    timestamp = db.Column(db.DateTime)
    printer_id = db.Column(db.Integer, db.ForeignKey('printer.id'))
    
    def __repr__(self):
        return '<PrintJob %r>' % (self.id)