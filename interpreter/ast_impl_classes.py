from ast_abstract_classes import *

class Context:
    vars_ = {}

    def __init__(self):
        self.vars_ = {}
        self.functions = {}
    
    def set_var(self, name, val):
        self.vars_[name] = val
    
    def get_var(self, name):
        if name not in self.vars_:
            print("{} NOT FOUND IN DICT".format(name))
            self.print()
            return None

        return self.vars_[name]

    def print(self):
        print("vars:")
        for k, v in self.vars_.items():
            print("  {} = {}".format(k, v))

def indent_str(text, indent):
    s = ""
    for i in range(0, indent):
        s += "  "
    
    s += text
    return s

class Program:
    statements: Statements = None
    def __init__(self, statements: Statements):
        self.statements = statements
    
    def eval(self, ctx):
        return self.statements.eval(ctx)

    def print(self):
        print("Program: ")
        self.statements.print(1)

class Statements_stmt_stmts(Statements):
    head: Statement = None
    tail: Statements = None

    def __init__(self, stmt: Statement, stmts: Statements):
        self.head = stmt
        self.tail = stmts 

    def eval(self, ctx):
        ctx_update = self.head.eval(ctx)
        return self.tail.eval(ctx_update)
    
    def print(self, indent):
        print(indent_str("Statements:", indent))
        print(indent_str("-head:", indent))
        self.head.print(indent + 1)
        print(indent_str("-tail:", indent))
        self.tail.print(indent + 1)


class Statements_stmts_stmt(Statements):
    head: Statements = None
    tail: Statement = None

    def __init__(self, stmts: Statements, stmt: Statement):
        self.head = stmts
        self.tail = stmt

    def eval(self, ctx):
        ctx_update = self.head.eval(ctx)
        return self.tail.eval(ctx_update)

    def print(self, indent):
        print(indent_str("Statements:", indent))
        print(indent_str("-head:", indent))
        self.head.print(indent + 1)
        print(indent_str("-tail:", indent))
        self.tail.print(indent + 1)

class Statements_stmt(Statements):
    head: Statement = None

    def __init__(self, stmt: Statement):
        self.head = stmt
    
    def eval(self, ctx):
        return self.head.eval(ctx)
    
    def print(self, indent):
        print(indent_str("Statements:", indent))
        print(indent_str("-statement:", indent))
        self.head.print(indent + 1)

class Statement_empty(Statement):
    def __init__(self):
        pass

    def eval(self, ctx):
        return ctx

    def print(self, indent):
        pass

class Statement_expr(Statement):
    expr: Expr = None

    def __init__(self, expr: Expr):
        self.expr = expr

    def eval(self, ctx):
        #TODO: store result of last expr
        return self.expr.eval(ctx)

    def print(self, indent):
        print(indent_str("Statement_expr:", indent))
        print(indent_str("-expr:", indent))
        self.expr.print(indent + 1)

class Statement_assign(Statement):
    assign: Assign = None
    
    def __init__(self, assign: Assign):
        self.assign = assign
    
    def eval(self, ctx):
        return self.assign.eval(ctx)

    def print(self, indent):
        print(indent_str("Statement:", indent))
        print(indent_str("-assign:", indent))
        self.assign.print(indent + 1)

class Assign_ref_exp(Assign):
    ref: RefExpr = None
    expr: Expr = None
    ref_cache = None
    expr_cache = None

    def __init__(self, ref: RefExpr, expr: Expr):
        self.ref = ref
        self.expr = expr

    def eval(self, ctx):
        ctx2 = self.ref.eval(ctx);
        self.ref_cache = self.ref.get_name()
        ctx3 = self.expr.eval(ctx2)
        self.expr_cache = self.expr.get_value()
        ctx3.set_var(self.ref_cache, self.expr_cache)
        return ctx3
    
    def get_ref(self):
        if self.ref_cache == None:
            print("ERROR, GET REF RUN FOR ASSSIGN THAT HASENT BEEN EVALD YET")
            return None

        return self.ref_cache

    def get_value(self):
        if self.expr_cache == None:
            print("ERROR, GET VALUE RUN FOR ASSIGN THAT HASENT BEEN EVALD YET")
            return None
        
        return self.expr_cache

    def print(self, indent):
        print(indent_str("Assign:", indent))
        print(indent_str("-ref:", indent))
        self.ref.print(indent + 1)
        print(indent_str("-expr:", indent))
        self.expr.print(indent + 1)

