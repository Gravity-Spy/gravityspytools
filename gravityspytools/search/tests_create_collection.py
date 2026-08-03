from datetime import datetime
from types import SimpleNamespace
from unittest import mock

import pandas as pd
from django.test import SimpleTestCase, RequestFactory

import search.utils as search_utils
import search.views as search_views


def _si_glitches():
    """A minimal, realistic similarity-search result: one non-sentinel subject to collect."""
    return pd.DataFrame({
        'searchedID': ['abc123'],
        'searchedzooID': [123],
        'links_subjects': [456],
    })


class CreateCollectionPanoptesTests(SimpleTestCase):
    """create_collection uses panoptes-client's context manager (`with panoptes_client.Panoptes()
    as client:`), which panoptes-client 1.1.1 supports with thread-local client state so concurrent
    requests do not overwrite one another's OAuth client. These tests exercise the real
    create_collection with panoptes_client fully mocked, verifying that the context manager is
    entered and exited, the request-scoped bearer token / expiry / logged_in flag are assigned to
    the client bound by __enter__, and the collection is created, project-linked, saved, populated,
    and its URL returned entirely inside the context. Every Panoptes/Zooniverse call is mocked and
    check_token is patched, so no network access can occur."""

    def _request(self):
        # check_token is patched out, so the session only needs the values create_collection reads.
        return SimpleNamespace(session={'access_token': 'tok-xyz', 'expires_in': 3600})

    def _run(self):
        events = []

        def _rec(name, retval):
            def _side_effect(*args, **kwargs):
                events.append(name)
                return retval
            return _side_effect

        # cm is the object returned by Panoptes(); `as client` binds cm.__enter__()'s return value.
        client = mock.MagicMock(name='client')
        cm = mock.MagicMock(name='panoptes_cm')
        cm.__enter__.side_effect = _rec('enter', client)
        cm.__exit__.side_effect = _rec('exit', False)

        fake_collection = mock.MagicMock(name='collection')
        fake_collection.save.side_effect = _rec(
            'save', {'collections': [{'slug': 'tester/similar-collection'}]})
        fake_collection.add.side_effect = _rec('add', None)
        fake_collection.set_default_subject.side_effect = _rec('set_default', None)

        panoptes = mock.MagicMock(name='panoptes_client')
        panoptes.Panoptes.return_value = cm
        panoptes.Collection.side_effect = _rec('Collection', fake_collection)

        with mock.patch.object(search_utils, 'panoptes_client', panoptes), \
                mock.patch.object(search_utils, 'check_token', side_effect=lambda r: r):
            url = search_utils.create_collection(self._request(), _si_glitches())

        return SimpleNamespace(
            url=url, client=client, cm=cm, collection=fake_collection,
            panoptes=panoptes, events=events,
        )

    def test_context_manager_entered_and_exited(self):
        r = self._run()
        r.panoptes.Panoptes.assert_called_once_with()   # plain construction, used as a context manager
        r.cm.__enter__.assert_called_once()
        r.cm.__exit__.assert_called_once()

    def test_bearer_credentials_assigned_to_context_client(self):
        r = self._run()
        # The client bound by `as client` (i.e. __enter__'s return) receives the session credentials.
        self.assertEqual(r.client.bearer_token, 'tok-xyz')
        self.assertTrue(r.client.logged_in)
        self.assertIsInstance(r.client.bearer_expires, datetime)

    def test_collection_built_and_saved_inside_context(self):
        r = self._run()
        r.panoptes.Collection.assert_called_once_with()
        self.assertEqual(r.collection.links.project, '1104')       # project linking
        r.collection.save.assert_called_once_with()
        r.collection.add.assert_called_once_with([456])            # subjects added
        r.collection.set_default_subject.assert_called_once_with(123)
        # All operations occur between __enter__ and __exit__, in order.
        self.assertEqual(
            r.events, ['enter', 'Collection', 'save', 'add', 'set_default', 'exit'])

    def test_returns_expected_collection_url(self):
        r = self._run()
        self.assertEqual(
            r.url,
            'https://www.zooniverse.org/projects/zooniverse/gravity-spy/collections/tester/similar-collection',
        )


class DoCollectionCreationMethodTests(SimpleTestCase):
    """A non-POST request to do_collection_creation must return a real response (405 Method Not
    Allowed), never fall through and return None (which Django rejects with 'didn't return an
    HttpResponse object')."""

    def setUp(self):
        self.rf = RequestFactory()

    def test_get_returns_405_not_none(self):
        response = search_views.do_collection_creation(
            self.rf.get('/search/do_collection_creation/')
        )
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 405)
