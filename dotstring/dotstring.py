from dotstring.type import is_str
from dotstring.type import to_float
from dotstring.type import to_int


def last_element(d, key_list):
    """Return the last element and key for a document d given a docstring.

    A document d is passed with a list of keys key_list.  A generator is then
    returned for all elements that match all keys.  Not that there may be 
    a 1-to-many relationship between keys and elements due to lists in the document.

    :param d: document d to return elements from
    :param key_list: list of keys that specify elements in the document d
    :return: generator for elements that match all keys
    """
    # preconditions
    if not d or not key_list:
        return
    k = key_list.pop(0)
    # termination
    if not key_list:
        yield k, d
    # recursion
    else:
        try:
            t = d[k]
        except KeyError:
            return # key does not exist
        except TypeError:
            return # not sub-scriptable
        if isinstance(t, dict):                
            yield from last_element(t, key_list)
        elif isinstance(t, list):
            for l in t:
                yield from last_element(l, key_list.copy())
        elif isinstance(t, tuple):
            # unsupported type
            raise ValueError("unsupported type in key {}".format(k))
    
def key_value(dictionary, key):
    """Return a generator for all values in a dictionary specific by a dotstirng (key)

    :param dictionary: a dictionary to return values from
    :param key: key that specifies a value in the dictionary
    :return: generator for values that match the given key
    """
    def safe_ref(k, d):
        if d:
            try:
                return d[k]
            except KeyError:
                pass

    if not is_str(key):
        raise TypeError("key argument must of be of type 'str'")
    key_list = key.split('.')
    for k, le in last_element(dictionary, key_list):
        yield safe_ref(k, le)

def set_key_value(dictionary, key, value):
    """Set values all values in dictionary matching a dotstring key to a specified value.

    :param dictionary: a dictionary to set values in
    :param key: key that specifies an element in the dictionary
    :return: dictionary after changes have been made
    """
    def safe_assign(k, d):
        if d:
            try:
                d[k] = value
            except KeyError:
                pass

    if not is_str(key):
        raise TypeError("key argument must of be of type 'str'")
    key_list = key.split('.')
    for k, le in last_element(dictionary, key_list):
        safe_assign(k, le)
    return dictionary

def remove_key(dictionary, key):
    """Remove field specified by the docstring key

    :param dictionary: a dictionary to remove the value from
    :param key: key that specifies an element in the dictionary
    :return: dictionary after changes have been made
    """
    if not is_str(key):
        raise TypeError("key argument must of be of type 'str'")
    key_list = key.split('.')
    for k, le in last_element(dictionary, key_list):
        try:
            del le[k]
        except KeyError:
            pass
    return dictionary

def traverse_keys(d, include_keys=[], exclude_keys=[]):
    """Return all key, value pairs for a document.

    By default, traverse all keys
    If include_keys is specified, only traverse the list from include_kes a.b, a.b.c
    If exclude_keys is specified, only exclude the list from exclude_keys

    :param d: a dictionary to traverse keys on
    :param include_keys: only traverse these keys (optional)
    :param exclude_keys: exclude all other keys except these keys (optional)
    :return: generate key, value pairs
    """
    def traverse_helper(d, keys):
        if isinstance(d, dict):
            for k in d.keys():
                yield from traverse_helper(d[k], keys + [k])
        elif isinstance(d, list):
            for i in d:
                yield from traverse_helper(i, keys)
        else:
            yield keys, d

    if include_keys:
        for k in include_keys:
            for val in key_value(d, k):
                yield k, val
    else:
        for kl, val in traverse_helper(d, []):
            key = '.'.join(kl)
            if key not in exclude_keys:
                yield key, val

def value_convert(d, fn, include_keys=[], exclude_keys=[]):
    """Convert elements in a document using a function fn.

    By default, traverse all keys
    If include_keys is specified, only convert the list from include_keys a.b, a.b.c
    If exclude_keys is specified, only exclude the list from exclude_keys

    :param d: a dictionary to traverse keys on
    :param fn: function to convert elements with
    :param include_keys: only convert these keys (optional)
    :param exclude_keys: exclude all other keys except these keys (optional)
    :return: generate key, value pairs
    """
    for path, value in traverse_keys(d, include_keys, exclude_keys):
        new_value = fn(value)
        set_key_value(d, path, new_value)
    return d

def int_convert(d, include_keys=[], exclude_keys=[]):
    """Convert elements in a document to integers.

    By default, traverse all keys
    If include_keys is specified, only convert the list from include_keys a.b, a.b.c
    If exclude_keys is specified, only exclude the list from exclude_keys

    :param d: a dictionary to traverse keys on
    :param include_keys: only convert these keys (optional)
    :param exclude_keys: exclude all other keys except these keys (optional)
    :return: generate key, value pairs
    """
    return value_convert(d, to_int, include_keys, exclude_keys)

def float_convert(d, include_keys=[], exclude_keys=[]):
    """Convert elements in a document to floats.

    By default, traverse all keys
    If include_keys is specified, only convert the list from include_keys a.b, a.b.c
    If exclude_keys is specified, only exclude the list from exclude_keys

    :param d: a dictionary to traverse keys on
    :param include_keys: only convert these keys (optional)
    :param exclude_keys: exclude all other keys except these keys (optional)
    :return: generate key, value pairs
    """
    return value_convert(d, to_float, include_keys, exclude_keys)

def unlist(d, include_keys=[], exclude_keys=[]):
    """Unlist elements in a document.

    If there is 1 value in the list, set the element to that value.  Otherwise,
    leave the list unchanged.

    By default, traverse all keys
    If include_keys is specified, only traverse the list from include_keys a.b, a.b.c
    If exclude_keys is specified, only exclude the list from exclude_keys

    :param d: a dictionary to unlist
    :param include_keys: only unlist these keys (optional)
    :param exclude_keys: exclude all other keys except these keys (optional)
    :return: generate key, value pairs
    """
    def unlist_helper(d, include_keys=[], exclude_keys=[], keys=[]):
        if isinstance(d, dict):
            for key, val in d.items():
                if isinstance(val, list):
                    if len(val) == 1:
                        path = '.'.join(keys + [key])
                        if include_keys and path in include_keys:
                            d[key] = val[0]
                        elif path not in exclude_keys:
                            d[key] = val[0]
                elif isinstance(val, dict):
                    unlist_helper(val, include_keys, exclude_keys, keys + [key])
    unlist_helper(d, include_keys, exclude_keys, [])
    return d
