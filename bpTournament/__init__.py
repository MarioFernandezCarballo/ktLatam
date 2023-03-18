from flask import Blueprint, render_template, current_app
from flask_login import current_user

from utils.tournament import getAllTournaments

tournamentBP = Blueprint('tournamentBluePrint', __name__)


@tournamentBP.route("/tournaments/<country>", methods={"GET", "POST"})
def tournamentsEndPoint(country):
    tors = getAllTournaments(country)
    return render_template(
        'tournaments.html',
        title="Torneos",
        country=current_app.config['COUNTRIES'][country],
        user=current_user if not current_user.is_anonymous else None,
        tors=tors
    )
