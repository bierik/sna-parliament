from client import Client
from models.parliamentrian import Parliamentarian
from models.connection import Connection
from models.lobby_group import LobbyGroup
from models.model import Model
from tqdm import tqdm


def to_sqlite_tuple(value):
    value['id'] = Model.global_id(value['id'])
    return tuple(value.values())


c = Client()

parliamentarians = c.get_parliamentarians()
Parliamentarian.insert_many(list(map(to_sqlite_tuple, parliamentarians)))

lobby_groups = c.get_lobby_groups()
LobbyGroup.insert_many(list(map(to_sqlite_tuple, lobby_groups)))

for parliamentarian in tqdm(parliamentarians, desc='Parliamentarians'):
    full_parliamentarian = c.get_parliamentarian(parliamentarian['id'])
    for connection in tqdm(full_parliamentarian['connections'], leave=False, desc='Connections'):
        organisation = c.get_organisation(connection['to']['id'])
        for lobby_group in organisation['lobbyGroups']:
            Connection.insert((
                Model.global_id(organisation['id']),
                organisation['name'],
                connection['potency'],
                parliamentarian['id'],
                lobby_group['id'],
            ))


