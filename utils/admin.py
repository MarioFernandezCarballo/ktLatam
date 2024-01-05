from database import User, Tournament, Club, Team

def patchPeru(app):
    for u in User.query.filter_by(country="Perú").all():
        u.country = "Peru"
        app.config['database'].session.commit()
    for t in Tournament.query.filter_by(country="Perú").all():
        t.country = "Peru"
        app.config['database'].session.commit()
    for c in Club.query.filter_by(country="Perú").all():
        c.country = "Peru"
        app.config['database'].session.commit()
    for c in Team.query.filter_by(country="Perú").all():
        c.country = "Peru"
        app.config['database'].session.commit()

def applyPatches(app):
    patchPeru(app)
    return 200