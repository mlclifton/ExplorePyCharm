
# playing about with Perceptrons


class SimplePerceptron:
    def __init__(self, a_bias):
        self._bias = a_bias
        self._input_weights = []
        self._input_values = []

    def add_input(self, a_weight):
        self._input_weights.append(a_weight)

    def set_input(self, a_index, a_value):
        self._input_values[a_index] = a_value

    def eval(self):
        idx = 0
        res = 0
        for ip in self._input_weights:
            res = res + self._input_weights[idx] * self._input_values[idx]
            idx = idx + 1
        return res


class TestPerceptron:
    def test_simple_nand(self):
        p = SimplePerceptron(3)
        p.add_input(-2)
        p.add_input(-2)
        result = p.eval()
        assert result == 1