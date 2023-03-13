import json
import secrets
import os
import requests

from werkzeug.security import generate_password_hash

from database import db, User
from bpAuth import loginManager, jwt


def createApp(app):
    config = json.load(open("secret/config.json"))

    app.config["SECRET_KEY"] = handleSecretKey()
    app.config['PORT'] = config['port']
    app.config['HOST'] = config['host']

    app.config["JWT_SECRET_KEY"] = handleSecretKey()
    app.config["JWT_TOKEN_LOCATION"] = ["cookies"]

    app.config["SQLALCHEMY_DATABASE_URI"] = config['db-uri']
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    app.config["BCP_API_EVENT"] = config['api-event-uri']
    app.config["BCP_API_USER"] = config['api-user-uri']
    app.config["BCP_API_USERS"] = config['api-users-uri']
    app.config["BCP_API_TEAM"] = config['api-team-uri']
    app.config["BCP_API_TEAM_PLACINGS"] = config['api-team-placings-uri']

    app.config["ADMIN_USERNAME"] = config['admin-name']
    app.config["ADMIN_PASSWORD"] = config['admin-password']

    app.config["COLLABORATOR_USERNAME"] = config['collab-name']
    app.config["COLLABORATOR_PASSWORD"] = config['collab-password']

    loginManager.init_app(app)
    app.config["loginManager"] = loginManager
    jwt.init_app(app)
    app.config["jwt"] = jwt
    db.init_app(app)
    app.config["database"] = db

    return app


def createDatabase(app):
    with app.app_context():
        if os.path.exists('database.txt'):
            pass
        else:
            createTables(app.config['database'])
            createAdmin(app)
            createCollaborator(app)
            file = open('database.txt', 'w')
            file.write("Database Created")
            file.close()


def handleSecretKey():
    keys = json.load(open("secret/config.json"))
    if keys['secret-key']:
        return keys['secret-key']
    else:
        key = secrets.token_hex(16)
        keys['secret-key'] = key
        json.dump(keys, open("secret/config.json", 'w'), indent=4)
        return key


def createTables(database):
    database.create_all()
    database.session.commit()


def createAdmin(app):
    new_user = User(
        bcpId="0000000000",
        name=app.config["ADMIN_USERNAME"],
        password=generate_password_hash(app.config["ADMIN_PASSWORD"], method='sha256'),
        permissions=15
    )
    app.config['database'].session.add(new_user)
    app.config['database'].session.commit()


def createCollaborator(app):
    new_user = User(
        bcpId="0000000000",
        name=app.config["COLLABORATOR_USERNAME"],
        password=generate_password_hash(app.config["COLLABORATOR_PASSWORD"], method='sha256'),
        permissions=13
    )
    app.config['database'].session.add(new_user)
    app.config['database'].session.commit()
