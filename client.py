from graphqlclient import GraphQLClient
from operator import itemgetter
import json


class Client:

    organisation_cache = {}

    def __init__(self, url='http://lobbywatch.ch/graphql', locale='de'):
        self.client = GraphQLClient(url)
        self.locale = locale

    def _build_function_params(self, params):
        return ', '.join(
            map(
                lambda param: ':'.join(
                    map(
                        lambda x: str(x),
                        param
                    )
                ),
                params.items(),
            )
        )

    def query(self, function, body, **kwargs):
        kwargs.update({'locale': 'de'})
        params = self._build_function_params(kwargs)
        query = '''
        {
            %s(%s) {
                %s
            }
        }
        ''' % (function, params, body)
        return self._query(query).get(function)

    def _query(self, query):
        return json.loads(self.client.execute(query))['data']

    def get_parliamentarians(self):
        body = '''
        id
        '''
        return self.query('parliamentarians', body)

    def get_parliamentarian(self, id):
        body = '''
        id
        connections {
            potency
            to {
                ... on Organisation {
                    id
                }
            }
        }
        '''
        return self.query('getParliamentarian', body, id=id)

    def get_organisation_connections_of_parliamentarian(self, id):
        def create_connection_dict(connection):
            return {
                'id': connection['to']['id'],
                'potency': connection['potency'],
            }

        return map(
            create_connection_dict,
            self.get_parliamentarian(id)['connections'],
        )

    def get_organisation(self, id):
        body = '''
        id
        name
        description
        lobbyGroups {
            name
        }
        '''
        return self.query('getOrganisation', body, id=id)

    def get_lobby_groups_from_organisation(self, id):
        return map(
            itemgetter('name'),
            self.get_organisation(id)['lobbyGroups']
        )

    def get_lobby_groups(self):
        body = '''
        name
        sector
        '''
        return self.query('lobbyGroups', body)
