from models.model import Model


class Connection(Model):
    @classmethod
    def insert(cls, connection):
        sql = '''
        INSERT OR REPLACE INTO connection(id, name, potency, parliamentarian_id, lobby_group_id) VALUES(?,?,?,?,?)
        '''
        cur = cls.execute(sql, connection)
        return cur.lastrowid

    @classmethod
    def insert_many(cls, connections):
        sql = '''
        INSERT OR REPLACE INTO connection(id, name, potency, parliamentarian_id, lobby_group_id) VALUES(?,?,?,?,?)
        '''
        cur = cls.execute_many(sql, connections)
        return cur.lastrowid

    @classmethod
    def get(cls, id):
        sql = '''
        SELECT * FROM connection where id=?
        '''
        try:
            return cls.query(sql, (id,))[0]
        except IndexError:
            return None

    @classmethod
    def all(cls):
        sql = '''
        SELECT * FROM connection ORDER BY name ASC
        '''
        return cls.query(sql)


Model.query('''
CREATE TABLE IF NOT EXISTS connection
(id integer PRIMARY KEY, name string, potency string, parliamentarian_id integer, lobby_group_id integer)
''')
