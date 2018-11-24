import string, mal_types

def print_str(expr):
	if (expr is None):
		return "()"
	elif (mal_types.isList(expr)):
		return '(' + printList(expr) + ')'
	else:
		return str(expr)

def printList(lst):
	if (mal_types.rest(lst) is None):
		return print_str(lst.car)
	else:
		return print_str(lst.car) + ' ' + printList(lst.cdr)
