
# 🗳️ Sondage en Ligne - Django

## 📌 Description

Cette application web de sondage permet aux **administrateurs** de créer des **enquêteurs**, qui peuvent ensuite créer et gérer des **enquêtes**.  
Les **participants** accèdent aux sondages via un lien reçu par email pour y répondre.

---

## ✨ Fonctionnalités

- 🔐 Gestion des rôles utilisateurs : Administrateurs & Enquêteurs
- 📝 Création et gestion des enquêtes et de leurs questions
- 📩 Envoi de liens aux participants par email
- 📊 Collecte et analyse des réponses

---

## 🛠️ Technologies

- **Langage** : Python
- **Framework** : Django
- **Base de données** : SQLite
- **Frontend** : Django Templates (HTML/CSS)

---

## 🧭 Structure du projet

Le projet est organisé autour de trois applications Django principales :

| **Application**   | **Rôle**                                      |
|--------------------|-----------------------------------------------|
| `utilisateurs`     | Gère les comptes Administrateurs et Enquêteurs |
| `enquetes`         | Crée les enquêtes et leurs questions          |
| `reponses`         | Stocke et traite les réponses des participants |

---

## 🚀 Installation

### ✅ Prérequis

- Python 3.8+
- `pip` et `virtualenv`

### 📦 Étapes

1. **Créer un environnement virtuel** :

   ```bash
   python -m venv env
   source env/bin/activate      # macOS/Linux
   env\Scripts\activate         # Windows
   ```

2. **Cloner le dépôt** :

   ```bash
   git clone https://github.com/TedAn-H0nzrA/SondageEnLigne.git
   cd SondageEnLigne
   ```

3. **Installer les dépendances** :

   ```bash
   pip install -r requirements.txt
   ```

4. **Appliquer les migrations** :

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Charger les rôles initiaux** :

   ```bash
   python manage.py loaddata initial_roles.json
   ```

6. **Lancer le serveur de développement** :

   ```bash
   python manage.py runserver
   ```

7. **Accéder à l'application** :
   <!-- - Admin : [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/) -->
   - Interface utilisateur : [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## 👤 Création d'un administrateur (via terminal)

Avec username explicite :

```bash
python manage.py create_admin your@gmail.com yourpassword --username yourusername
```

Sans username (généré automatiquement depuis l'email) :

```bash
python manage.py create_admin your@gmail.com yourpassword
```

---

## Suppression des fichier inutile

```bash
# Supprimer les fichiers __pycache__
find . -type d -name "__pycache__" -exec rm -r {} +

# Supprimer les migrations (sauf __init__.py)
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete

# Supprimer la base de données
rm db.sqlite3
```
