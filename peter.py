from client import Client
from models.parliamentrian import Parliamentarian
from models.connection import Connection


c = Client()
hess = c.get_parliamentarian(11)
# Parliamentarian.insert((hess['id'], hess['name']))
for connection in hess['connections']:
    Connection.insert((connection['to']['id'], connection['to']['name'], connection['potency'], hess['id']))
# print(c.get_organisation(6345))
