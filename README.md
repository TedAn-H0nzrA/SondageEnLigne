# Sondage en Ligne - Django

## Description

Ce projet est une application web de sondage en ligne permettant aux administrateurs de créer des enquêteurs, qui à leur tour créent et gèrent des enquêtes. Les participants peuvent répondre aux enquêtes via un lien reçu par email.

## Fonctionnalités

- Gestion des utilisateurs (administrateurs, enquêteurs)
- Création et gestion des enquêtes et des questions
- Envoi de liens aux participants pour répondre aux sondages
- Stockage et analyse des réponses

## Technologies utilisées

- **Langage** : Python
- **Framework Web** : Django
- **Base de données** : SQLite
- **Frontend** : Django Templates

## Structure du projet

Le projet est divisé en trois applications principales :

1. **Utilisateurs** : Gestion des administrateurs et enquêteurs.
2. **Enquêtes** : Gestion des enquêtes et des questions.
3. **Réponses** : Stockage et gestion des réponses des participants.

## Installation

### Prérequis

- Python 3.8+
- pip et virtualenv

### Étapes d'installation

1. Cloner le dépôt :

   ```sh
   git clone https://github.com/TedAn-H0nzrA/SondageEnLigne.git
   cd SondageEnLigne
   ```

2. Créer et activer un environnement virtuel :

   ```sh
   python -m venv environment
   source environment/bin/activate  # Sur macOS/Linux
   environment\Scripts\activate     # Sur Windows
   ```

3. Installer les dépendances :

   ```sh
   pip install -r requirements.txt
   ```

4. Appliquer les migrations :

   ```sh
   python manage.py migrate
   ```

5. Lancer le serveur de développement :

   ```sh
   python manage.py runserver
   ```

6. Accéder à l'application :
   - Interface d'administration : `http://127.0.0.1:8000/admin/`
   - Interface utilisateur (selon implémentation) : `http://127.0.0.1:8000/`

## Contribution

1. Forker le projet
2. Créer une branche (`feature-nouvelle-fonctionnalite`)
3. Committer vos changements (`git commit -m 'Ajout d'une nouvelle fonctionnalité'`)
4. Pousser la branche (`git push origin feature-nouvelle-fonctionnalite`)
5. Ouvrir une Pull Request
