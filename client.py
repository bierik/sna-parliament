from graphqlclient import GraphQLClient
import json


class Client:

    cache = {
        "organisation": {},
    }

    def __init__(self, url="http://lobbywatch.ch/graphql", locale="de"):
        self.client = GraphQLClient(url)
        self.locale = locale

    def _build_function_params(self, params):
        return ", ".join(
            map(lambda param: ":".join(map(lambda x: str(x), param)), params.items(),)
        )

    def query(self, function, body, **kwargs):
        kwargs.update({"locale": "de"})
        params = self._build_function_params(kwargs)
        query = """
        {
            %s(%s) {
                %s
            }
        }
        """ % (
            function,
            params,
            body,
        )
        return self._query(query).get(function)

    def _query(self, query):
        return json.loads(self.client.execute(query))["data"]

    def get_parliamentarians(self):
        body = """
        id
        name
        """
        return self.query("parliamentarians", body)

    def get_parliamentarian(self, id):
        body = """
        id
        name
        connections {
            potency
            to {
                ... on Organisation {
                    id
                    name
                }
            }
        }
        """
        return self.query("getParliamentarian", body, id=f'"{id}"')

    def get_organisation(self, id):
        if self.cache["organisation"].get(id):
            return self.cache["organisation"].get(id)
        body = """
        id
        name
        lobbyGroups {
            id
        }
        """
        organisation = self.query("getOrganisation", body, id=f'"{id}"')
        self.cache["organisation"][id] = organisation
        return organisation

    def get_lobby_groups(self):
        body = """
        id
        name
        sector
        """
        return self.query("lobbyGroups", body)
