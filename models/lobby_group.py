from models.model import Model


class LobbyGroup(Model):

    @classmethod
    def insert(cls, lobby_group):
        sql = '''
        INSERT OR REPLACE INTO lobby_group(id, name, sector) VALUES(?,?,?)
        '''
        cur = cls.execute(sql, lobby_group)
        return cur.lastrowid

    @classmethod
    def insert_many(cls, lobby_groups):
        sql = '''
        INSERT OR REPLACE INTO lobby_group(id, name, sector) VALUES(?,?,?)
        '''
        cur = cls.execute_many(sql, lobby_groups)
        return cur.lastrowid

    @classmethod
    def get(cls, id):
        sql = '''
        select * from lobby_group where id=?
        '''
        try:
            return cls.query(sql, (id,))[0]
        except IndexError:
            return None

    @classmethod
    def all(cls):
        sql = '''
        select * from lobby_group
        '''
        return cls.query(sql)


Model.query('''
CREATE TABLE IF NOT EXISTS lobby_group
(id integer PRIMARY KEY, name string, sector string)
''')
