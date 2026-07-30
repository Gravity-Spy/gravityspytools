from unittest import mock

from django.test import SimpleTestCase, RequestFactory

import search.views as search_views
import collectioninfo.views as collectioninfo_views
import display_glitches_DB.views as db_views


class InvalidFormResponseTests(SimpleTestCase):
    """Invalid form input must yield a controlled response, never a 500 fall-through."""

    def setUp(self):
        self.rf = RequestFactory()

    def test_daterange_invalid_returns_400(self):
        response = search_views.daterange(self.rf.get('/daterange', {}))
        self.assertEqual(response.status_code, 400)

    def test_dategraph_invalid_returns_400(self):
        response = collectioninfo_views.dategraph(self.rf.get('/collection-info/dategraph', {}))
        self.assertEqual(response.status_code, 400)

    def test_do_DB_search_invalid_is_not_server_error(self):
        response = db_views.do_DB_search(self.rf.get('/display-glitches-db', {}))
        self.assertIsNotNone(response)
        self.assertLess(response.status_code, 500)

    def test_daterange_valid_still_returns_png(self):
        with mock.patch.object(search_views, 'SearchForm') as Form, \
                mock.patch.object(search_views, 'similarity_search'), \
                mock.patch.object(search_views, 'obtain_figure'), \
                mock.patch.object(search_views, 'FigureCanvas'):
            Form.return_value.is_valid.return_value = True
            response = search_views.daterange(self.rf.get('/daterange', {}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'image/png')

    def test_do_DB_search_valid_still_renders_results(self):
        with mock.patch.object(db_views, 'SearchDBForm') as Form, \
                mock.patch.object(db_views, 'searchDB') as searchDB:
            Form.return_value.is_valid.return_value = True
            searchDB.return_value.to_dict.return_value = []
            response = db_views.do_DB_search(self.rf.get('/display-glitches-db', {}))
        self.assertEqual(response.status_code, 200)
