from sqlalchemy import desc

from database import User, Team, Tournament, UserTournament, UserFaction, UserClub, Club


def updateStats(db, tor=None):
    if tor:
        for usr in tor.users:
            best = db.session.query(UserTournament, Tournament).order_by(desc(UserTournament.ibericonScore)).filter(
                UserTournament.userId == usr.id).join(Tournament, Tournament.id == UserTournament.tournamentId).all()
            cities = {}
            score = 0
            counter = 0
            for to in best:
                if not to.Tournament.isTeam:
                    to.UserTournament.countingScore = False
                    try:
                        cities[to.Tournament.city] += 1
                    except KeyError:
                        cities[to.Tournament.city] = 1

                    if cities[to.Tournament.city] <= 3:
                        score += to.UserTournament.ibericonScore
                        to.UserTournament.countingScore = True
                        counter += 1
                    if counter == 4:
                        break
            usr.ibericonScore = score
            for usrFct in UserFaction.query.filter_by(userId=usr.id).all():
                score = 0
                count = 0
                for t in best:
                    if t.UserTournament.factionId == usrFct.factionId:
                        count += 1
                        score += t.UserTournament.ibericonScore
                    if count == 3:
                        break
                usrFct.ibericonScore = score
            for usrCl in UserClub.query.filter_by(userId=usr.id).all():
                score = 0
                count = 0
                for t in best:
                    if t.UserTournament.clubId == usrCl.clubId:
                        count += 1
                        score += t.UserTournament.ibericonScore
                    if count == 3:
                        break
                usrCl.ibericonScore = score
        for tm in tor.teams:
            best = db.session.query(UserTournament, Tournament).order_by(desc(UserTournament.ibericonScore)).filter(
                UserTournament.teamId == tm.id).join(Tournament, Tournament.id == UserTournament.tournamentId).all()
            tm.ibericonScore = sum([t.UserTournament.ibericonTeamScore for t in best[:4]]) / 3  # Team Players
        for cl in Club.query.all():
            best = UserClub.query.filter_by(clubId=cl.id).order_by(desc(UserClub.ibericonScore)).all()
            cl.ibericonScore = sum([t.ibericonScore for t in best[:10]])
    else:
        for usr in User.query.all():
            best = db.session.query(UserTournament, Tournament).order_by(desc(UserTournament.ibericonScore)).filter(
                UserTournament.userId == usr.id).join(Tournament, Tournament.id == UserTournament.tournamentId).all()
            cities = {}
            score = 0
            counter = 0
            for to in best:
                if not to.Tournament.isTeam:
                    to.UserTournament.countingScore = False
                    try:
                        cities[to.Tournament.city] += 1
                    except KeyError:
                        cities[to.Tournament.city] = 1

                    if cities[to.Tournament.city] <= 3:
                        score += to.UserTournament.ibericonScore
                        to.UserTournament.countingScore = True
                        counter += 1
                    if counter == 4:
                        break
            usr.ibericonScore = score
            for usrFct in UserFaction.query.filter_by(userId=usr.id).all():
                score = 0
                count = 0
                for t in best:
                    if t.UserTournament.factionId == usrFct.factionId:
                        count += 1
                        score += t.UserTournament.ibericonScore
                    if count == 3:
                        break
                usrFct.ibericonScore = score
            for usrCl in UserClub.query.filter_by(userId=usr.id).all():
                score = 0
                count = 0
                for t in best:
                    if t.UserTournament.clubId == usrCl.clubId:
                        count += 1
                        score += t.UserTournament.ibericonScore
                    if count == 3:
                        break
                usrCl.ibericonScore = score
        for tm in Team.query.all():
            best = db.session.query(UserTournament, Tournament).order_by(desc(UserTournament.ibericonTeamScore)).filter(
                UserTournament.teamId == tm.id).join(Tournament, Tournament.id == UserTournament.tournamentId).all()
            tm.ibericonScore = sum([t.UserTournament.ibericonTeamScore for t in best[:4]]) / 3  # Team Players
        for cl in Club.query.all():
            best = UserClub.query.filter_by(clubId=cl.id).order_by(desc(UserClub.ibericonScore)).all()
            cl.ibericonScore = sum([t.ibericonScore for t in best[:10]])
    db.session.commit()
    return 200
