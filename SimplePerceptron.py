##################################################
## playing about with Perceptrons
##################################################
import pytest


##################################################
## basic Perceptron
##################################################
class SimplePerceptron:
	""" Simple perceptron implementation supporting inputs and a bias.
	"""
	def __init__(self, bias=0.0):
		""" Initialises with the specified bias.
		
		Parameters
		----------
		bias
			The perceptron's bias. This will be the value returned by eval() if no inputs are set; thus allowing the same class to be used as an input layer node.
		"""
		self._bias = bias
		self._input_weights = []
		self._input_values = []
		
	def set_bias(self, bias: float) -> None:
		"""Change the bias after initialisation"""
		self._bias = bias
		
	def add_input(self, weight: float) -> int:
		"""Setup a new input with specified weight.
		
		Parameters
		----------
		weight
			Weight applied to this input.
			
		Returns
		-------
		int
			The index used to reference the newly added input.
		"""
		self._input_weights.append(weight)
		self._input_values.append(None)
		return len(self._input_weights) - 1
		
	def set_input(self, index: int, value: float) -> None:
		"""Set an input value
		
		Parameters
		----------
		index
			As returned by a call to add_input
		value
			The new value for the input identified by index
		"""
		self._input_values[index] = value
		
	def get_input(self, index: int) -> int:
		"""Read a previously created input
		
		Parameters
		----------
		index
			As returned by a call to add_input
		"""
		if index <= len(self._input_values) - 1:
			return self._input_values[index]
		else:
			return None
			
	def eval(self) -> float:
		"""Evaluate this Perceptron

		Returns
		-------
		float
			sum of all products of input values and associated weights added to the bias.
		"""
		idx = 0
		res = 0
		for ip in self._input_weights:
			res = res + self._input_weights[idx] * self._input_values[idx]
			idx = idx + 1
		return res + self._bias
		
		
class TestSimplePerceptron:
	@pytest.fixture()
	def setup_nand_perceptron(self):
		self.simple_perceptron = SimplePerceptron(bias=3)
		self.simple_perceptron.add_input(weight=-2)
		self.simple_perceptron.add_input(weight=-2)
		
	def test_setup(self):
		p = SimplePerceptron(bias=3)
		ip1_h = p.add_input(weight=-2)
		assert p.get_input(ip1_h) is None
		ip2_h = p.add_input(weight=-2)
		assert p.get_input(ip2_h) is None
		
	def test_can_set_inputs(self):
		p = SimplePerceptron(bias=3)
		ip1_h = p.add_input(weight=-2)
		p.set_input(ip1_h, 0)
		assert p.get_input(ip1_h) == 0
		ip2_h = p.add_input(weight=-2)
		p.set_input(ip2_h, 1)
		assert p.get_input(ip2_h) == 1
		
	@pytest.mark.usefixtures("setup_nand_perceptron")
	def test_simple_nand_00(self):
		self.simple_perceptron.set_input(0, 0)
		self.simple_perceptron.set_input(1, 0)
		assert self.simple_perceptron.eval() > 0
		
	@pytest.mark.usefixtures("setup_nand_perceptron")
	def test_simple_nand_01(self):
		self.simple_perceptron.set_input(0, 0)
		self.simple_perceptron.set_input(1, 1)
		assert self.simple_perceptron.eval() > 0
		
	@pytest.mark.usefixtures("setup_nand_perceptron")
	def test_simple_nand_10(self):
		self.simple_perceptron.set_input(0, 1)
		self.simple_perceptron.set_input(1, 0)
		assert self.simple_perceptron.eval() > 0
		
	@pytest.mark.usefixtures("setup_nand_perceptron")
	def test_simple_nand_11(self):
		self.simple_perceptron.set_input(0, 1)
		self.simple_perceptron.set_input(1, 1)
		assert self.simple_perceptron.eval() < 0
	
	def test_input_percertron(self):
		p = SimplePerceptron(bias=3)
		assert p.eval() == 3
		p = SimplePerceptron(bias=0)
		assert p.eval() == 0
		p = SimplePerceptron(bias=-3)
		assert p.eval() == -3
		p = SimplePerceptron(bias=0.5)
		assert p.eval() == 0.5

