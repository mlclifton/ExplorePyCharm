# understanding pytest


# EXPLORE GIT & PYCHARM MULTI FILE COMMIT MADE TO MULTIPLE


import pytest


def test_func():
    pass


def test_another_test_with_assert():
    assert False, "This should fail"


def test_a_third_test():
    pass


class TestClass:

    def test_in_a_class(self):
        pass

    def this_is_not_a_test_in_a_class(self):
        pass


class NotATestClass:

    def test_name_but_wont_be_collected(self):
        pass


@pytest.fixture()
def another_named_fixture():
    pass


@pytest.fixture()
def named_fixture():
    pass


# this should call named_fixture() before entering the function.
def test_using_named_fixture(named_fixture):
    pass


@pytest.mark.usefixtures("named_fixture")
def test_also_using_named_fixture():
    pass


class DummyClass():
    def __init__(self):
        self.some_list = ['Foo', 'Bar']


class TestClassUsingFixture:
    def __init__(self):
        self.some_class_instance = DummyClass()

    @pytest.fixture()
    def setup_test_fixture(self):
        self.some_class_instance.some_list[0] = 'FooBar'
        self.some_class_instance.some_list[1] = 'BarFoo'

    def test_a_method_using_a_fixture(self, setup_test_fixture):
        assert self.some_class_instance.some_list[0] == 'FooBar'
