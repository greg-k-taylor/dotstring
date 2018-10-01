from vconvert.type import is_str
from vconvert.type import to_float
from vconvert.type import to_int


def last_element(d, key_list):
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
            yield from last_element(d[k], key_list)
        elif isinstance(t, list):
            for l in t:
                yield from last_element(l, key_list.copy())
        elif isinstance(t, tuple):
            # unsupported type
            raise ValueError("unsupported type in key {}".format(k))
    
def key_value(dictionary, key):
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

def traverse_keys(d, include_keys=[], exclude_keys=[]):
    """
    # bydefault, traverse all keys
    # only traverse the list from include_kes a.b, a.b.c
    # only exclude the list from exclude_keys
    """
    def traverse_helper(d, keys):
        if isinstance(d, dict):
            for k in d.keys():
                yield from traverse_helper(d[k], keys + [k])
        if isinstance(d, list):
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
                print(key, val)
                yield key, val

def value_convert(d, fn, include_keys=[], exclude_keys=[]):
    for path, value in traverse_keys(d, include_keys, exclude_keys):
        new_value = fn(value)
        set_key_value(d, path, new_value)
    return d

def int_convert(d, include_keys=[], exclude_keys=[]):
    return value_convert(d, to_int, include_keys, exclude_keys)

def float_convert(d, include_keys=[], exclude_keys=[]):
    return value_convert(d, to_float, include_keys, exclude_keys)
