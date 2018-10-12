# dotstring v0.1.1

Consider the following python nested object:

```python
self.nested = {
    'drugdb': {
        'pharmacology': {
            'id_lst': ['123'],
            'actions': 'cure'
            'xref': {
                'wikipedia': 'www.wiki.com'
            }
        }
    }
}
```

Now, suppose that we want to act on the wikipedia field.  Then, using
this utility module, we could call a helper function with the argument
`drugdb.pharmacology.xref.wikipedia`.  This would act on the nested
wikipedia field.  I can this dotation a "dot-string".

# Supported Utility Functions using Dot-Strings

`remove_key` - remove a field in a document for a "dot-string".
If removal is not possible then no action is taken.

`float_convert` - convert a field to a float (if possible) for a "dot-string".
If conversion is not possible then no action is taken.

`int_convert` - convert a field to an int (if possible) for a "dot-string".
If conversion is not possible then no action is taken.

`value_convert` - convert a field using the specified function (if possible) for a "dot-string".
If conversion is not possible then no action is taken.

`unlist` - convert a list field with one element to that element for a "dot-string".
If conversion is not possible then no action is taken.
