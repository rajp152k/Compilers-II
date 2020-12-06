import matplotlib.pyplot as plt
import numpy as np


from pathlib import Path
from lark import Lark, Transformer, v_args
from random import choice
import argparse
prs = argparse.ArgumentParser()
prs.add_argument('--src',help='.fu source file',default=None)
args = prs.parse_args()


############################################################
# utility procedures
def parse_size(rows, cols):
	# parse the number of rows
	if rows:
		rows = int(rows)
		if rows < 1:
			raise Exception("Number of rows must be at least 1")
	else: rows = 1

	# parse the number of columns
	if cols:
		cols = int(cols)
		if cols < 1:
			raise Exception("Number of cols must be at least 1")
	else: cols = 1

	# return the parsed rows and cols
	return (rows, cols)

# parses the bounds for the ranges
def parse_bounds(start, end, type, jump=None):
	# parse the start
	if not start:	raise Exception("Lower bound of interval must be provided")
	if not end:		raise Exception("Upper bound of interval must be provided")
	# parse values to type
	start = type(start)
	end = type(end)
	if not jump:
		# start <= end has to be satisfied
		if start > end:	raise Exception("Lower bound ({}) must be less than or equal to Upper bound ({})".format(start, end))
	elif jump == 0:
		# jump must be non-zero
		raise Exception("Step must be non-zero")
	elif jump > 0:	
		# start <= end has to be satisfied
		if start > end:	raise Exception("Lower bound ({}) must be less than or equal to Upper bound ({}) for step {}".format(start, end, step))
	else:
		# start >= end has to be satisfied
		if start < end:	raise Exception("Lower bound ({}) must be greater than or equal to Upper bound ({}) for step {}".format(start, end, step))
	# return the computed pair
	return (start, end)


# parses the given list
def parse_list(type, points):
	# stores the list items
	items = []
	# iterate through every point
	for point in points:
		items.append(type(point))
	# return the list
	return np.array(items)


# evaluates the reuslt for (item1 op item2)
def evaluate_op(item1, op, item2):
	if 		op == '+':	return np.add(item1, item2)
	elif 	op == "-":	return np.subtract(item1, item2)
	elif 	op == "*":	return np.multiply(item1, item2)
	elif 	op == "/":	return np.divide(item1, item2)
	elif 	op == "%":	return np.mod(item1, item2)
	elif 	op == "^":	return np.power(item1, item2)
	else 	:			raise Exception("Invalid operator {}".format(op))

# invokes the function on given item(s)
# TODO: add functions
def invoke_function(func, item):
	# take decision based on func
	if 		func == 'sin':	return np.sin(item)
	elif 	func == 'cos':	return np.cos(item)
	elif	func == 'log':	return np.log(item)
	elif	func == 'exp':	return np.exp(item)
	else	:				raise Exception("Unknown function {}".format(func))


# parses the constant
def parse_constant(value):
	if 		value == 'PI':		return np.pi
	elif 	value == 'EXP':		return np.e
	else	:					raise Exception("Unknown constant {}".format(value))


# returns the first empty-cell (if any otherwise last cell)
# index returned are 1-based
def first_empty_cell(grid, start_row=0, start_col=0):
	# get the number of rows and cols
	rows, cols = grid.shape
	# iterate through all cells
	for i in range(start_row, rows):
		for j in range(start_col, cols):
			# check if this satisify the criteria
			if grid[i][j] == 0:
				return (i + 1, j + 1)
	# return the last cell
	return (rows, cols)

# creates a plot with given values on given axes
def plot_plot(xs, ys, ax, props):
	# TODO: read props and apply properties
	title = props.get('title', None)
	x_label = props.get('xlabel', None)
	y_label = props.get('ylabel', None)
	label = props.get('label', None)
	if title: ax.set_title(title)
	if x_label: ax.set_xlabel(x_label)
	if y_label: ax.set_ylabel(y_label)
	if label:	ax.set_label(label)
	ax.plot(xs, ys, label=label)

# creates the plot for the user
def create_plot(ax, grid, xs, ys, attr_list):
	# fetch the number or rows and cols
	rows, cols = grid.shape
	# fetch the first non-empty cell
	def_row, def_col = first_empty_cell(grid)
	# fetch the index to plot
	row = attr_list.get('row', None)
	col = attr_list.get('col', None)
	# parse to integers
	if row:	row = int(row)
	if col: col = int(col)
	# if neither row nor col are provided we scan entire grid
	if	not row and not col:
		# default ends to last cell
		row = rows; col = cols; found = False;
		# iterate through all cells
		for i in range(rows):
			for j in range(cols):
				if grid[i][j] == 0: col = j + 1; found=True; break;
			if found: row = i + 1; break;
	# if column but not row is provided we scan row
	elif 	not row and col:		
		# check if column is valid
		if col < 1 or col > cols: 
			raise Exception("Column index out of range")
		# default ends to last row
		row = rows
		# iterate through all rows in this col
		for i in range(rows):
			if grid[i][col - 1] == 0: row = i + 1; break;
	# if row but not col is provided we scan col
	elif	row and not col:
		# check if row is valid		
		if row < 1 or row > rows: 
			raise Exception("Row index out of range")
		# default ends to last col
		col = cols
		# iterate through all cols in this row
		for j in range(cols):
			if grid[row - 1][j] == 0: col = j + 1; break;

	# check bounds
	if row < 1 or row > rows: raise Exception("Row index out of range")
	if col < 1 or col > cols: raise Exception("Column index out of range")

	# find appropriate indexing
	if rows == 1 and cols == 1:
		# axis cannot be subscript
		plot_plot(xs, ys, ax, attr_list)
	elif rows == 1 or cols == 1:
		# axis can be subscript using one index
		plot_plot(xs, ys, ax[row * col - 1], attr_list)
	else:
		# axis can be subscript using both index
		plot_plot(xs, ys, ax[row - 1][col - 1], attr_list)

	# occupy this location
	grid[row - 1][col - 1] = 1.0


