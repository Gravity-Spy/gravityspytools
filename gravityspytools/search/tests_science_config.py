import os
import unittest

from gravityspytools.dbconfig import science_db_host, PROD_SCIENCE_DB_HOST
from search.science_tables import (
    validate_science_table,
    is_supported_science_table,
    UnsupportedScienceTable,
)

ENV = 'GRAVITYSPY_SCIENCE_DB_HOST'
DEV_HOST = 'gravityspyplus-dev.ciera.northwestern.edu'


class ScienceDBHostTests(unittest.TestCase):
    def setUp(self):
        self._saved = os.environ.pop(ENV, None)

    def tearDown(self):
        os.environ.pop(ENV, None)
        if self._saved is not None:
            os.environ[ENV] = self._saved

    def test_defaults_to_production_host(self):
        self.assertEqual(science_db_host(), 'gravityspyplus.ciera.northwestern.edu')
        self.assertEqual(science_db_host(), PROD_SCIENCE_DB_HOST)

    def test_environment_override_to_dev_host(self):
        os.environ[ENV] = DEV_HOST
        self.assertEqual(science_db_host(), DEV_HOST)


class ScienceTableValidationTests(unittest.TestCase):
    def test_valid_similarity_index_o3(self):
        self.assertTrue(is_supported_science_table('similarity_index_o3'))
        self.assertEqual(validate_science_table('similarity_index_o3'), 'similarity_index_o3')

    def test_missing_database(self):
        self.assertFalse(is_supported_science_table(None))
        with self.assertRaises(UnsupportedScienceTable):
            validate_science_table(None)

    def test_invalid_table_name(self):
        self.assertFalse(is_supported_science_table('similarityindex'))
        with self.assertRaises(UnsupportedScienceTable):
            validate_science_table('glitches; DROP TABLE glitches')


if __name__ == '__main__':
    unittest.main()
