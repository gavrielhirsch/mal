class Symbol(str):
        pass

class SeqIterator:
	def __init__(self, seq):
		self.seq = seq
	def next(self):
		if (iterDone(self.seq)):
			raise StopIteration
		else:
			curr = first(self.seq)
			self.seq = rest(self.seq)
			return curr

class List:
	def __init__(self, car, cdr):
		self.car = car
		self.cdr = cdr
	def __iter__(self):
		return SeqIterator(self)

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

def iterDone(seq):
	if (isList(seq)):
		return isEmpty(seq)
	else:
		return True

def cons(a, b):
	return List(a, b)

# Functions for determining classes
def isEmpty(lst):
	return lst is None

def isList(lst):
	return (isinstance(lst, List) or lst is None)

def isSymbol(sym):
	return isinstance(sym, Symbol)

# Functions for parsing
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
