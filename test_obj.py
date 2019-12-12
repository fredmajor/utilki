"""
Test object utils
"""
from unittest import TestCase
from unittest.mock import Mock

from obj import get_value_or_default


class Cls1:
    """
    Test data container
    """
    def __init__(self, a):
        self.a = a


class Cls2:
    """
    Another test data container
    """
    def __init__(self, b):
        self.b = Cls1(b)


class TestUtilsObj(TestCase):
    """
    Test object utils
    """

    def test_get_value_or_default_obj(self):
        """
        Test using objects as containers.
        """
        test_obj = Cls2(2)
        actual = get_value_or_default(test_obj, None, 'b', 'a')
        self.assertEqual(actual, 2)

        test_obj = Cls2(None)
        actual = get_value_or_default(test_obj, 'def', 'b', 'a')
        self.assertEqual(actual, 'def')

        actual = get_value_or_default(test_obj, 'def', 'b', 'c')
        self.assertEqual(actual, 'def')

        actual = get_value_or_default(test_obj, 'def', 'b', 'c', 'd')
        self.assertEqual(actual, 'def')

    def test_get_value_or_default_dict(self):
        """
        Test using dicts as containers.
        """
        tested = {
            'a': {
                'b': 'the value'
            }
        }
        actual = get_value_or_default(tested, 'def', 'a', 'b')
        self.assertEqual(actual, 'the value')

        actual = get_value_or_default(tested, 'def', 'a', 'c')
        self.assertEqual(actual, 'def')

        actual = get_value_or_default(tested, 'def', 'a', 'c', 'd')
        self.assertEqual(actual, 'def')

    def test_get_value_or_default_mixed_dict(self):
        """
        Test using a mix of dict-object as containers.
        """
        tested_dict_1 = {
            'a': {
                'b': Cls2(2)
            }
        }
        actual = get_value_or_default(tested_dict_1, 'def', 'a', 'b', 'b', 'a')
        self.assertEqual(actual, 2)

        actual = get_value_or_default(tested_dict_1, 'def', 'a', 'z', 'b', 'a')
        self.assertEqual(actual, 'def')

        actual = get_value_or_default(tested_dict_1, 'def', 'a', 'b', 'z', 'a')
        self.assertEqual(actual, 'def')

        actual = get_value_or_default(tested_dict_1, 'def', 'a', 'z', 'z', 'a')
        self.assertEqual(actual, 'def')

    def test_get_value_or_default_mixed_obj(self):
        """
        Test using a mix of object-dict as containers.
        """
        inside_dict = {
            'a': {
                'b': 'the value'
            }
        }
        tested_obj = Cls2(inside_dict)

        actual = get_value_or_default(tested_obj, 'def', 'b', 'a', 'a', 'b')
        self.assertEqual(actual, 'the value')

        actual = get_value_or_default(tested_obj, 'def', 'b', 'z', 'a', 'b')
        self.assertEqual(actual, 'def')

        actual = get_value_or_default(tested_obj, 'def', 'b', 'a', 'z', 'b')
        self.assertEqual(actual, 'def')

        actual = get_value_or_default(tested_obj, 'def', 'b', 'z', 'z', 'b')
        self.assertEqual(actual, 'def')

    def test_callable_default(self):
        """
        Check if a callable default works fine.
        """
        dflt = lambda: "hello world"

        tested = {
            'a': {
                'b': 'the value'
            }
        }

        actual = get_value_or_default(tested, dflt, 'a', 'c')
        self.assertEqual(actual, "hello world")

    def test_callable_lazy(self):
        """
        Check if a callable default is truly lazy.
        """
        dflt = Mock(return_value="hello world")

        tested = {
            'a': {
                'b': 'the value'
            }
        }

        get_value_or_default(tested, dflt, 'a', 'b')
        dflt.assert_not_called()
