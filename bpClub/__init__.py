from flask import Blueprint, render_template, current_app
from flask_login import current_user

from utils.club import getClubs, getClub, getClubOnly


clubBP = Blueprint('clubBluePrint', __name__)


@clubBP.route("/clubs/<country>", methods={"GET", "POST"})
def clubsEndPoint(country):
    clb = getClubs(country)
    return render_template(
        'clubs.html',
        title="Clubes",
        clubs=clb,
        country=country,
        library=current_app.config['COUNTRIES'],
        user=current_user if not current_user.is_anonymous else None
    )


@clubBP.route("/club/<cl>", methods={"GET", "POST"})
def clubEndPoint(cl):
    club = getClubOnly(cl)
    clTor = getClub(cl)
    return render_template(
        'club.html',
        title=club.name,
        club=club,
        clTor=clTor,
        user=current_user if not current_user.is_anonymous else None
    )
