from models.model import Model


class Organisation(Model):
    @classmethod
    def insert(cls, organisation):
        sql = """
        INSERT OR REPLACE INTO organisation(id, name) VALUES(?,?)
        """
        cur = cls.execute(sql, organisation)
        return cur.lastrowid

    @classmethod
    def get(cls, id):
        sql = """
        SELECT * FROM organisation where id=?
        """
        try:
            return cls.query(sql, (id,))[0]
        except IndexError:
            return None

    @classmethod
    def all(cls):
        sql = """
        SELECT * FROM organisation ORDER BY name ASC
        """
        return cls.query(sql)


Model.query(
    """
CREATE TABLE IF NOT EXISTS organisation (id integer PRIMARY KEY, name string)
"""
)
