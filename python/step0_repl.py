import sys, traceback

def READ(s):
	return s

def EVAL(s):
	return s

def PRINT(s):
	return s

def rep(s):
	return PRINT(EVAL(READ(s)))

while True:
	try:
		line = raw_input('user> ')
		print(rep(line))
	except EOFError:
		break
	except Exception:
		print("".join(traceback.format_exception(*sys.exc_info())))
