import re, mal_types, printer

class Reader:
	def __init__(self, tokens, pos):
		self.tokens = tokens
		self.pos = pos

	def next(self):
		curr = self.peek()
		self.pos += 1
		return curr

	def peek(self):
		if (len(self.tokens) > self.pos):
			return self.tokens[self.pos]
		else:
			return None

def tokenizer(s):
	tre = re.compile(r"""[\s,]*(~@|[\[\]{}()'`~^@]|"(?:[\\].|[^\\"])*"?|;.*|[^\s\[\]{}()'"`@,;]+)""");
	return [t for t in re.findall(tre, s) if t[0] != ';']

def read_str(s):
	reader = Reader(tokenizer(s), 0)
	return read_form(reader)

def read_form(reader):
	next = reader.next()
	if (next == '('):
		return read_list(reader)
	return read_atom(next)

def read_list(reader):
	if (reader.peek() == ')'):
		reader.next()
		return None
	else:
		first = read_form(reader)
		rest = read_list(reader)
		return mal_types.cons(first, rest)

def read_atom(s):
	if (mal_types.isNil(s)):
		return None
	elif (mal_types.isInt(s)):
		return int(s)
	elif (mal_types.isFloat(s)):
		return float(s)
	else:
		return mal_types.Symbol(s)
