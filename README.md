# Forum Flask - Projet Python

Ce projet est un **forum de discussion** développé en Python avec Flask.
Il permet aux utilisateurs de créer un compte, se connecter, poster des commentaires et échanger au sein d’une communauté.

---

## Fonctionnalités principales

* Inscription et authentification des utilisateurs
* Publication et affichage de commentaires
* Interface simple avec des templates HTML

---

## Installation

1. Cloner le dépôt :

```bash
git clone https://ton-depot.git
cd ton-projet-flask
```

2. Installer les dépendances :

```bash
pip install -r requirements.txt
```

---

## Configuration de la base de données

Le projet utilise une base MongoDB pour stocker les données.

L’URI de connexion doit avoir cette forme :
`mongodb+srv://{username}:{password}@cluster0.kaxfyuy.mongodb.net/forum?retryWrites=true&w=majority&appName=Cluster0`

Avant de lancer l’application, exporte les variables d’environnement suivantes :

```bash
export MONGO_USERNAME="ton_nom_utilisateur"
export MONGO_PASSWORD="ton_mot_de_passe"
```

Ces variables seront utilisées pour construire l’URI de connexion dans le code.

---

## Lancement de l’application

```bash
python server.py
```

Le serveur Flask utilise `host="0.0.0.0"`, donc l’application est accessible non seulement en localhost, mais aussi depuis d’autres machines du réseau local via l’IP de la machine hébergeant le serveur.

L’adresse d’accès sera :
`http://<IP_de_ta_machine>:5000`

---

## Remarques

* Ce projet est un exemple simple qui peut être amélioré (modération, profils utilisateurs, notifications...).
* Vérifie que ta base MongoDB est accessible et que les identifiants sont corrects pour éviter les erreurs.

---