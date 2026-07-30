import os
import unittest

from gravityspytools.dbconfig import allowed_hosts, DEFAULT_ALLOWED_HOSTS

ENV = 'GRAVITYSPY_ALLOWED_HOSTS'


class AllowedHostsTests(unittest.TestCase):
    def setUp(self):
        self._saved = os.environ.pop(ENV, None)

    def tearDown(self):
        os.environ.pop(ENV, None)
        if self._saved is not None:
            os.environ[ENV] = self._saved

    def test_default_when_unset(self):
        self.assertEqual(allowed_hosts(), DEFAULT_ALLOWED_HOSTS)

    def test_default_when_empty(self):
        os.environ[ENV] = ''
        self.assertEqual(allowed_hosts(), DEFAULT_ALLOWED_HOSTS)

    def test_comma_separated_override(self):
        os.environ[ENV] = 'gravityspytools-dev.ciera.northwestern.edu,gravityspytools.ciera.northwestern.edu,localhost,127.0.0.1'
        self.assertEqual(
            allowed_hosts(),
            ['gravityspytools-dev.ciera.northwestern.edu', 'gravityspytools.ciera.northwestern.edu', 'localhost', '127.0.0.1'],
        )

    def test_whitespace_trimmed(self):
        os.environ[ENV] = ' a.example ,  b.example ,c.example '
        self.assertEqual(allowed_hosts(), ['a.example', 'b.example', 'c.example'])

    def test_empty_entries_ignored(self):
        os.environ[ENV] = 'a.example,,b.example, ,'
        self.assertEqual(allowed_hosts(), ['a.example', 'b.example'])


if __name__ == '__main__':
    unittest.main()
