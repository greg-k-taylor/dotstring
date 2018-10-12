from copy import deepcopy
import unittest
from dotstring import value_convert
from dotstring import int_convert
from dotstring import unlist
# private methods
from dotstring.dotstring import key_value
from dotstring.dotstring import set_key_value
from dotstring.dotstring import last_element
from dotstring.dotstring import remove_key
from dotstring.dotstring import traverse_keys


class TestDotString(unittest.TestCase):

    def setUp(self):
        # test simple document
        self.simple = {
            'field': 'value'
            }
        # test simple list document
        self.simple_lst = {
            'lst': ['123']
            }
        # test nested document
        self.nested = {
            'drugdb': {
                'pharmacology': {
                    'actions': ['123'],
                    'xref': {
                        'wikipedia': 'www.wiki.com'
                        }
                    }
                }
            }

    def test_key_value(self):

        # test small document
        d = deepcopy(self.simple)
        res = key_value(d, 'field')
        self.assertEqual(list(res), ['value'])

        # test nested document
        d = deepcopy(self.nested)
        res = key_value(d, "drugdb.pharmacology.xref.wikipedia")
        self.assertEqual(list(res), ["www.wiki.com"])

        res = key_value(d, "drugdb.udef_field.xref")
        self.assertEqual(list(res), [])
        
    def test_set_key_value(self):

        # test small document
        d = deepcopy(self.simple)
        res = set_key_value(d, 'field', 'new-value')
        self.assertEqual(res['field'], 'new-value')

        # test nested document
        d = deepcopy(self.nested)

        # test where field is present
        res = set_key_value(d, "drugdb.pharmacology.xref.wikipedia", "www.myurl.com")
        self.assertEqual(res['drugdb']['pharmacology']['xref']['wikipedia'], "www.myurl.com")

        # test where field is not present
        res = set_key_value(d, "drugdb.pharmacology.xref-invalid.wikipedia", "www.wiki.com")
        self.assertEqual(res['drugdb']['pharmacology']['xref']['wikipedia'], "www.myurl.com")

        # test invalid input cases
        with self.assertRaises(TypeError):
            res = set_key_value(d, None, "www.myurl.com")

    def test_last_element(self):
        d = {
            'drugdb': {
                'measurement': [
                    {'pH': '6'},
                    {'pH': '7.5'},
                    {'pH': '8'},
                    ]
                }
            }
        key_list = ["drugdb", "measurement", "pH"]
        res = []
        for k, le in last_element(d, key_list):
            res.append(le[k])
        self.assertEqual(res, ['6', '7.5', '8'])

    def test_value_convert(self):
        d = {
            'drugdb': {'id': '123'},
            'pharmgkb': {'id': '456'},
            'chebi': {'id': '789'},
            'other': {'id': '9'}
            }
        res = int_convert(d,
                          include_keys=[
                                "drugdb.id",
                                "pharmgkb.id",
                                "chebi.id"
                                ])
        r = key_value(d, "drugdb.id")
        self.assertEquals(list(r), [123])
        r = key_value(d, "pharmgkb.id")
        self.assertEquals(list(r), [456])
        r = key_value(d, "chebi.id")
        self.assertEquals(list(r), [789])

        # not-converted
        r = key_value(d, "other.id")
        self.assertEquals(list(r), ['9'])

    def test_traverse_keys(self):
        # test nested document
        d = {
            'drugdb': {
                'pharmacology': {
                    'actions': '123',
                    'xref': {
                        'wikipedia': 'www.wiki.com'
                        }
                    }
                }
            }
        res = []
        for k, elem in traverse_keys(d, [], []):
            res.append(k)

        self.assertEquals(res,
                          ["drugdb.pharmacology.actions",
                           "drugdb.pharmacology.xref.wikipedia"])

    def test_unlist(self):
        # test simple document
        d = deepcopy(self.simple_lst)
        res = unlist(d, [], [])
        self.assertEquals(res['lst'], '123')

        # default args
        d = deepcopy(self.nested)
        res = unlist(d, [], [])
        self.assertEquals(res['drugdb']['pharmacology']['actions'], '123')

        # include_keys
        d = deepcopy(self.nested)
        res = unlist(d, ['drugdb.pharmacology.actions'], [])
        self.assertEquals(res['drugdb']['pharmacology']['actions'], '123')

        # exclude_keys
        d = deepcopy(self.nested)
        res = unlist(d, [], ['drugdb.pharmacology.actions'])
        self.assertEquals(res['drugdb']['pharmacology']['actions'], ['123'])

    def test_remove_key(self):
        # default args
        d = deepcopy(self.simple_lst)
        res = remove_key(d, "lst")
        self.assertEquals(res, {})

        # nested doc
        d = deepcopy(self.nested)
        res = remove_key(d, "drugdb.pharmacology.actions")
        self.assertTrue('actions' not in res['drugdb']['pharmacology'].keys())
