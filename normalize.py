from models.connection import Connection
from normalisation_map import get_organisations_to_normalize


def normalize():
    records_to_normalize = get_organisations_to_normalize()
    for record in records_to_normalize:
        Connection.normalize_organisation(record)
