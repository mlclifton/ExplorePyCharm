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
from collections import namedtuple



def test_subscript_through_literal():
	some_list = []
	some_list.append('foo')
	some_list.append('bar')
	assert len(some_list) == 2

def subscript_through_int_param(index: int) -> str:
	some_list = []
	some_list.append('foo')
	some_list.append('bar')
	val = some_list[index]
	return val
	
def test_subscript_through_int_param():
	val = subscript_through_int_param(1)
	assert val == 'bar'

class ThingInAList():
	def __init__(self, bias):
		self.WeightedInput = namedtuple('WeightedInput', 'weight value')
		self.bias = bias
		self.inputs = []
	
	def add_input(self, weight: float) -> int:
		handle = len(self.inputs)
		new_input = self.WeightedInput(weight = weight, value = 0)
		self.inputs.append(new_input)
		return handle
		
	def set_input(self, handle: int, value: float):
		ip = self.inputs[handle]
		ip.value = value


class TestListUnderstanding():

	def test_create_a_thing(self):
		a_thing = ThingInAList(2)
	
	def test_add_an_input(self):
		a_thing = ThingInAList(2)
		iph1 = a_thing.add_input(2)
		a_thing.set_input(iph1, 1)
		

if __name__ == '__main__':
	test_subscript_through_literal()
