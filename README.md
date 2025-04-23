
# API Address Risk

API Dockerisée pour la gestion d'adresses et l'analyse des risques associés

## 🚀 Instructions de lancement

### Prérequis
- Docker 20.10+
- Docker Compose 2.0+

### Installation
```bash
git clone [URL_DU_DEPOT]
cd address-risk-api
cp .env.example .env  # Configurer les variables si nécessaire
```

### Lancer l'application
```bash
docker compose build
docker compose up
```
L'API sera disponible sur http://localhost:8000

## 🔧 Variables d'environnement

Fichier `.env` à créer :
```ini
# Configuration de base
DEBUG=True
SECRET_KEY=votre_clé_secrète

# Base de données
DATABASE_URL=sqlite:////app/data/db.sqlite3

# Timeouts API externes (en secondes)
BAN_API_TIMEOUT=5
GEORISQUES_API_TIMEOUT=5
```

## 🌐 Architecture de l'application

```
.
├── Dockerfile                # Configuration Docker
├── docker-compose.yml        # Orchestration
├── requirements.txt          # Dépendances Python
├── addresses/                # Application principale
│   ├── models.py             # Modèle Address
│   ├── serializers.py        # Sérialisation des données
│   ├── views.py              # Logique des endpoints
│   ├── urls.py               # Routes API
│   └── tests.py              # Tests unitaires
├── config/                   # Configuration Django
│   ├── settings.py           # Paramètres
│   └── urls.py               # Routes principales
└── data/                     # Volume de données
    └── db.sqlite3            # Base SQLite
```

## 📡 Endpoints API

### POST /api/addresses/

Enregistre une nouvelle adresse via l'API BAN

**Requête** :
```json
{
  "q": "8 bd du Port"
}
```

**Réponses** :

- **200 Succès** :
```json
{
  "id": 1,
  "label": "8 bd du Port, 56170 Sarzeau",
  "housenumber": "8",
  "street": "bd du Port",
  "postcode": "56170",
  "citycode": "56242",
  "latitude": 47.58234,
  "longitude": -2.73745
}
```

- **400 Requête invalide** :
```json
{
  "error": "Le champ 'q' est requis et doit être une chaîne non vide."
}
```

### GET /api/addresses/<id>/risks/

Récupère les risques associés à une adresse

**Réponses** :

- **200 Succès** :
```json
{
  "risks": [
    {
      "type": "inondation",
      "level": "moyen"
    }
  ]
}
```

- **404 Adresse introuvable** :
```json
{
  "error": "Adresse non trouvée."
}
```

## 🧪 Tests

### Lancer tous les tests
```bash
docker compose exec web python manage.py test
```

### Tests disponibles
```bash
# Test création d'adresse
docker compose exec web python manage.py test addresses.tests.AddressAPITests

# Test récupération de risques
docker compose exec web python manage.py test addresses.tests.AddressRiskViewTest
```

## 🛠 Dépendances techniques

- **Backend** :
  - Django 5.0
  - Django REST Framework 3.14
  - Requests 2.31

- **Infrastructure** :
  - Docker
  - SQLite

📄 *Documentation mise à jour le 23/04/2025*
