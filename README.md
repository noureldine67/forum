# Forum Flask - Projet Python

Ce projet est un **forum de discussion** développé en Python avec le framework Flask.  
Il permet aux utilisateurs de créer un compte, se connecter, poster des commentaires et interagir dans un espace communautaire.

---

## Fonctionnalités principales

- Inscription et authentification des utilisateurs  
- Création et affichage de commentaires  
- Interface simple avec des templates HTML  

---

## Installation

1. Cloner le dépôt :  
   ```bash
   git clone https://ton-depot.git
   cd ton-projet-flask
````

2. Installer les dépendances :

   ```bash
   pip install -r requirements.txt
   ```

---

## Configuration de la base de données

Ce projet utilise une base de données **MongoDB** pour stocker les données du forum.

Tu dois disposer d’une base MongoDB accessible via une URI de ce type :

```
mongodb+srv://{username}:{password}@cluster0.kaxfyuy.mongodb.net/forum?retryWrites=true&w=majority&appName=Cluster0
```

Avant de lancer l’application, il est nécessaire d’**exporter** les variables d’environnement suivantes dans ton terminal :

```bash
export MONGO_USERNAME="ton_nom_utilisateur"
export MONGO_PASSWORD="ton_mot_de_passe"
```

Ces variables sont utilisées dans le code pour construire l’URI de connexion sécurisée.

---

## Lancement de l’application

```bash
python server.py
```

Par défaut, le serveur Flask utilise `host="0.0.0.0"`, ce qui signifie que l’application n’est pas limitée à `localhost` mais est accessible depuis d’autres machines du même réseau local, via l’adresse IP de la machine hébergeant le serveur.

L’application sera donc accessible à l’adresse :
`http://<IP_de_ta_machine>:5000`

---

## Remarques

* Ce projet est un exemple simple et peut être amélioré avec des fonctionnalités supplémentaires (modération, profils utilisateurs, notifications, etc.).
* Assure-toi que ta base MongoDB est accessible et que les identifiants sont corrects pour éviter les erreurs de connexion.

```