from extensions import db

class Mentor(db.Model):
    __tablename__ = 'mentors'
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    competences = db.Column(db.JSON, nullable=False)       # ["Python", "SQL"]
    disponibilites = db.Column(db.JSON, nullable=False)    # [{"jour":"lundi","debut":8,"fin":12}]
    filiere = db.Column(db.String(100))
    niveau = db.Column(db.String(50))
    format = db.Column(db.String(20), default="les_deux")  # presentiel, en_ligne, les_deux
