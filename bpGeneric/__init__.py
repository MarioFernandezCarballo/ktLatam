from flask import Blueprint, render_template
from flask_login import current_user

from utils.user import getUsers, getUserOnly
from utils.team import getTeams
from utils.club import getClubs


genericBP = Blueprint('genericBluePrint', __name__)


@genericBP.route("/", methods={"GET", "POST"})
def generalEndPoint():
    usr = getUsers()
    tms = getTeams()
    clb = getClubs()
    golden1 = None  # getUserOnly(X)  TODO ganador torneo Madrid
    golden2 = None  # getUserOnly(X)  TODO ganador torneo Silver
    golden3 = None  # getUserOnly(X)  TODO ganador torneo Final 16
    silver1 = getUserOnly(3)  # 2023 Chapu
    silver2 = getUserOnly(4)  # 2023 Ace
    silver3 = None  # getUserOnly(X)  TODO ganador Valladolid
    silver4 = None  # getUserOnly(X)  TODO ganador La Cabra
    return render_template(
        'general.html',
        title="General",
        users=usr,
        teams=tms,
        clubs=clb,
        golden1=golden1,
        golden2=golden2,
        golden3=golden3,
        silver1=silver1,
        silver2=silver2,
        silver3=silver3,
        silver4=silver4,
        user=current_user if not current_user.is_anonymous else None
    )


@genericBP.route("/about", methods={"GET", "POST"})
def aboutEndPoint():
    return render_template(
        'about.html',
        title="About",
        user=current_user if not current_user.is_anonymous else None
    )
