from app import create_app
from extensions import db
from models import Mentor

app = create_app()

with app.app_context():
    db.create_all()

    mentors = [
        Mentor(
            nom="Koffi Mensah",
            competences=["Python", "SQL", "Algo"],
            disponibilites=[
                {"jour": "lundi", "debut": 8, "fin": 12},
                {"jour": "mercredi", "debut": 14, "fin": 18}
            ],
            filiere="GL",
            niveau="L3",
            format="en_ligne"
        ),
        Mentor(
            nom="Aminata Diallo",
            competences=["Java", "Python", "Réseaux"],
            disponibilites=[
                {"jour": "mardi", "debut": 10, "fin": 16},
                {"jour": "jeudi", "debut": 8, "fin": 12}
            ],
            filiere="SI",
            niveau="L2",
            format="presentiel"
        ),
        Mentor(
            nom="Jacques Ahouansou",
            competences=["Anglais", "Stats", "SQL"],
            disponibilites=[
                {"jour": "lundi", "debut": 9, "fin": 13},
                {"jour": "vendredi", "debut": 14, "fin": 18}
            ],
            filiere="IA",
            niveau="L3",
            format="les_deux"
        )
    ]

    for m in mentors:
        db.session.add(m)
    db.session.commit()
    print("3 mentors ajoutés !")

