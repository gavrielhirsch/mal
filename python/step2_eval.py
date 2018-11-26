import sys, traceback, reader, printer, mal_types

repl_env = {'+': lambda a,b: a+b,
            '++': lambda a,b,c: a+b+c,
            '-': lambda a,b: a-b,
            '*': lambda a,b: a*b,
            '/': lambda a,b: int(a/b)}

def READ(s):
	return reader.read_str(s)

def EVAL(ast, env):
	if (not mal_types.isList(ast)):
		return eval_ast(ast, env)
	elif (mal_types.isEmpty(ast)):
		return ast
	else:
		evaluated = eval_ast(ast, env)
		return evaluated.car(*evaluated.cdr)

def PRINT(expr):
	return printer.print_str(expr)

def rep(s):
	return PRINT(EVAL(READ(s), repl_env))

def eval_ast(ast, env):
	if (mal_types.isSymbol(ast)):
		val = env.get(ast)
		if (val is None):
			raise ValueError('Symbol ' + ast + ' is not defined')
		else:
			return val
	elif (not mal_types.isList(ast)):
		return ast
	else:
		return eval_list(ast, env)

def eval_list(lst, env):
	if (mal_types.isEmpty(lst)):
		return None
	else:
		return mal_types.cons(EVAL(lst.car, env), eval_list(lst.cdr, env))

while True:
	try:
		line = raw_input('user> ')
		print(rep(line))
	except EOFError:
		break
	except Exception:
		print("".join(traceback.format_exception(*sys.exc_info())))
