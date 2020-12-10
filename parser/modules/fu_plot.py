# necessary imports
from matplotlib.colors import is_color_like


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
# TODO: parse the props and add to plot statement
def plot(xs, ys, zs, ax, props):
	# TODO: read props and apply properties
	title = props.get('title', None)
	x_label = props.get('xlabel', None)
	y_label = props.get('ylabel', None)
	label = props.get('label', None)


	color = props.get('color', 'black')
	if color != None and not is_color_like(color):
		raise Exception('Illegal value {} for parameter color'.format(color))
	
	level = props.get('level', None)
	if (level != "single" and level != "multiple" and level != None):
		raise Exception('Illegal value {} for parameter level'.format(all_level))

	if title: ax.set_title(title)
	if x_label: ax.set_xlabel(x_label)
	if y_label: ax.set_ylabel(y_label)
	if label:	ax.set_label(label)
	if zs is not None:
		if level == "multiple": ax.contour(xs, ys, zs)
		else: ax.contour(xs, ys, zs, [0])
	else: 
		ax.plot(xs, ys, label=label, color=color)


# creates the plot for the user
def create_plot(ax, grid, xs, ys, zs=None, attr_list=None):
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
		plot(xs, ys, zs, ax, attr_list)
	elif rows == 1 or cols == 1:
		# axis can be subscript using one index
		plot(xs, ys, zs, ax[row * col - 1], attr_list)
	else:
		# axis can be subscript using both index
		plot(xs, ys, zs, ax[row - 1][col - 1], attr_list)

	# occupy this location
	grid[row - 1][col - 1] = 1.0

