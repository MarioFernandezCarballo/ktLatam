from database import Faction, UserFaction, User
from flask import current_app
from sqlalchemy import desc, asc


def getFaction(fct):
    return current_app.config["database"].session.query(Faction, UserFaction).join(UserFaction).filter(
        Faction.id == fct).order_by(desc(UserFaction.bcpScore)).all()


def getFactionOnly(fct):
    return Faction.query.filter_by(id=fct).first()


def getFactions(country):
    if country == "latam":
        factUsers = current_app.config["database"].session.query(Faction, UserFaction, User).filter(
            Faction.id == UserFaction.factionId).filter(UserFaction.userId == User.id).order_by(Faction.name).order_by(
            desc(UserFaction.bcpScore)).all()
    else:
        factUsers = current_app.config["database"].session.query(Faction, UserFaction, User).filter(
            Faction.id == UserFaction.factionId).filter(UserFaction.userId == User.id).filter(User.country == country).order_by(Faction.name).order_by(
            desc(UserFaction.bcpScore)).all()
    return Faction.query.order_by(Faction.name).all(), factUsers


def addFaction(db, fct):
    if fct['army']:
        if not Faction.query.filter_by(bcpId=fct['armyId']).first():
            db.session.add(Faction(
                bcpId=fct['armyId'],
                name=fct['army']['name'].strip(),
                shortName=fct['army']['name'].replace(" ", "").lower()
            ))
    db.session.commit()
    return Faction.query.filter_by(bcpId=fct['armyId']).first() if fct['army'] else None
