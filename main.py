from flask import Flask
from utils import createApp, createDatabase

from bpGeneric import genericBP
from bpAuth import authBP
from bpAdmin import adminBP
from bpTeam import teamBP
from bpClub import clubBP
from bpUser import userBP
from bpFaction import factionBP
from bpTournament import tournamentBP

app = Flask(__name__)
app.register_blueprint(genericBP)
app.register_blueprint(authBP)
app.register_blueprint(adminBP)
app.register_blueprint(teamBP)
app.register_blueprint(clubBP)
app.register_blueprint(userBP)
app.register_blueprint(factionBP)
app.register_blueprint(tournamentBP)

app = createApp(app)
createDatabase(app)


if __name__ == '__main__':
    app.run(host=app.config['HOST'], port=app.config['PORT'], debug=app.config['DEBUG'])

# TODO
#  - Hacer página 404
#  - No dar informacion de la bd en html -> Eliminar caracteres especiales
#  - Cambiar cinco mejores puntuaciones y diez mejores en equipos con tres máximo por persona
#  - Borrar torneo

# TODO
#  - Añadir counting en bd para clubs y facciones
#  - Pensarlo bien para que quede bonico y pesioso
