# some tests to explore collections in Python

# EXPLORE GIT & PYCHARM MULTI FILE COMMIT MADE TO MULTIPLE


def function_taking_an_int(an_int: int) -> int:
    new_int = an_int + 1
    return new_int


def test_calling_func_taking_an_int() -> None:
    org_int = 1
    some_int = function_taking_an_int(org_int)
    assert some_int != org_int


def test_accessing_index():
    some_list = ['foo', 'bar']
    how_many = len(some_list)
    assert how_many == 2
