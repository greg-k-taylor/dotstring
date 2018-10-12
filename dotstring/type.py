import sys


####################
# is_str
####################
if sys.version_info.major == 3:
    str_types = str
else:
    str_types = (str, unicode)

def is_str(s):
    """return True or False if input is a string or not.
        python3 compatible.
    """
    return isinstance(s, str_types)

##############################
# safe type conversion
##############################
def safe_type(f, val):
    """
    Convert an input string to int/float.  If the
    conversion fails then None is returned.
    If value of a type other than a string
    then the original value is returned.
    """
    if is_str(val):
        try:
            return f(val)
        except ValueError:
            pass
    return val

def to_float(val):
    """convert an input string to int"""
    return safe_type(float, val)

def to_int(val):
    """convert an input string to float"""
    return safe_type(int, val)
