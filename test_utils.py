import unittest
from utils import key_value, set_key_value


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
