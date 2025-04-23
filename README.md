
# API Address Risk - Documentation

![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)

API Dockerisée pour la gestion d'adresses et l'analyse des risques associés.

## 📋 Table des matières
- [Prérequis](#-prérequis)
- [Installation](#-installation)
- [Lancement](#-lancement)
- [Endpoints](#-endpoints)
- [Tests](#-tests)
- [Dépannage](#-dépannage)

## 🛠 Prérequis

- Docker 20.10+
- Docker Compose 2.2+
- Git 2.30+

```bash
# Vérification des versions
docker --version
docker-compose --version
git --version
```

## 🚀 Installation

### Cloner le dépôt :
```bash
git clone https://github.com/YOUSSEF-BOUJYDAH/address-risk-api.git
cd address-risk-api
```

### Configurer l'environnement :
```bash
cp .env.example .env
nano .env  # Éditer avec vos valeurs
```

### Construire l'image :
```bash
docker compose build
```

## 🏃 Lancement
```bash
# Démarrer les services
docker compose up

# Lancer en arrière-plan
docker compose up -d

# Arrêter les services
docker compose down
```

L'API sera disponible sur : http://localhost:8000

## 🌐 Endpoints

### POST /api/addresses/

Enregistre une nouvelle adresse

**Requête :**
```bash
curl -X POST http://localhost:8000/api/addresses/ \
  -H "Content-Type: application/json" \
  -d '{"q": "8 bd du Port"}'
```

**Réponse :**
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

### GET /api/addresses/<id>/risks/

Récupère les risques associés

**Requête :**
```bash
curl http://localhost:8000/api/addresses/1/risks/
```

## 🧪 Tests

### Tests unitaires
```bash
# Lancer tous les tests
docker compose exec web python manage.py test

# Lancer un test spécifique
docker compose exec web python manage.py test addresses.tests.AdresseAPITests
```

### Tests manuels
```bash
# Test création valide
curl -X POST http://localhost:8000/api/addresses/ -d '{"q": "test"}'

# Test erreur
curl -X POST http://localhost:8000/api/addresses/ -d '{"q": ""}'
```



## 🆘 Dépannage

**Problème : Erreurs de dépendances**  
**Solution :**
```bash
docker compose down
docker compose build --no-cache
```

**Problème : Variables d'environnement non chargées**  
**Vérifier :**
```bash
docker compose exec web env | grep DEBUG
```
