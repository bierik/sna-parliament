from models.model import Model


class Connection(Model):
    @classmethod
    def insert(cls, connection):
        sql = '''
        INSERT OR REPLACE INTO connection(potency, parliamentarian_id, organisation_id, sector_id) VALUES(?,?,?,?)
        '''
        cur = cls.execute(sql, connection)
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
        SELECT * FROM connection
        '''
        return cls.query(sql)


Model.query('''
CREATE TABLE IF NOT EXISTS connection
(potency integer, parliamentarian_id integer, organisation_id integer, sector_id integer)
''')
