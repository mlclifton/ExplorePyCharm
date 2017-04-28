# understanding pytest

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
