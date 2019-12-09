from models.model import Model


class Connection(Model):
    @classmethod
    def insert(cls, connection):
        sql = '''
        INSERT INTO connection(id, name, potency, parliamentarian_id)
            VALUES(?,?,?,?)
        '''
        cur = cls.query(sql, connection)
        return cur.lastrowid


Model.query('''
CREATE TABLE IF NOT EXISTS connection
(id string PRIMARY KEY, name string, potency string, parliamentarian_id string)
''')
