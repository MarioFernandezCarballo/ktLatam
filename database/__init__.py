from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin


db = SQLAlchemy()


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    bcpId = db.Column(db.String(30), nullable=False)
    bcpName = db.Column(db.String(100))
    name = db.Column(db.String(50))
    password = db.Column(db.String(200))
    shortName = db.Column(db.String(30))
    permissions = db.Column(db.Integer)
    bcpScore = db.Column(db.Float, default=0.0)
    winRate = db.Column(db.Float)
    factions = db.relationship('Faction', secondary="userfaction", cascade='all,delete', back_populates='users')
    teams = db.relationship('Team', secondary="userteam", cascade='all,delete', back_populates='users')
    clubs = db.relationship('Club', secondary="userclub", cascade='all,delete', back_populates='users')
    tournaments = db.relationship('Tournament', secondary="usertournament", back_populates='users')


class Team(db.Model):
    __tablename__ = 'team'
    id = db.Column(db.Integer, primary_key=True)
    bcpId = db.Column(db.String(30), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    shortName = db.Column(db.String(50))
    bcpScore = db.Column(db.Float, default=0.0)
    users = db.relationship('User', secondary="userteam", back_populates='teams')
    tournaments = db.relationship('Tournament', secondary='usertournament', back_populates='teams', overlaps="tournaments")


class Club(db.Model):
    __tablename__ = 'club'
    id = db.Column(db.Integer, primary_key=True)
    bcpId = db.Column(db.String(30), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    shortName = db.Column(db.String(50))
    bcpScore = db.Column(db.Float, default=0.0)
    users = db.relationship('User', secondary="userclub", back_populates='clubs')
    tournaments = db.relationship('Tournament', secondary='usertournament', back_populates='clubs', overlaps="tournaments")


class Faction(db.Model):
    __tablename__ = 'faction'
    id = db.Column(db.Integer, primary_key=True)
    bcpId = db.Column(db.String(30), nullable=False)
    name = db.Column(db.String(30), nullable=False)
    shortName = db.Column(db.String(30))
    users = db.relationship('User', secondary="userfaction", back_populates='factions')
    tournaments = db.relationship('Tournament', secondary="usertournament", back_populates='factions', overlaps="tournaments,tournaments")


class Tournament(db.Model):
    __tablename__ = 'tournament'
    id = db.Column(db.Integer, primary_key=True)
    bcpId = db.Column(db.String(30), nullable=False)
    bcpUri = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    shortName = db.Column(db.String(50))
    city = db.Column(db.String(50))
    date = db.Column(db.String(50))
    isTeam = db.Column(db.Boolean)
    totalPlayers = db.Column(db.Integer)
    rounds = db.Column(db.Integer)
    users = db.relationship('User', secondary="usertournament", cascade='all,delete', back_populates='tournaments', overlaps="tournaments,tournaments,tournaments")
    teams = db.relationship('Team', secondary="usertournament", cascade='all,delete', back_populates='tournaments', overlaps="tournaments,tournaments,tournaments,users")
    clubs = db.relationship('Club', secondary="usertournament", cascade='all,delete', back_populates='tournaments', overlaps="teams,tournaments,tournaments,tournaments,users")
    factions = db.relationship('Faction', secondary="usertournament", cascade='all,delete', back_populates='tournaments', overlaps="clubs,teams,tournaments,tournaments,tournaments,users")


class UserTournament(db.Model):
    __tablename__ = 'usertournament'
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'))
    factionId = db.Column(db.Integer, db.ForeignKey('faction.id'))
    teamId = db.Column(db.Integer, db.ForeignKey('team.id'))
    clubId = db.Column(db.Integer, db.ForeignKey('club.id'))
    tournamentId = db.Column(db.Integer, db.ForeignKey('tournament.id'))
    position = db.Column(db.Integer)
    teamPosition = db.Column(db.Integer)
    bcpScore = db.Column(db.Float, default=0.0)
    bcpTeamScore = db.Column(db.Float, default=0.0)
    countingScore = db.Column(db.Boolean, default=False)
    performance = db.Column(db.String(500))


class UserFaction(db.Model):
    __tablename__ = 'userfaction'
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'))
    factionId = db.Column(db.Integer, db.ForeignKey('faction.id'))
    bcpScore = db.Column(db.Float, default=0.0)


class UserTeam(db.Model):
    __tablename__ = 'userteam'
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'))
    teamId = db.Column(db.Integer, db.ForeignKey('team.id'))
    bcpScore = db.Column(db.Float, default=0.0)


class UserClub(db.Model):
    __tablename__ = 'userclub'
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'))
    clubId = db.Column(db.Integer, db.ForeignKey('club.id'))
    bcpScore = db.Column(db.Float, default=0.0)
