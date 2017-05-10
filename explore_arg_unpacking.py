import pytest


def normal_func(p1: int, p2: str) -> None:
	print('p1 is % and p2 is %', p1, p2)

def test_positional_call(capsys):
	normal_func(99, 'Hello')
	out, err = capsys.readouterr()
	assert out == "p1 is 99 and p2 is Hello\n"

def test_packed(capsys):
	list = [99, 'Hello']
	normal_func(*list)
	out, err = capsys.readouterr()
	assert out == "p1 is 99 and p2 is Hello\n"

