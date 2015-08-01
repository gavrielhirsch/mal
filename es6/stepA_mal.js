import { readline } from './node_readline';
import { Sym, _list_Q, _malfunc, _malfunc_Q, _sequential_Q } from './types';
import { BlankException, read_str } from './reader';
import { pr_str } from './printer';
import { new_env, env_set, env_get } from './env';
import { core_ns } from './core';

// read
const READ = (str) => read_str(str);

// eval
const is_pair = x => _sequential_Q(x) && x.length > 0

const quasiquote = ast => {
    if (!is_pair(ast)) {
        return [new Sym("quote"), ast];
    } else if (ast[0].name === 'unquote') {
        return ast[1];
    } else if (is_pair(ast[0]) && ast[0][0].name === 'splice-unquote') {
        return [new Sym("concat"), ast[0][1], quasiquote(ast.slice(1))];
    } else {
        return [new Sym("cons"), quasiquote(ast[0]), quasiquote(ast.slice(1))];
    }
}

function is_macro_call(ast, env) {
    return _list_Q(ast) &&
           ast[0] instanceof Sym &&
           ast[0] in env &&
           env_get(env, ast[0]).ismacro;
}

function macroexpand(ast, env) {
    while (is_macro_call(ast, env)) {
        let mac = env_get(env, ast[0]);
        ast = mac(...ast.slice(1));
    }
    return ast;
}


const eval_ast = (ast, env) => {
    if (ast instanceof Sym) {
        return env_get(env, ast)
    } else if (_list_Q(ast)) {
        return ast.map((x) => EVAL(x, env));
    } else {
        return ast;
    }
}

const EVAL = (ast, env) => {
  while (true) {
    //console.log("EVAL:", pr_str(ast, true));
    if (!_list_Q(ast)) { return eval_ast(ast, env) }

    ast = macroexpand(ast, env);
    if (!_list_Q(ast)) { return ast; }

    let [{ name: a0sym }, a1, a2, a3] = ast;
    switch (a0sym) {
        case 'def!': 
            return env_set(env, a1, EVAL(a2, env));
        case 'let*':
            let let_env = new_env(env);
            for (let i=0; i < a1.length; i+=2) {
                env_set(let_env, a1[i], EVAL(a1[i+1], let_env));
            }
            env = let_env;
            ast = a2;
            break; // continue TCO loop
        case "quote":
            return a1;
        case "quasiquote":
            ast = quasiquote(a1);
            break; // continue TCO loop
        case "defmacro!":
            let func = EVAL(a2, env);
            func.ismacro = true;
            return env_set(env, a1, func);
        case "macroexpand":
            return macroexpand(a1, env);
        case "try*":
            try {
                return EVAL(a1, env);
            } catch (exc) {
                if (a2 && a2[0].name === "catch*") {
                    if (exc instanceof Error) { exc = exc.message; }
                    return EVAL(a2[2], new_env(env, [a2[1]], [exc]));
                } else {
                    throw exc;
                }
            }
        case "do":
            eval_ast(ast.slice(1,ast.length-1), env);
            ast = ast[ast.length-1];
            break; // continue TCO loop
        case "if":
            let cond = EVAL(a1, env);
            if (cond === null || cond === false) {
                ast = (typeof a3 !== "undefined") ? a3 : null;
            } else {
                ast = a2;
            }
            break; // continue TCO loop
        case "fn*":
            return _malfunc((...args) => EVAL(a2, new_env(env, a1, args)),
                    a2, env, a1);
        default:
            let [f, ...args] = eval_ast(ast, env);
            if (_malfunc_Q(f)) {
                env = new_env(f.env, f.params, args);
                ast = f.ast;
                break; // continue TCO loop
            } else {
                return f(...args);
            }
    }
  }
}

// print
const PRINT = (exp) => pr_str(exp, true);

// repl
let repl_env = new_env();
const REP = (str) => PRINT(EVAL(READ(str), repl_env));

// core.EXT: defined using ES6
for (let [k, v] of core_ns) { env_set(repl_env, new Sym(k), v) }
env_set(repl_env, new Sym('eval'), a => EVAL(a, repl_env));
env_set(repl_env, new Sym('*ARGV*'), []);

// core.mal: defined using language itself
REP("(def! *host-language* \"ecmascript6\")")
REP("(def! not (fn* (a) (if a false true)))")
REP("(def! load-file (fn* (f) (eval (read-string (str \"(do \" (slurp f) \")\")))))")
REP("(defmacro! cond (fn* (& xs) (if (> (count xs) 0) (list 'if (first xs) (if (> (count xs) 1) (nth xs 1) (throw \"odd number of forms to cond\")) (cons 'cond (rest (rest xs)))))))")
REP("(defmacro! or (fn* (& xs) (if (empty? xs) nil (if (= 1 (count xs)) (first xs) `(let* (or_FIXME ~(first xs)) (if or_FIXME or_FIXME (or ~@(rest xs))))))))")

if (process.argv.length > 2) { 
    env_set(repl_env, '*ARGV*', process.argv.slice(3));
    REPL('(load-file "' + process.argv[2] + '")');
    process.exit(0);
}

REP("(println (str \"Mal [\" *host-language* \"]\"))")
while (true) {
    let line = readline("user> ");
    if (line == null) break;
    try {
        if (line) { console.log(REP(line)); }
    } catch (exc) {
        if (exc instanceof BlankException) { continue; }
        if (exc.stack) { console.log(exc.stack); }
        else           { console.log("Error: " + exc); }
    }
}