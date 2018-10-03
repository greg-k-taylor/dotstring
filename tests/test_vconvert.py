from copy import deepcopy
import unittest
from vconvert import value_convert
from vconvert import int_convert
from vconvert import unlist
# private methods
from vconvert.vconvert import key_value
from vconvert.vconvert import set_key_value
from vconvert.vconvert import last_element
from vconvert.vconvert import traverse_keys


class TestDrugbankUtils(unittest.TestCase):

    def test_key_value(self):

        # test small document
        d = {
            'field': 'value'
            }
        res = key_value(d, 'field')
        self.assertEqual(list(res), ['value'])

        d = {
            'drugbank': {
                'pharmacology': {
                    'actions': '123',
                    'xref': {
                        'wikipedia': 'www.wiki.com'
                        }
                    }
                }
            }
        res = key_value(d, "drugbank.pharmacology.xref.wikipedia")
        self.assertEqual(list(res), ["www.wiki.com"])

        res = key_value(d, "drugbank.udef_field.xref")
        self.assertEqual(list(res), [])
        
    def test_set_key_value(self):

        # test small document
        d = {
            'field': 'value'
            }
        res = set_key_value(d, 'field', 'new-value')
        self.assertEqual(res['field'], 'new-value')

        # test nested document
        d = {
            'drugbank': {
                'pharmacology': {
                    'actions': '123',
                    'xref': {
                        'wikipedia': 'www.wiki.com'
                        }
                    }
                }
            }

        # test where field is present
        res = set_key_value(d, "drugbank.pharmacology.xref.wikipedia", "www.myurl.com")
        self.assertEqual(res['drugbank']['pharmacology']['xref']['wikipedia'], "www.myurl.com")

        # test where field is not present
        res = set_key_value(d, "drugbank.pharmacology.xref-invalid.wikipedia", "www.wiki.com")
        self.assertEqual(res['drugbank']['pharmacology']['xref']['wikipedia'], "www.myurl.com")

        # test invalid input cases
        with self.assertRaises(TypeError):
            res = set_key_value(d, None, "www.myurl.com")

    def test_last_element(self):
        d = {
            'drugbank': {
                'measurement': [
                    {'pH': '6'},
                    {'pH': '7.5'},
                    {'pH': '8'},
                    ]
                }
            }
        key_list = ["drugbank", "measurement", "pH"]
        res = []
        for k, le in last_element(d, key_list):
            res.append(le[k])
        self.assertEqual(res, ['6', '7.5', '8'])

    def test_value_convert(self):
        d = {
            'drugbank': {'id': '123'},
            'pharmgkb': {'id': '456'},
            'chebi': {'id': '789'},
            'other': {'id': '9'}
            }
        res = int_convert(d,
                          include_keys=[
                                "drugbank.id",
                                "pharmgkb.id",
                                "chebi.id"
                                ])
        r = key_value(d, "drugbank.id")
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
            'drugbank': {
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
                          ["drugbank.pharmacology.actions",
                           "drugbank.pharmacology.xref.wikipedia"])

    def test_unlist(self):
        # test simple document
        d = {
            'lst': ['123']
            }
        res = unlist(d, [], [])
        self.assertEquals(res['lst'], '123')

        # test nested document
        input = {
            'drugbank': {
                'pharmacology': {
                    'actions': ['123'],
                    'xref': {
                        'wikipedia': 'www.wiki.com'
                        }
                    }
                }
            }
        # default args
        d = deepcopy(input)
        res = unlist(d, [], [])
        self.assertEquals(res['drugbank']['pharmacology']['actions'], '123')

        # include_keys
        d = deepcopy(input)
        res = unlist(d, ['drugbank.pharmacology.actions'], [])
        self.assertEquals(res['drugbank']['pharmacology']['actions'], '123')

        # exclude_keys
        d = deepcopy(input)
        res = unlist(d, [], ['drugbank.pharmacology.actions'])
        self.assertEquals(res['drugbank']['pharmacology']['actions'], ['123'])
