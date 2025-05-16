from routes import app, mongo
from flask_socketio import SocketIO, emit
from flask import session, request
from pytz import timezone, utc
from form import CommentForm
import datetime

socketio = SocketIO(app)


@socketio.on("new_comment")
def handle_new_comment(data):
    """
    Réception d'un nouveau commentaire
    """

    # Si l'utilisateur n'est pas connecté, renvoyer une erreur
    if "username" not in session:
        emit(
            "auth_error",
            {"message": "Vous devez être connecté pour poster un commentaire."},
            room=request.sid,
        )
        return

    # Récupérer les infos saisies par l'utilisateur + echaper les caractères spéciaux
    comment = data.get("comment")
    topic_filter = data.get("topic")
    username = session["username"]

    # Formulaire de commentaire
    form_com = CommentForm()

    # Récupérer le label du topic
    topic_label = dict(form_com.topic.choices).get(topic_filter)

    # Récupérer l'heure actuelle en UTC
    utc_now = datetime.datetime.now(utc)

    # Convertir l'heure en fuseau horaire français (CET/CEST)
    french_timezone = timezone("Europe/Paris")
    french_time = utc_now.astimezone(french_timezone)

    # formatter la date en français
    formatted_time = french_time.strftime("%d/%m/%Y %H:%M")

    # Insertion du commentaire dans la base de données
    mongo.db.comments.insert_one(
        {
            "username": username,
            "comment": comment,
            "topic": topic_filter,
            "topic_label": topic_label,
            "time": formatted_time,
        }
    )

    # Réémettre à tous les clients pour affichage en temps réel
    emit(
        "broadcast_comment",
        {
            "username": username,
            "comment": comment,
            "topic_label": topic_label,
            "time": formatted_time,
        },
        broadcast=True,
    )


# Main
if __name__ == "__main__":
    # Lancer le serveur accessible sur toutes les interfaces
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)
