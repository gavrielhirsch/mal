import re, mal_types

class Reader:
	def __init__(self, tokens, pos):
		self.tokens = tokens
		self.pos = pos

	def next(self):
		curr = self.peek()
		self.pos += 1
		return curr

	def peek(self):
		if(len(self.tokens) > self.pos):
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
	if(next == '('):
		return read_list(reader)
	return read_atom(next)

def read_list(reader): # Should change this to use more LISP-y lists, can add to mal_types
	l = []
	while(reader.peek() != ')'):
		l.append(read_form(reader))
	return l

def read_atom(s):
	if(mal_types.isInt(s)):
		return int(s)
	elif(mal_types.isFloat(s)):
		return float(s)
	else:
		return mal_types.Symbol(s)
