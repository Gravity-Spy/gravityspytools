import os
import unittest

from gravityspytools.dbconfig import require_env, DatabaseConfigError

CANON = 'GRAVITYSPYTOOLS_TEST_CANON'
LEGACY = 'GRAVITYSPYTOOLS_TEST_LEGACY'


class RequireEnvTests(unittest.TestCase):
    def setUp(self):
        for name in (CANON, LEGACY):
            os.environ.pop(name, None)

    def tearDown(self):
        for name in (CANON, LEGACY):
            os.environ.pop(name, None)

    def test_canonical_present(self):
        os.environ[CANON] = 'canon-value'
        self.assertEqual(require_env(CANON, legacy=[LEGACY]), 'canon-value')

    def test_legacy_fallback_present(self):
        os.environ[LEGACY] = 'legacy-value'
        self.assertEqual(require_env(CANON, legacy=[LEGACY]), 'legacy-value')

    def test_canonical_takes_precedence_over_legacy(self):
        os.environ[CANON] = 'canon-value'
        os.environ[LEGACY] = 'legacy-value'
        self.assertEqual(require_env(CANON, legacy=[LEGACY]), 'canon-value')

    def test_empty_canonical_falls_back_to_legacy(self):
        os.environ[CANON] = ''
        os.environ[LEGACY] = 'legacy-value'
        self.assertEqual(require_env(CANON, legacy=[LEGACY]), 'legacy-value')

    def test_default_used_when_all_missing(self):
        self.assertEqual(require_env(CANON, legacy=[LEGACY], default='5432'), '5432')

    def test_missing_required_raises_clear_error(self):
        with self.assertRaises(DatabaseConfigError) as ctx:
            require_env(CANON, legacy=[LEGACY])
        self.assertIn(CANON, str(ctx.exception))

    def test_error_message_contains_no_secret_value(self):
        os.environ[CANON] = ''
        os.environ[LEGACY] = ''
        secret = 'p@ssw0rd-should-not-appear'
        os.environ['GRAVITYSPYTOOLS_TEST_DECOY'] = secret
        try:
            with self.assertRaises(DatabaseConfigError) as ctx:
                require_env(CANON, legacy=[LEGACY])
            self.assertNotIn(secret, str(ctx.exception))
            self.assertIn(CANON, str(ctx.exception))
        finally:
            os.environ.pop('GRAVITYSPYTOOLS_TEST_DECOY', None)


if __name__ == '__main__':
    unittest.main()
