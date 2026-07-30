# Tables the similarity search is allowed to query. Request-supplied table
# names are interpolated into SQL, so they must be checked against this list.
SUPPORTED_SCIENCE_TABLES = frozenset({'similarity_index_o3'})


class UnsupportedScienceTable(ValueError):
    pass


def is_supported_science_table(table):
    return table in SUPPORTED_SCIENCE_TABLES


def validate_science_table(table):
    if not is_supported_science_table(table):
        raise UnsupportedScienceTable('Unsupported similarity table selection.')
    return table