class Statement_for(Statement):
    index_var = None
    range_vals = None

    assign: Assign = None
    statements: Statements = None

    def __init__(self, assign: Assign, stmts: Statements):
        self.assign = assign
        self.statements = stmts
    
    def eval(self, ctx):
        ctx2 = self.assign.eval(ctx) #this variable only exists for the lifetime of the loop, and we are manually handling its context, so we only need this to do side effects
        self.index_var = self.assign.get_ref()
        self.range_vals = self.assign.get_value()

        #at this point, the variable from the assign is set to the iteration range in ctx2, we need to overwrite that

        for elem in self.range_vals:
            #SET (index_var, elem) TO CTX2
            #ctx2.set((index_var, elem)) #this should functionally delete the assigned varaible while keeping the side effects of the assign
            ctx2 = self.statements.eval(ctx2) #handle it like this to allow accumulators in the loop

        return ctx2 


class Name:
    val = None

    def __init__(self, val):
        self.val = val

    def eval(self, ctx):
        return ctx

    def get_value(self):
        return self.val

    def print(self, indent):
        print(indent_str("NAME: "+self.val, indent))

class Expr_number(Expr):
    val = None

    def __init__(self, val):
        self.val = float(val)

    def eval(self, ctx):
        return ctx

    def get_value(self):
        return self.val

    def print(self, indent):
        print(indent_str("NUMBER: "+str(self.val), indent))

class Expr_string(Expr):
    val = None

    def __init__(self, val):
        self.val = str(val)

    def eval(self, ctx):
        return ctx

    def get_value(self):
        return self.val

class Expr_binop(Expr):
    left = None
    right = None
    op = None

    result = None

    def __init__(self, left: Expr, op, right: Expr):
        self.left = left
        self.right = right
        self.op = op

    def eval(self, ctx):
        ctx2 = self.left.eval(ctx)
        ctx3 = self.right.eval(ctx2)

        ops = {
            '+': (lambda a,b: a+b)
        }
        self.result = ops[self.op](self.left.get_value(), self.right.get_value())
        
        return ctx3

    def get_value(self):
        return self.result

    def print(self, indent):
        print(indent_str("BinOp:", indent))
        print(indent_str("-left:", indent))
        self.left.print(indent + 1)
        print(indent_str("op: "+self.op, indent))
        print(indent_str("right:", indent))
        self.right.print(indent + 1)



class Args_args_expr(Args):
    args: Args = None
    expr: Expr = None

    cached_value = None

    def __init__(self, args: Args, expr: Expr):
        self.args = args
        self.expr = expr

    def eval(self, ctx):
        ctx2 = self.args.eval(ctx)
        ctx3 = self.expr.eval(ctx2)
        self.cached_value = self.args.get_values()[:].append(self.expr.get_value())
        return ctx3
    
    def get_values(self):
        if self.cached_value == None:
            print("ERROR: RAN get_values FOR ARGS BEFORE EVALING THEM")
            return None
        
        return self.cached_value

class Args_expr(Args):
    expr: Expr = None

    cached_value = None

    def __init__(self, expr: Expr):
        self.expr = expr
    
    def eval(self, ctx):
        ctx2 = self.expr.eval(ctx)
        self.cached_value = [self.expr.get_value()] #argument values provided as list
        return ctx2

    def get_values(self):
        if self.cached_value == None:
            print("ERROR: RAN get_values FOR ARGS BEFORE EVALING THEM")
            return None

        return self.cached_value

class RefExpr_function_call(RefExpr):
    ref_id = None
    args = None

    arg_val_cache = None
    result_cache = None

    def __init__(self, name: Name, args: Args):
        self.ref_id = name
        self.args = args

    def eval(self, ctx):
        ctx2 = self.args.eval(ctx)
        self.arg_val_cache = self.args.get_values()
        #look up function of name self.name in ctx function table
        if ctx2.function_table.has(self.name.get_value()):
            #eval the found function with the given args
            pass
        else:
            self.result_cache = None #ctx2.vars.get(self.name.get_value()).get_value()

        return ctx2

class RefExpr_name(RefExpr):
    ref_id = None
    val = None

    def __init__(self, name: Name):
        self.ref_id = name

    def eval(self, ctx):
        self.val = ctx.get_var(self.ref_id.get_value())
        return ctx
    
    def get_value(self):
        return self.val
    
    def get_name(self):
        return self.ref_id.get_value()

    def print(self, indent):
        print(indent_str("RefExpr_name:", indent))
        self.ref_id.print(indent + 1)
        