############################################################
# handles the evaluation using aliases
@v_args(inline=True)
class ProcessTree(Transformer):

	# constructor
	def __init__(self):
		# start with an empty list of variables
		self.rows = 1
		self.cols = 1
		self.fig_id = "We Do Give A Figure"
		self.vars = {}
		self.fig = None
		self.ax = None
		self.grid = []

	# figure statement alias - stmt_list is irrelevant here
	def figure(self, fig_id=None, *stmt_list):
		# fig_id must be provided
		if not fig_id:	raise Exception("FigureId must be provided")
		# update the figure
		self.fig_id = fig_id


	# displays the plot to the user
	def show_plots(self):
		plt.tight_layout()
		plt.legend()
		plt.show()

	# print_stmt alias
	def print_stmt(self, *var_ids):
		# iterate through all variables
		for var_id in var_ids:
			# get the string representation from Token
			var_id = str(var_id)
			# validate id
			if var_id not in self.vars: raise Exception("Unknown parameter {}".format(var_id))
			print("{} = {}".format(var_id, self.vars[var_id]))


	# plt_stmt alias	
	def plt_stmt(self, x_id, y_id, *attr_list):
		# get the string representation from Token
		x_id = str(x_id)
		y_id = str(y_id)
		# validate values
		if x_id not in self.vars:	raise Exception("Unknown parameter {}".format(x_id))
		if y_id not in self.vars:	raise Exception("Unknown parameter {}".format(y_id))
		# fetch values
		xs = self.vars[x_id]
		ys = self.vars[y_id]
		props = {}
		for item in attr_list: props = item
		create_plot(self.ax, self.grid, xs, ys, props)


	# size_stmt alias - attr_list LATER
	def size_stmt(self, rows=None, cols=None, attr_list=None):
		# parse the rows and cols
		self.rows, self.cols = parse_size(rows, cols)
		# create subplots
		self.fig, self.ax = plt.subplots(self.rows, self.cols)
		self.grid = np.zeros((self.rows, self.cols))






	# real_points_list alias 
	def real_points_list(self, *points):
		# parse and return the list
		return parse_list(float, points)

	# str_points_list alias 
	def str_points_list(self, *points):
		# parse and return the list
		return parse_list(str, points)

	# range_int_to_int alias
	def range_int_to_int(self, start=None, end=None):
		# parse the start and end values
		start, end = parse_bounds(start, end, int)
		# create and return teh array
		return np.arange(start, end)

	# range_real_to_real alias
	def range_real_to_real(self, start=None, end=None, step=None):
		# default jump
		jump = 0.1
		# update jump if provided
		if step:	jump = float(step)
		# parse the start and end values
		start, end = parse_bounds(start, end, float, jump)
		# create and return the array
		return np.arange(start, end, jump)


	# range_stmt alias
	def range_stmt(self, var_id, items=[]):
		# get the string representation from Token
		var_id = str(var_id)
		# add this variable
		self.vars[var_id] = items

	# expr_const alias
	def expr_const(self, const_item):
		# return the value of the constant
		return parse_constant(const_item)

	# expr_real alias
	def expr_real(self, number):
		# return the number
		return float(number)

	# expr_negation alias
	def expr_negation(self, value):
		# return the negation of expression
		return -1.0 * value

	# nested_expr alias
	def nested_expr(self, value):
		# return the value
		return value

	# expr_op_expr alias
	def expr_op_expr(self, value1, op, value2):
		# evaluate the expression
		return evaluate_op(value1, op, value2)







	# func_id alias
	def func_id(self, var_id):
		# get the string representation from Token
		var_id = str(var_id)
		# check if value exist
		if var_id not in self.vars:	raise Exception("Unknown parameter {}".format(var_id))
		# fetch the list of values for this variable
		items = self.vars[var_id]
		# return the values
		return items

	# func_real alias	
	def func_real(self, number):
		# parse and return the number
		return float(number)

	# func_const alias
	def func_cost(self, value):
		# take decision based on value
		return parse_constant(value)

	# func_negation alias
	def func_negation(self, item):
		# take unary negation
		return np.multiply(item, -1)

	# func_call alias 
	def func_call(self, func_name, item):
		# invoke the given function 
		return invoke_function(func_name, item)

	# nested_func alias
	def nested_func(self, expression):
		print(expression)

	# func_op_func alias
	def func_op_func(self, item1, op, item2):
		# evaluate the expression
		return evaluate_op(item1, op, item2)

	# fun_stmt alias
	def func_stmt(self, var_id, items):
		# get the string representation from Token
		var_id = str(var_id)
		# assign the values to the variable
		self.vars[var_id] = items



	# grabs and returns the attr_list
	def attr_list(self, *attrs):
		return dict(attrs)

	# grabs and returns the attribute
	def attribute(self, key, value):
		return (str(key), str(value))

# importing grammar
fg = Path('./fg.lark')
assert(fg.is_file())
with open(fg,'r') as f:
    grammar_raw = f.read()


if args.src is None:
    source = choice(list((Path()/'tests').glob('**/*.fu')))
    # tests on a random source from test
else:
    source = Path('.')/f'{args.src}'

assert(source.is_file() and source.suffix == '.fu')
print(f'testing {source.name}')

with open(source,'r') as f:
    code_raw = f.read()

# quick eval code for now: pretty prints program tree 
parser = Lark(grammar_raw, parser="lalr", transformer=ProcessTree())
parser.parse(code_raw)