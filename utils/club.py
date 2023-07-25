from flask import current_app
from sqlalchemy import desc

from database import Club, Tournament, UserTournament


def getClub(te):
    return current_app.config["database"].session.query(UserTournament, Tournament, Club
                                                        ).filter(UserTournament.clubId == te
                                                                 ).join(Tournament,
                                                                        Tournament.id == UserTournament.tournamentId
                                                                        ).join(Club,
                                                                               Club.id == UserTournament.clubId).all()


def getClubOnly(te):
    return Club.query.filter_by(id=te).first()


def getClubs(country, qty=0):
    if qty > 0:
        result = Club.query.filter(Club.bcpScore > 0).order_by(desc(Club.bcpScore)).all() if country == "latam" else Club.query.filter_by(country=current_app.config["COUNTRIES"][country]).order_by(desc(Club.bcpScore)).all()
        return result[0:qty-1]
    else:
        return Club.query.filter(Club.bcpScore > 0).order_by(desc(Club.bcpScore)).all() if country == "latam" else Club.query.filter_by(country=current_app.config["COUNTRIES"][country]).order_by(desc(Club.bcpScore)).all()


def addClub(db, te, tor):
    if te['team']:
        if not Club.query.filter_by(bcpId=te['teamId']).filter_by(country=tor.country).first():
            db.session.add(Club(
                bcpId=te['teamId'],
                name=te['team']['name'].strip(),
                country=tor.country,
                shortName=te['team']['name'].replace(" ", "").lower()
            ))
    db.session.commit()
    return Club.query.filter_by(bcpId=te['teamId']).filter_by(country=tor.country).first() if te['team'] else None


def updateClub(db):
    users = Club.query.all()
    for usr in users:
        if usr.country == "Perú":
            usr.country = "Peru"
    db.session.commit()
