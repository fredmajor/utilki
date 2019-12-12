"""
Generic utils for working with objects
"""


def _return_default(default):
    """
    If the default is a callable, return result of its execution. Return raw value otherwise.
    """
    return default() if callable(default) else default


def get_value_or_default(element, default, *keys):
    """
    Generic get-or-default for getting data from complex object-dict hierarchies.
    You specify a path to the element you need and the util traverse the hierarchy and
    returns the value.

    For example:

    class Cls1:
        def __init__(self, a):
            self.a = a

    class Cls2:
        def __init__(self, b):
            self.b = Cls1(b)

    my_dict = {
        'a': {
            'b': Cls2(2)
        }
    }
    val = get_value_or_default(my_dict, 'my_default', 'a', 'b', 'b', 'a')
    val == 2

    Warning: if path exists but contains None - default is returned.

    :param element: the object or dict you want to get the data from
    :param default: default value to use when the full path not found. If it is a callable, then it
        is lazy evaluated upon return. Default is used also when the path exists, but contains None.
    :param keys: path to the value you need
    :return: the value from your requested path or default
    """
    if not element:
        return _return_default(default)
    if len(keys) == 0:
        return element
    keys = list(keys)
    key = keys.pop(0)
    keys = tuple(keys)
    if not key:
        raise KeyError('You can not search for None')

    if type(element) is dict:
        try:
            element = element[key]
        except KeyError:
            return _return_default(default)
    else:
        element = getattr(element, key, None)
        if element is None:
            return _return_default(default)

    return get_value_or_default(element, default, *keys)
