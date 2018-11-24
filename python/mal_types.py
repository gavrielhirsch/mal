class Symbol(str):
        pass

class List:
	def __init__(self, car, cdr):
		self.car = car
		self.cdr = cdr

def isList(lst):
	return (isinstance(lst, List) or lst is None)

def first(seq):
	if (seq is None):
		return None
	elif (isList(seq)):
		return seq.car
	else:
		raise ValueError('Argument is not a sequence')

def rest(seq):
	if (seq is None):
		return None
	elif (isList(seq)):
		return seq.cdr
	else:
		raise ValueError('Argument is not a sequence')

def cons(a, b):
	return List(a, b)

def isNil(s):
	return (s == 'NIL' or s == 'nil' or s == "'()")

def isInt(s):
	try:
		int(s)
		return True
	except (ValueError, TypeError):
		return False

def isFloat(s):
	try:
		float(s)
		return True
	except (ValueError, TypeError):
		return False
