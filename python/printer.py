import string

def print_str(expr):
	if(isinstance(expr, list)):
		return '(' + string.join(map(lambda e: print_str(e), expr), ' ') + ')'
	else:
		return str(expr)
