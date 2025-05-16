# Import utils
from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    EmailField,
    SubmitField,
    TextAreaField,
    SelectField,
)
from wtforms.validators import DataRequired, Email, Length


# Formulaire de connexion
class LoginForm(FlaskForm):

    # Nom d'utilisateur
    username = StringField("Nom d'utilisateur", validators=[DataRequired()])
    
    # Mot de passe
    password = PasswordField("Mot de passe", validators=[DataRequired()])
    
    # Champ pour soumettre le formulaire
    submit = SubmitField("Connexion")


# Formulaire d'inscription
class SigninForm(FlaskForm):
    
    # Email de l'utilisateur 
    email = EmailField("Email", validators=[DataRequired(), Email()])
    
    # Nom d'utilisateur
    username = StringField("Nom d'utilisateur", validators=[DataRequired()])

    # Mot de passe
    password = PasswordField("Mot de passe", validators=[DataRequired(), Length(min=6)])
    
    # Champ pour soumettre le formulaire
    submit = SubmitField("Inscription")


# Formulaire commentaire
class CommentForm(FlaskForm):
    
    # Commentaire
    comment = TextAreaField("Votre commentaire", validators=[DataRequired()])
    
    # Choix des topics disponibles
    topic = SelectField(
        "Choisissez un sujet",
        choices=[
            ("cooking", "Cuisine"),
            ("sport", "Sport"),
            ("religion", "Religion"),
            ("philosophy", "Philosophie"),
            ("technology", "Technologie"),
            ("entertainment", "Divertissement"),
            ("other", "Autre"),
        ],
        validators=[DataRequired()],
    )

    # Champ pour soumettre le formulaire
    submit = SubmitField("Poster")


# Formulaire filtre
class CommentFilterForm(FlaskForm):
    
    # Choix des topics disponibles, placé à "all" par défaut pour la requête GET
    topic_filter = SelectField(
        "Filtrer par sujet",
        choices=[
            ("all", "-- Tous les sujets --"),
            ("cooking", "Cuisine"),
            ("sport", "Sport"),
            ("religion", "Religion"),
            ("philosophy", "Philosophie"),
            ("technology", "Technologie"),
            ("entertainment", "Divertissement"),
            ("other", "Autre"),
        ],
        default="all",
    )

    # Champ pour soumettre le formulaire
    submit_filter = SubmitField("Filtrer")
