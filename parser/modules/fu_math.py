# necessary imports
import math
import numpy as np

# define the constants
CONSTANTS = {
	'PI' : np.pi,
	'EXP': np.e
}

# invokes the function on given item(s)
# TODO: Add more function as per numpy library
def invoke_function(func, item):
	# take decision based on func
	if 		func == 'sin':	return np.sin(item)
	elif 	func == 'cos':	return np.cos(item)
	elif	func == 'log':	return np.log(item)
	elif	func == 'exp':	return np.exp(item)
	else	:				raise Exception("Unknown function {}".format(func))


# parses the constant
# TODO: Add more required constants
def parse_constant(value):
	if value in CONSTANTS:	return CONSTANTS[value]
	# if 		value == 'PI':		return np.pi
	# elif 	value == 'EXP':		return np.e
	else	:					raise Exception("Unknown constant {}".format(value))


# evaluates the reuslt for (item1 op item2)
def evaluate_op(item1, op, item2):
	if 		op == '+':	return np.add(item1, item2)
	elif 	op == "-":	return np.subtract(item1, item2)
	elif 	op == "*":	return np.multiply(item1, item2)
	elif 	op == "/":	return np.divide(item1, item2)
	elif 	op == "%":	return np.mod(item1, item2)
	elif 	op == "^":	return np.power(item1, item2)
	else 	:			raise Exception("Invalid operator {}".format(op))
