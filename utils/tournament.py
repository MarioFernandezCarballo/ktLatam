import requests
import json

from flask import current_app
from geopy.geocoders import Nominatim

from database import Tournament, UserTournament
from utils.user import addUser
from utils.team import addTeam, getTeamUsers
from utils.faction import addFaction
from utils.club import addClub


def getTournament(to):
    return Tournament.query.filter_by(id=to).first()


def getAllTournaments():
    return Tournament.query.all()


def addNewTournament(db, form):
    if "https://www.bestcoastpairings.com/event/" in form['bcpLink']:
        eventId = form["bcpLink"].split("/")[-1].split("?")[0]
        uri = current_app.config["BCP_API_EVENT"].replace("####event####", eventId)
        response = requests.get(uri)
        info = json.loads(response.text)
        if not info['ended']:
            return 400, None
        if Tournament.query.filter_by(bcpId=info['id']).first():
            return 400, None
        tor = manageTournament(db, info)
        if tor.isTeam:
            manageTeams(db, tor)
        else:
            manageUsers(db, tor)
        return 200, tor
    return 400, None


def manageTournament(db, info):
    isTeamTournament = info['teamEvent']
    geoLocator = Nominatim(user_agent="geoapiExercises")
    location = geoLocator.reverse(str(info['coordinate'][1]) + "," + str(info['coordinate'][0]))
    try:
        city = location.raw['address']['state_district']
    except KeyError:
        city = location.raw['address']['city']
    db.session.add(Tournament(
        bcpId=info['id'],
        bcpUri="https://www.bestcoastpairings.com/event/" + info['id'],
        name=info['name'].strip(),
        shortName=info['name'].replace(" ", "").lower(),
        city=city,
        isTeam=isTeamTournament,
        date=info['eventDate'].split("T")[0],
        totalPlayers=info['totalPlayers'],
        rounds=info['numberOfRounds']
    ))
    db.session.commit()
    return Tournament.query.filter_by(bcpId=info['id']).first()


def manageUsers(db, tor):
    uri = current_app.config["BCP_API_USERS"].replace("####event####", tor.bcpId)
    response = requests.get(uri)
    info = json.loads(response.text)
    for user in info['data']:
        usr = addUser(db, user)
        fct = addFaction(db, user)
        cl = addClub(db, user)
        tor.users.append(usr)
        usrTor = UserTournament.query.filter_by(userId=usr.id).filter_by(tournamentId=tor.id).first()
        usrTor.position = user['placing']
        usrTor.performance = json.dumps(user['total_games'])

        uri = current_app.config["BCP_API_USER"].replace("####event####", tor.bcpId).replace("####user####", usr.bcpId)
        response = requests.get(uri)
        infoUsr = json.loads(response.text)

        usrTor.bcpScore = infoUsr['data'][0]['ITCPoints']

        if fct:
            if fct not in usr.factions:
                usr.factions.append(fct)
            usrTor.factionId = fct.id
        if cl:
            if cl not in usr.clubs:
                usr.clubs.append(cl)
            usrTor.clubId = cl.id
        db.session.commit()


def manageTeams(db, tor):
    uri = current_app.config["BCP_API_TEAM"].replace("####event####", tor.bcpId)
    response = requests.get(uri)
    infoTeams = json.loads(response.text)
    uri = current_app.config["BCP_API_TEAM_PLACINGS"].replace("####event####", tor.bcpId)
    response = requests.get(uri)
    infoTeamPlacings = json.loads(response.text)
    uri = current_app.config["BCP_API_USERS"].replace("####event####", tor.bcpId)
    response = requests.get(uri)
    infoUsers = json.loads(response.text)
    for teamPlacing in infoTeamPlacings['data']:
        team = [tpl for tpl in infoTeams['data'] if tpl['id'] == teamPlacing['id']][0]
        uss = getTeamUsers(team, infoUsers)
        tm = addTeam(db, team)
        if tm:
            tor.teams.append(tm)

        for us in uss:
            usr = addUser(db, us)
            fct = addFaction(db, us)
            cl = addClub(db, us)

            tor.users.append(usr)
            tm.users.append(usr)

            usrTor = UserTournament.query.filter_by(userId=usr.id).filter_by(tournamentId=tor.id).first()
            usrTor.position = us['placing']
            usrTor.performance = json.dumps('total_games')

            usrTor.teamPosition = teamPlacing['placing']

            performance = [0, 0, 0]
            maxPoints = len(teamPlacing['games']) * 3
            maxIbericon = 3
            playerModifier = 1 + tor.totalPlayers / 100
            for game in teamPlacing['games']:
                performance[game['gameResult']] += 1
            points = ((performance[2] * 3) + performance[1])
            finalPoints = points * maxIbericon / maxPoints
            usrTor.bcpTeamScore = finalPoints * playerModifier * 10
            usrTor.teamId = tm.id

            performance = [0, 0, 0]
            maxPoints = len(us['games']) * 3
            maxIbericon = 3
            playerModifier = 1 + tor.totalPlayers / 100
            for game in us['games']:
                performance[game['gameResult']] += 1
            points = ((performance[2] * 3) + performance[1])
            finalPoints = points * maxIbericon / maxPoints
            usrTor.bcpScore = finalPoints * playerModifier * 10

            if fct:
                if fct not in usr.factions:
                    usr.factions.append(fct)
                usrTor.factionId = fct.id
            if cl:
                if cl not in usr.clubs:
                    usr.clubs.append(cl)
                usrTor.clubId = cl.id
            db.session.commit()


def deleteTournament(db, to):
    UserTournament.query.filter_by(tournamentId=to).delete()
    db.session.delete(Tournament.query.filter_by(id=to).first())
    db.session.commit()
    return 200
