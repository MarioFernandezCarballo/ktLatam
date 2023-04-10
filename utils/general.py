from sqlalchemy import desc

from database import User, Team, Tournament, UserTournament, UserFaction, Club, Faction, UserClub


def updateStats(db):
    for usr in User.query.all():
        usr.bcpScore = 0
        best = db.session.query(UserTournament, Tournament).order_by(desc(UserTournament.bcpScore)).filter(
            UserTournament.userId == usr.id).join(Tournament, Tournament.id == UserTournament.tournamentId).all()
        counter = 0
        for to in best:
            if not to.Tournament.isTeam:
                to.UserTournament.countingScore = False
                counter += 1
                if counter <= 5:
                    usr.bcpScore += to.UserTournament.bcpScore
                    to.UserTournament.countingScore = True
    for tm in Team.query.all():
        best = db.session.query(UserTournament, Tournament).order_by(desc(UserTournament.bcpScore)).filter(
            UserTournament.teamId == tm.id).join(Tournament, Tournament.id == UserTournament.tournamentId).all()
        tm.bcpScore = sum([t.UserTournament.bcpTeamScore for t in best[:4]]) / 3  # Team Players
    for cl in Club.query.all():
        cl.bcpScore = 0
        countClub = 0
        for usr in cl.users:
            usCl = UserClub.query.filter_by(clubId=cl.id).filter_by(userId=usr.id).first()
            usCl.bcpScore = 0
            count = 0
            for t in UserTournament.query.filter_by(clubId=cl.id).filter_by(userId=usr.id).order_by(
                    desc(UserTournament.bcpScore)).all():
                t.countingScoreClub = False
                count += 1
                if countClub <= 10:
                    if count <= 3:
                        usCl.bcpScore += t.bcpScore
                        cl.bcpScore += t.bcpScore
                        t.countingScoreClub = True
                        countClub += 1
                else:
                    break
            if countClub > 10:
                break
    for fct in Faction.query.all():
        fct.bcpScore = 0
        for usr in fct.users:
            usFct = UserFaction.query.filter_by(factionId=fct.id).filter_by(userId=usr.id).first()
            usFct.bcpScore = 0
            count = 0
            for t in UserTournament.query.filter_by(factionId=fct.id).filter_by(userId=usr.id).order_by(desc(UserTournament.bcpScore)).all():
                t.countingScoreFaction = False
                count += 1
                if count <= 4:
                    usFct.bcpScore += t.bcpScore
                    fct.bcpScore += t.bcpScore
                    t.countingScoreFaction = True
    db.session.commit()
    return 200
