from models.model import Model


class Parliamentarian(Model):
    @classmethod
    def insert(cls, parliamentarian):
        sql = '''
        INSERT OR REPLACE INTO parliamentarian(id, name) VALUES(?,?)
        '''
        cur = cls.execute(sql, parliamentarian)
        return cur.lastrowid

    @classmethod
    def insert_many(cls, parliamentarians):
        sql = '''
        INSERT OR REPLACE INTO parliamentarian(id, name) VALUES(?,?)
        '''
        cur = cls.execute_many(sql, parliamentarians)
        return cur.lastrowid

    @classmethod
    def get(cls, id):
        sql = '''
        select * from parliamentarian where id=?
        '''
        try:
            return cls.query(sql, (id,))[0]
        except IndexError:
            return None

    @classmethod
    def all(cls):
        sql = '''
        select * from parliamentarian
        '''
        return cls.query(sql)


Model.query('CREATE TABLE IF NOT EXISTS parliamentarian (id integer PRIMARY KEY, name string)')
