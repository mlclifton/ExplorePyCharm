import pytest

# Some pretty basic python tests to verify my understanding of Python's classes


class SimpleClass:

    # this should be the equivalent of a constructor
    def __init__(self, str_val: str, int_val: int):
        # the underscore should make this private
        self.__str_val = str_val
        self.__int_val = int_val
        self.__int_prop = 0
        self.public_str_val = str_val

    # this should provide a pretty print
    # http://stackoverflow.com/questions/1436703/difference-between-str-and-repr-in-python/2626364#2626364
    def __str__(self) -> str:
        return 'SimpleClass(str_val="%s", int_val=%s, public_str_val="%s", twice_the_int_val=%i)' % (
            self.__str_val, self.__int_val, self.public_str_val, self.twice_the_int_val)

    # should return a string that can be used to construct and instance using eval()
    # in this case, init() takes only two arguments and so repr() only includes them whereas str()
    # produces a string with all attributes / properties
    # http://stackoverflow.com/questions/1436703/difference-between-str-and-repr-in-python/2626364#2626364
    def __repr__(self) -> str:
        return 'SimpleClass(str_val="%s", int_val=%s)' % (self.__str_val, self.__int_val)

    # deep check for equality
    # http://stackoverflow.com/questions/1227121/compare-object-instances-for-equality-by-their-attributes-in-python
    def __eq__(self, other) -> bool:
        return self.__dict__ == other.__dict__

    # This implements a read-only / computed property as there is no setter.
    # A setter could be implemented as follows:
    #     @twice_the_int_val.setter
    #     def twice_the_int_val(self, twice_the_int_val):
    #         pass
    @property
    def twice_the_int_val(self) -> int:
        return self.__int_val * 2

    # This creates a read / write property. As implemented here it's fairly pointless and a simple
    # public attribute would do just as well however, there is an opportunity to compute the returned
    # value or validate / constrain the set value.
    @property
    def rw_int_property(self) -> int:
        return self.__int_prop

    # this is the setter or a set/get property pair
    @rw_int_property.setter
    def rw_int_property(self, rw_int_property: int) -> None:
        self.__int_prop = rw_int_property


class TestMyUnderstandingOfClasses:

    # simple test to build an instance - succeeds if no error is raised.
    def test_instantiation(self):
        SimpleClass(str_val="one", int_val=3)

    # does repr() give the expected string representation
    def test_string_representation(self):
        c1 = SimpleClass(str_val="one", int_val=3)
        str_rep = repr(c1)
        assert str_rep == 'SimpleClass(str_val="one", int_val=3)'

    # can I reform the same object after serialising it?
    def test_eval_from_serialised_representation(self):
        c1 = SimpleClass(str_val="one", int_val=3)
        str_rep = repr(c1)
        c2 = eval(str_rep)
        assert c1 == c2

    # does it print as expected?
    def test_print_as_expected(self, capsys):
        c1 = SimpleClass(str_val="one", int_val=3)
        print(c1)
        out, err = capsys.readouterr()
        assert out == 'SimpleClass(str_val="one", int_val=3, public_str_val="one", twice_the_int_val=6)\n'

    # does an exception get raised when we try to assign to what should
    # be a read-only propert?
    def test_read_only_propery(self):
        c1 = SimpleClass(str_val="one", int_val=3)
        assert c1.twice_the_int_val == 6
        with pytest.raises(Exception):
            c1.twice_the_int_val = 10

    # pre-pending double underscore should make an attribute private to the class
    def test_cant_access_private_attribute(self):
        c1 = SimpleClass(str_val="one", int_val=3)
        c1.__str_val = "not really private!"
        str_rep = str(c1)
        # If the access attempt above worked then this assert would fail as str_val would have changed
        assert str_rep == 'SimpleClass(str_val="one", int_val=3, public_str_val="one", twice_the_int_val=6)'

    # rw_int_property is implemented as a property with a getter and a setter ... simple test to ensure I
    # can set it and get it.
    def test_rw_property_works(self):
        c1 = SimpleClass(str_val="one", int_val=3)
        c1.rw_int_property = 10
        assert c1.rw_int_property == 10
