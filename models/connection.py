from normalisation_map import normalize_organisation
from models.model import Model


class Connection(Model):
    @classmethod
    def insert(cls, connection):
        sql = """
        INSERT OR REPLACE INTO connection(potency, parliamentarian_id, organisation_id, sector_id) VALUES(?,?,?,?)
        """
        cur = cls.execute(sql, connection)
        return cur.lastrowid

    @classmethod
    def get(cls, id):
        sql = """
        SELECT * FROM connection where id=?
        """
        try:
            return cls.query(sql, (id,))[0]
        except IndexError:
            return None

    @classmethod
    def all(cls):
        sql = """
        SELECT * FROM connection
        """
        return cls.query(sql)

    @classmethod
    def normalize_organisation(cls, source):
        target = normalize_organisation(source)
        sql = """
        UPDATE connection set organisation_id=? where organisation_id=?
        """
        cur = cls.execute(sql, (target, source))
        return cur.lastrowid


Model.query(
    """
CREATE TABLE IF NOT EXISTS connection
(potency integer, parliamentarian_id integer, organisation_id integer, sector_id integer)
"""
)
