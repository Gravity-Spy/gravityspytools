from types import SimpleNamespace
from unittest import mock

import pandas as pd
from django.test import SimpleTestCase, RequestFactory

import search.views as search_views


def _si_glitches():
    """A minimal, realistic similarity-search result so the searchlog DataFrame builds with real values."""
    return pd.DataFrame({
        'searchedID': ['abc123'],
        'searchedzooID': [123],
        'links_subjects': [456],
    })


class SearchlogNonFatalTests(SimpleTestCase):
    """Gate 1: a searchlog append failure must not 500 an already-created Zooniverse collection,
    while failures from create_collection itself must still propagate."""

    def setUp(self):
        self.rf = RequestFactory()

    def _post(self):
        request = self.rf.post('/search/do_collection_creation/', {})
        request.user = SimpleNamespace(username='tester')
        return request

    def _patches(self):
        """Common patches: valid form, similarity search, external collection, and DB engine.
        Zooniverse/Panoptes is never contacted because create_collection is fully mocked."""
        form = mock.patch.object(search_views, 'SearchForm')
        sim = mock.patch.object(search_views, 'similarity_search', return_value=_si_glitches())
        coll = mock.patch.object(search_views, 'create_collection', return_value='http://example/collection')
        engine = mock.patch.object(search_views, 'create_engine', return_value=mock.Mock())
        return form, sim, coll, engine

    def test_successful_append_retains_behavior(self):
        form, sim, coll, engine = self._patches()
        with form as Form, sim, coll as create_collection, engine, \
                mock.patch.object(pd.DataFrame, 'to_sql', return_value=None) as to_sql:
            Form.return_value.is_valid.return_value = True
            Form.return_value.cleaned_data = {'howmany': '5'}
            response = search_views.do_collection_creation(self._post())
        self.assertEqual(response.status_code, 200)
        to_sql.assert_called_once()
        create_collection.assert_called_once()

    def test_to_sql_failure_still_returns_success(self):
        from sqlalchemy.exc import ProgrammingError
        form, sim, coll, engine = self._patches()
        boom = ProgrammingError('INSERT INTO searchlog ...', {}, Exception('permission denied for table searchlog'))
        with form as Form, sim, coll as create_collection, engine, \
                mock.patch.object(pd.DataFrame, 'to_sql', side_effect=boom):
            Form.return_value.is_valid.return_value = True
            Form.return_value.cleaned_data = {'howmany': '5'}
            response = search_views.do_collection_creation(self._post())
        # Collection created once, response still rendered normally despite the logging failure.
        self.assertEqual(response.status_code, 200)
        create_collection.assert_called_once()

    def test_to_sql_failure_does_not_duplicate_collection(self):
        form, sim, coll, engine = self._patches()
        with form as Form, sim, coll as create_collection, engine, \
                mock.patch.object(pd.DataFrame, 'to_sql', side_effect=RuntimeError('boom')):
            Form.return_value.is_valid.return_value = True
            Form.return_value.cleaned_data = {'howmany': '5'}
            search_views.do_collection_creation(self._post())
        self.assertEqual(create_collection.call_count, 1)

    def test_create_collection_failure_propagates(self):
        form, sim, _coll, engine = self._patches()
        with form as Form, sim, \
                mock.patch.object(search_views, 'create_collection', side_effect=RuntimeError('panoptes down')), \
                engine, \
                mock.patch.object(pd.DataFrame, 'to_sql') as to_sql:
            Form.return_value.is_valid.return_value = True
            Form.return_value.cleaned_data = {'howmany': '5'}
            with self.assertRaises(RuntimeError):
                search_views.do_collection_creation(self._post())
        # A collection-creation failure must not be swallowed, and no searchlog write is attempted.
        to_sql.assert_not_called()

    def test_logging_failure_records_class_not_message(self):
        """The warning must identify the failure by exception class only, never the SQL/params
        (which carry the bound row values / user input)."""
        form, sim, coll, engine = self._patches()
        secret_sql = 'INSERT INTO searchlog ... [parameters: user=tester returned_ids=456]'
        with form as Form, sim, coll, engine, \
                mock.patch.object(pd.DataFrame, 'to_sql', side_effect=ValueError(secret_sql)), \
                mock.patch.object(search_views.logger, 'warning') as warn:
            Form.return_value.is_valid.return_value = True
            Form.return_value.cleaned_data = {'howmany': '5'}
            search_views.do_collection_creation(self._post())
        warn.assert_called_once()
        # call_args.args/.kwargs accessors are Python 3.8+; on the deployed Python 3.6 they resolve
        # to a chained mock, not the call arguments. Unpack the call tuple and render with logging
        # %-semantics instead of stringifying the mock call object.
        call_args, call_kwargs = warn.call_args
        fmt = call_args[0]
        fmt_args = tuple(call_args[1:])
        rendered = fmt % fmt_args
        self.assertEqual(fmt_args, ('ValueError',))   # ONLY the exception class is passed to the logger
        self.assertEqual(call_kwargs, {})             # no keyword args carrying data
        self.assertIn('ValueError', rendered)         # class name is present
        self.assertNotIn(secret_sql, rendered)        # original exception message absent
        self.assertNotIn(secret_sql, fmt)             # not hidden in the format string either
        self.assertNotIn('parameters', rendered)      # SQL parameters marker absent
        self.assertNotIn('returned_ids', rendered)    # bound row values absent
