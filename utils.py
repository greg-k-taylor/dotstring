

def to_int(val):
    """convert an input string to int."""
    if isinstance(val, str):
        try:
            return int(val)
        except ValueError:
            pass
    return val

def to_float(val):
    """convert an input string to float."""
    if isinstance(val, str):
        try:
            return float(val)
        except ValueError:
            pass
    return val

def last_element(d, key_list):
    k = key_list.pop(0)
    if not len(key_list):
        return k, d
    else:
        t = d[k]
        if isinstance(t, dict):                
            return last_element(d[k], key_list)
        elif isinstance(t, list):
            for l in t:
                return last_element(l, key_list)
        elif isinstance(t, tuple):
            # unsupported type
            raise ValueError("unsupported type in key {}".format(k))

def key_value(dictionary, key):
    key_list = key.split('.')
    k, le = last_element(dictionary, key_list)
    return le[k]
    
def set_key_value(dictionary, key, value):
    key_list = key.split('.')
    k, le = last_element(dictionary, key_list)
    le[k] = value
    return dictionary

def traverse_keys(d, include_keys=[], exclude_keys=[]):
    """
    # bydefault, traverse all kes
    # only traverse the list from include_kes a.b, a.b.c
    # only exclude the list from exclude_keys
    """
    if include_keys:
        for k in include_keys:
            yield k, key_value(d, k)

def value_convert(d, fn, include_keys=[], exclude_keys=[]):
    for path, value in traverse_keys(d, include_keys, exclude_keys):
        new_value = fn(value)
        set_key_value(d, path, new_value)
    return d
