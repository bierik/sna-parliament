from models.model import Model


class Parliamentarian(Model):
    @classmethod
    def insert(cls, parliamentarian):
        sql = '''
        INSERT INTO parliamentarian(id, name) VALUES(?,?)
        '''
        cur = cls.query(sql, parliamentarian)
        return cur.lastrowid


Model.query('CREATE TABLE IF NOT EXISTS parliamentarian (id string PRIMARY KEY, name string)')
