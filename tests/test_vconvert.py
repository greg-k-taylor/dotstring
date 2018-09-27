import unittest
from vconvert import value_convert
from vconvert import to_int
from vconvert import to_float
# private methods
from vconvert.vconvert import key_value, set_key_value


class TestDrugbankUtils(unittest.TestCase):

    def test_key_value(self):
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
        print(res)
        self.assertEqual(res, "www.wiki.com")
        
    def test_set_key_value(self):
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

        res = set_key_value(d, "drugbank.pharmacology.xref.wikipedia", "www.myurl.com")
        print(res)
        self.assertEqual(res['drugbank']['pharmacology']['xref']['wikipedia'], "www.myurl.com")

    def test_value_convert(self):
        d = {
            'drugbank': {'id': '123'},
            'pharmgkb': {'id': '456'},
            'chebi': {'id': '789'}
            }
        res = value_convert(d, to_int,
                            include_keys=[
                                "drugbank.id",
                                "pharmgkb.id",
                                "chebi.id"
                                ])
        r = key_value(d, "drugbank.id")
        self.assertEquals(r, 123)
        r = key_value(d, "pharmgkb.id")
        self.assertEquals(r, 456)
        r = key_value(d, "chebi.id")
        self.assertEquals(r, 789)
