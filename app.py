from dotenv import load_dotenv
load_dotenv()

from flask import Flask, request, jsonify, send_from_directory
from config import Config
from extensions import db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    return app


app = create_app()

# Importer le modèle
from models import Mentor

# Créer les tables au démarrage
with app.app_context():
    db.create_all()

# ==================== MATCHING ====================
@app.route('/api/search', methods=['POST'])
def search():
    data = request.get_json()
    competences_recherchees = [c.lower() for c in data.get('competences', [])]
    jour_recherche = data.get('jour', '')
    heure_recherche = float(data.get('heure', 0))
    filiere = data.get('filiere', '')

    mentors = Mentor.query.all()
    resultats = []

    for mentor in mentors:
        # 1. Compétences communes
        competences_mentor = set(c.lower() for c in (mentor.competences or []))
        competences_user = set(competences_recherchees)
        communes = competences_mentor & competences_user

        if not communes:
            continue  # Pas de compétence commune → on ignore

        # 2. Compatibilité horaire (±1h)
        horaire_ok = False
        for dispo in mentor.disponibilites:
            if dispo['jour'].lower() == jour_recherche.lower():
                debut = dispo['debut']
                fin = dispo['fin']
                if debut - 1 <= heure_recherche <= fin + 1:
                    horaire_ok = True
                    break

        if not horaire_ok:
            continue  # Horaire incompatible → on ignore

        # 3. Score simple
        score = len(communes) * 20  # 20 points par compétence commune
        if filiere and mentor.filiere and filiere.lower() == mentor.filiere.lower():
            score += 10  # Bonus filière

        resultats.append({
            'id': mentor.id,
            'nom': mentor.nom,
            'competences_communes': list(communes),
            'disponibilites': mentor.disponibilites,
            'format': mentor.format,
            'filiere': mentor.filiere,
            'niveau': mentor.niveau,
            'score': score
        })

    # Trier par score décroissant
    resultats.sort(key=lambda x: x['score'], reverse=True)
    return jsonify(resultats)


# ==================== PAGE PRINCIPALE ====================
@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
