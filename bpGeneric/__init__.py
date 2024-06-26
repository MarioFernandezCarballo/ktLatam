from flask import Blueprint, render_template, current_app
from flask_login import current_user

from utils.user import getUsers
from utils.team import getTeams
from utils.club import getClubs


genericBP = Blueprint('genericBluePrint', __name__)


@genericBP.route("/", methods={"GET", "POST"})
def generalEndPoint():
    usr = getUsers("latam")
    tms = getTeams("latam")
    clb = getClubs("latam")
    return render_template(
        'general.html',
        title="General",
        users=usr,
        teams=tms,
        clubs=clb,
        library=current_app.config['COUNTRIES'],
        user=current_user if not current_user.is_anonymous else None
    )


@genericBP.route("/about", methods={"GET", "POST"})
def aboutEndPoint():
    return render_template(
        'about.html',
        title="Información",
        user=current_user if not current_user.is_anonymous else None
    )


@genericBP.route("/sponsor", methods={"GET", "POST"})
def sponsorsEndPoint():
    return render_template(
        'sponsor.html',
        title="Patrocinios",
        user=current_user if not current_user.is_anonymous else None
    )

@genericBP.route("/privacy", methods={"GET", "POST"})
def privacyEndPoint():
    return render_template(
        'privacy.html',
        title="Privacidad y Seguridad",
        user=current_user if not current_user.is_anonymous else None
    )

@genericBP.route('/hof/<year>/<country>', methods={"GET"})
def hallOfFameEndPoint(year, country):
    return render_template(
        'hof' + year + country + '.html',
        title="HoF 23-24",
        user=current_user if not current_user.is_anonymous else None
    )
