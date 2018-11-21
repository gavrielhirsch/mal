import reader, printer

def READ(s):
	return reader.read_str(s)

def EVAL(expr):
	return expr

def PRINT(expr):
	return printer.print_str(expr)

def rep(s):
	return PRINT(EVAL(READ(s)))

while True:
	try:
		line = raw_input('user> ')
		print(rep(line))
	except EOFError:
		break
