import sys, traceback, reader, printer, mal_types, env

def READ(s):
	return reader.read_str(s)

def EVAL(ast, envm):
	if (not mal_types.isList(ast)):
		return eval_ast(ast, envm)
	elif (mal_types.isEmpty(ast)):
		return ast
	else:
		first = ast.car
		rest = ast.cdr
		if (first == 'def!'):
			rest = ast.cdr
			def_value = EVAL(rest.cdr.car, envm)
			envm.set(rest.car, def_value)
			return def_value
		elif (first == 'let*'):
			let_env = env.Env(envm)
			bind_list = rest.car
			bind(let_env, bind_list)

			stmt = rest.cdr.car
			return EVAL(stmt, let_env)
		else:
			evaluated = eval_ast(ast, envm)
			return evaluated.car(*evaluated.cdr)

def PRINT(expr):
	return printer.print_str(expr)

def rep(s):
	return PRINT(EVAL(READ(s), repl_env))

def bind(envm, bind_list):
	if (not mal_types.isEmpty(bind_list)):
		envm.set(bind_list.car, EVAL(bind_list.cdr.car, envm))
		bind(envm, bind_list.cdr.cdr)

def eval_ast(ast, envm):
	if (mal_types.isSymbol(ast)):
		return envm.get(ast)
	elif (not mal_types.isList(ast)):
		return ast
	else:
		return eval_list(ast, envm)

def eval_list(lst, envm):
	if (mal_types.isEmpty(lst)):
		return None
	else:
		return mal_types.cons(EVAL(lst.car, envm), eval_list(lst.cdr, envm))


repl_env = env.Env(None)
repl_env.set('+', lambda a,b: a+b)
repl_env.set('-', lambda a,b: a-b)
repl_env.set('*', lambda a,b: a*b)
repl_env.set('/', lambda a,b: int(a/b))

while True:
	try:
		line = raw_input('user> ')
		print(rep(line))
	except EOFError:
		break
	except Exception:
		print("".join(traceback.format_exception(*sys.exc_info())))
