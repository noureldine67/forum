# Import utils
from flask import (
    render_template,
    redirect,
    url_for,
    request,
    flash,
    session,
)
from werkzeug.security import generate_password_hash, check_password_hash
from form import LoginForm, SigninForm, CommentForm, CommentFilterForm
from app_configuration import create_app

# Récupérer l'application, le limiteur et la base de données
app, limiter, mongo = create_app()


@app.after_request
def add_security_headers(response):

    # Protection contre le clickjacking
    response.headers["X-Frame-Options"] = "DENY"
    # Empêche le MIME sniffing
    response.headers["X-Content-Type-Options"] = "nosniff"
    # Contrôle des referrers
    response.headers["Referrer-Policy"] = "no-referrer-when-downgrade"

    # Limite les API navigateur (ici : désactive la géolocalisation)
    response.headers["Permissions-Policy"] = "geolocation=()"

    # response.headers["Strict-Transport-Security"] = "max-age=63072000; includeSubDomains; preload"  # Force HTTPS (utile si tu actives SSL)
    return response


@app.route("/")
def index():
    """
    Page d'accueil du forum
    """
    # Requête GET, Renvoyer la page index.html + un code valant 200
    return render_template("html/index.html"), 200


@app.route("/signin", methods=["GET", "POST"])
def signin():
    """
    Page d'inscription utilisateur
    """
    # Formulaire d'inscription
    form = SigninForm()

    # Réception d'une requête POST correspondant à l'envoie d'un formulaire d'inscription
    if form.validate_on_submit():

        # Récupération des données du formulaire + echaper les caractères spéciaux
        email = form.email.data
        username = form.username.data
        # Hash du mot de passe pour la sécurité
        password = generate_password_hash(form.password.data)

        # Vérification de l'unicité de l'utilisateur (email ou nom d'utilisateur déjà existant)
        existing_user = mongo.db.users.find_one(
            {"$or": [{"email": email}, {"username": username}]}
        )

        # Si l'utilisateur n'est pas vide alors on affiche un message d'erreur
        if existing_user:
            # Afficher un message d'erreur à l'écran
            flash("Erreur : email ou nom d'utilisateur déjà utilisé.", "danger")

            # Redirection sur la même page
            return redirect(url_for("signin"))

        # Insertion du nouvel utilisateur dans la base de données
        mongo.db.users.insert_one(
            {"email": email, "username": username, "password": password}
        )

        # Afficher un message de succès à l'écran
        flash("Création de compte avec succès!", "success")

        # Redirection vers la page de connexion
        return redirect(url_for("login"))

    # Requête GET de la part d'un utilisateur, renvoyer la page signin.html + code valant 200
    return render_template("html/signin.html", form=form), 200


# Limiteur mis en place pour ralentir en cas d'attaque par force brute
@limiter.limit("5 per minute")
@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Page de connexion utilisateur
    """
    # Formulaire de connexion
    form = LoginForm()

    # Réception d'une requête POST correspondant à l'envoie d'un formulaire de connexion
    if form.validate_on_submit():

        # Récupération des champs
        username = form.username.data
        password = form.password.data

        # Recherche de l'utilisateur dans la base de données
        user = mongo.db.users.find_one({"username": username})

        # Si le user n'est pas vide et que le mot de passe saisi correspond au mot de passe de la base de données
        if user and check_password_hash(user["password"], password):

            # Ajouter l'utilisateur dans la session
            session["username"] = username

            # Afficher un message à l'écran comme quoi l'utilisateur est bien connecté
            flash("Connexion avec succès.", "success")

            # Redirection vers la page de commentaires
            return redirect(url_for("comments"))

        # Si l'utilisateur est vide ou bien le mot de passe faux alors
        else:

            # Afficher un message d'erreur à l'écran
            flash("Erreur : nom d'utilisateur ou mot de passe incorrect.", "danger")

            # Redirection vers la page de connexion
            return redirect(url_for("login"))

    # Requête GET, renvoyer la page login.html + code valant 200
    return render_template("html/login.html", form=form), 200


@app.route("/logout")
def logout():
    """
    Déconnexion de l'utilisateur
    """
    # Retirer l'utilisateur de la session
    session.pop("username", None)

    # Afficher un message à l'écran pour prévenir l'utilisateur qu'il a bien été deconnecté
    flash("Vous avez été déconnecté.", "success")

    # Renvoyer vers la page de connexion
    return redirect(url_for("login"))


@app.route("/comments")
def comments():
    """
    Récupérer les commentaires présent dans la base de données et les renvoyer à la page comments.html
    """

    # Récupére les infos du formulaire permettant de filtrer les commentaires par topic
    form_filter = CommentFilterForm(request.args)
    topic_filter = form_filter.topic_filter.data

    # Si le filtre vaut tout alors on renvoyant tous les commentaires dans la base de données
    if topic_filter == "all":
        comments = mongo.db.comments.find()

    # Sinon on filtre par le topic
    else:
        comments = mongo.db.comments.find({"topic": topic_filter})

    # Transformer sous formes de liste
    comments = list(comments)

    # Si aucun utilisateur n'est présent dans la session alors ne pas instancier le formulaire permettant de commenter
    form_com = None if "username" not in session else CommentForm()

    # Renvoyer la page comments.html + code valant 200
    return (
        render_template(
            "html/comments.html",
            form_com=form_com,
            form_filter=form_filter,
            comments=comments,
        ),
        200,
    )


@app.errorhandler(429)
def handle_429(e):
    """
    Gestion de l'erreur 429
    """
    # Renvoyer vers la page error429.html + code valant 200
    return render_template("html/error429.html"), 200
