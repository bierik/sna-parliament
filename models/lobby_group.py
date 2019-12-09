from models.model import Model


class LobbyGroup(Model):
    def insert(self, lobby_group):
        sql = '''
        INSERT INTO lobby_group(id, name, connection_id) VALUES(?,?,?)
        '''
        cur = self.query(sql)
        return cur.lastrowid


Model.query('''
CREATE TABLE IF NOT EXISTS lobby_group
(id string PRIMARY KEY, name string, connection_id string)
''')
