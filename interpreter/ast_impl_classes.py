from ast_abstract_classes import *
from std_lib import fn_table 

class Context:
    frames = None
    functions = fn_table

    def __init__(self):
        self.frames = [{}]
        self.function_table = fn_table

    def search_stack(self, name):
        for f in reversed(self.frames):
            if name in f.keys():
                return f[name]
        
        return None
    
    def update_stack(self, name, value):
        #if the value already exists on the stack, update it
        for f in reversed(self.frames):
            if name in f.keys():
                f[name] = value
        
        #otherwise add it to the current frame
        self.frames[-1][name] = value

    def clear_var_in_frame(self, name):
        del self.frames[-1][name]

    def push_frame(self):
        self.frames.append({})
    
    def pop_frame(self):
        self.frames.pop(-1)

    def get_fn(self, name):
        return self.function_table[name]
    
    def has_fn(self, name):
        return name in self.function_table

    def print(self):
        print("frames (bottom to top):")
        for i, f in enumerate(self.frames):
            print("===== frame {} ======".format(i))
            for k, v in f.items():
                print("  {} = {}".format(k, v))

        print("function_table:")
        for k, v in self.function_table.items():
            print("  {}: {}".format(k, v))

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
        ctx4 = self.ref.set_value(ctx3, self.expr_cache)
        return ctx4
    
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

        ctx2.clear_var_in_frame(self.index_var)
        #at this point, the variable from the assign is set to the iteration range in ctx2, we need to overwrite that

        for elem in self.range_vals:
            ctx2.push_frame()
            ctx2.update_stack(self.index_var, elem)
            ctx2 = self.statements.eval(ctx2) #handle it like this to allow accumulators in the loop
            ctx2.pop_frame()

        return ctx2 

    def print(self, indent):
        print(indent_str("For Loop (var = {}):".format(self.index_var), indent))
        print(indent_str("-assign:", indent))
        self.assign.print(indent+1)
        print(indent_str("-body:", indent))
        self.statements.print(indent+1)


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

    def print(self, indent):
        print(indent_str("STRING: "+self.val, indent))

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
            '+': (lambda a,b: a+b),
            '-': (lambda a,b: a-b),
            '*': (lambda a,b: a*b),
            '/': (lambda a,b: a/b),
            '<': (lambda a,b: 1 if a < b else 0),
            '>': (lambda a,b: 1 if a > b else 0),
            '<=': (lambda a,b: 1 if a <= b else 0),
            '>=': (lambda a,b: 1 if a >= b else 0),
            '==': (lambda a,b: 1 if a == b else 0),
            '~=': (lambda a,b: 1 if a != b else 0),
            '||': (lambda a,b: 1 if a == 1 or b == 1 else 0),
            '&&': (lambda a,b: 1 if a == 1 and b == 1 else 0)
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
        self.cached_value = self.args.get_values() + [self.expr.get_value()]
        return ctx3
    
    def get_values(self):
        if self.cached_value == None:
            print("ERROR: RAN get_values FOR ARGS BEFORE EVALING THEM")
            return None
        
        return self.cached_value

    def print(self, indent):
        print(indent_str("args_head: ", indent))
        self.args.print(indent + 1)
        print(indent_str("arg_tail: ", indent))
        self.expr.print(indent + 1)

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

    def print(self, indent):
        print(indent_str("arg: ", indent))
        self.expr.print(indent + 1)

class RefExpr_function_call(RefExpr):
    ref_id = None
    args = None

    args_val_cache = None
    result_cache = None

    is_array = False

    def __init__(self, name: Name, args: Args):
        self.ref_id = name
        self.args = args

    def eval(self, ctx):
        ctx2 = self.args.eval(ctx) if self.args != None else ctx
        self.args_val_cache = self.args.get_values()
        #look up function of name self.name in ctx function table
        
        if ctx2.has_fn(self.ref_id):
            fn = ctx2.get_fn(self.ref_id)
            self.result_cache = fn(self.args_val_cache)
            self.is_array = False
            
        else:
            arr = ctx2.search_stack(self.ref_id)
            self.is_array = True

            indexes = self.args_val_cache
            cur_arr = ctx.search_stack(self.ref_id)
            temp_arr = cur_arr
            for i in range(0, len(indexes) - 1):
                temp_arr = temp_arr[int(indexes[i])]

            self.result_cache = temp_arr[int(indexes[-1])]

        return ctx2

    def get_value(self):
        return self.result_cache
    
    def set_value(self, ctx, value):
        if self.is_array is False:
            print("ERROR: TRIED TO SET VALUE OF FUNCTION EVALUATION")
            return ctx
        
        #if we are here, we need to set an array value
        indexes = self.args_val_cache
        cur_arr = ctx.search_stack(self.ref_id)
        temp_arr = cur_arr
        for i in range(0, len(indexes) - 1):
            temp_arr = temp_arr[int(indexes[i])]

        temp_arr[int(indexes[-1])] = value
        return ctx

    def get_name(self):
        return self.ref_id
    
    def print(self, indent):
        print(indent_str("function_call: "+self.ref_id, indent))
        #print(indent_str("-name:", indent))
        #self.ref_id.print(indent + 1)
        print(indent_str("-args:", indent))
        self.args.print(indent + 1)


class RefExpr_name(RefExpr):
    ref_id = None
    val = None

    def __init__(self, name: Name):
        self.ref_id = name

    def eval(self, ctx):
        self.val = ctx.search_stack(self.ref_id.get_value())
        return ctx
    
    def get_value(self):
        return self.val
    
    def get_name(self):
        return self.ref_id.get_value()

    def set_value(self, ctx, value):
        ctx.update_stack(self.get_name(), value)
        return ctx

    def print(self, indent):
        print(indent_str("RefExpr_name:", indent))
        self.ref_id.print(indent + 1)
        

class ArrayVals_expr(ArrayVals):
    expr = None
    result_cache = None

    def __init__(self, expr: Expr):
        self.expr = expr
    
    def eval(self, ctx):
        ctx2 = self.expr.eval(ctx)
        self.result_cache = self.expr.get_value()

        return ctx2
    
    def get_values(self):
        return [self.result_cache]
    
    def print(self, indent):
        print(indent_str("ArrayVal expr:", indent))
        self.expr.print(indent + 1)

class ArrayVals_expr_array_vals(ArrayVals):
    expr = None
    array_vals: ArrayVals = None

    result_cache = None

    def __init__(self, expr: Expr, array_vals: ArrayVals):
        self.expr = expr
        self.array_vals = array_vals
    
    def eval(self, ctx):
        ctx2 = self.expr.eval(ctx)
        ctx3 = self.array_vals.eval(ctx2)

        self.result_cache = [self.expr.get_value()] + self.array_vals.get_values()

        return ctx3
    
    def get_values(self):
        return self.result_cache
    
    def print(self, indent):
        print(indent_str("ArrayVal expr:", indent))
        print(indent_str("-head:", indent))
        self.expr.print(indent + 1)
        print(indent_str("-tail:", indent))
        self.array_vals.print(indent + 1)

class ArrayLiteral:
    array_vals = None
    result_cache = None

    def __init__(self, values: ArrayVals):
        self.array_vals = values
    
    def eval(self, ctx):
        ctx2 = self.array_vals.eval(ctx)
        self.result_cache = self.array_vals.get_values()
        return ctx2
    
    def get_value(self):
        return self.result_cache
    
    def print(self, indent):
        print(indent_str("ArrayLiteral:", indent))
        self.array_vals.print(indent + 1)

class IfStatement_no_else(IfStatement):
    cond = None
    tblock = None

    def __init__(self, cond, tblock):
        self.cond = cond
        self.tblock = tblock
    
    def eval(self, ctx):
        ctx2 = self.cond.eval(ctx)
        ctx3 = ctx2
        if self.cond.get_value() > 0: #0 is false, other is true
            ctx3 = self.tblock.eval(ctx2)
        
        return ctx3
    
    def print(self, indent):
        print(indent_str("If no else:", indent))
        print(indent_str("-condition:", indent))
        self.cond.print(indent + 1)
        print(indent_str("-true block:", indent))
        self.tblock.print(indent + 1)
        

class IfStatement_else(IfStatement):
    cond = None
    tblock = None
    fblock = None

    def __init__(self, cond, tblock, fblock):
        self.cond = cond
        self.tblock = tblock
        self.fblock = fblock
    
    def eval(self, ctx):
        ctx2 = self.cond.eval(ctx)
        ctx3 = ctx2
        if self.cond.get_value() > 0: #0 is false, other is true
            ctx3 = self.tblock.eval(ctx2)
        else:
            ctx3 = self.fblock.eval(ctx2)
        
        return ctx3
    
    def print(self, indent):
        print(indent_str("If else:", indent))
        print(indent_str("-condition:", indent))
        self.cond.print(indent + 1)
        print(indent_str("-true block:", indent))
        self.tblock.print(indent + 1)
        print(indent_str("-false block:", indent))
        self.fblock.print(indent + 1)

class IfStatement_elseif(IfStatement):
    cond = None
    tblock = None
    elseif = None

    def __init__(self, cond, tblock, elseif):
        self.cond = cond
        self.tblock = tblock
        self.elseif = elseif

    def eval(self, ctx):
        ctx2 = self.cond.eval(ctx)
        if self.cond.get_value() > 0:
            return self.tblock.eval(ctx2)
        else:
            return self.elseif.eval(ctx2)

    def print(self, indent):
        print(indent_str("If elseif:", indent))
        print(indent_str("-condition:", indent))
        self.cond.print(indent + 1)
        print(indent_str("-true block:", indent))
        self.tblock.print(indent + 1)
        print(indent_str("-false elseif:", indent))
        self.elseif.print(indent + 1)

class Elseif_elseif:
    cond = None
    tblock = None
    elseif = None

    def __init__(self, cond, tblock, elseif):
        self.cond = cond
        self.tblock = tblock
        self.elseif = elseif

    def eval(self, ctx):
        ctx2 = self.cond.eval(ctx)
        if self.cond.get_value() > 0:
            return self.tblock.eval(ctx2)
        else:
            return self.elseif.eval(ctx2)

    def print(self, indent):
        print(indent_str("Elseif elseif:", indent))
        print(indent_str("-condition:", indent))
        self.cond.print(indent + 1)
        print(indent_str("-true block:", indent))
        self.tblock.print(indent + 1)
        print(indent_str("-false elseif:", indent))
        self.elseif.print(indent + 1)

class Elseif_else:
    cond = None
    tblock = None
    fblock = None

    def __init__(self, cond, tblock, fblock):
        self.cond = cond
        self.tblock = tblock
        self.fblock = fblock
    
    def eval(self, ctx):
        ctx2 = self.cond.eval(ctx)
        ctx3 = ctx2
        if self.cond.get_value() > 0: #0 is false, other is true
            ctx3 = self.tblock.eval(ctx2)
        else:
            ctx3 = self.fblock.eval(ctx2)
        
        return ctx3
    
    def print(self, indent):
        print(indent_str("Elseif else:", indent))
        print(indent_str("-condition:", indent))
        self.cond.print(indent + 1)
        print(indent_str("-true block:", indent))
        self.tblock.print(indent + 1)
        print(indent_str("-false block:", indent))
        self.fblock.print(indent + 1)

class ArrayColon(Expr):
    left = None
    right = None

    val_cache = None

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def eval(self, ctx):
        ctx2 = self.left.eval(ctx)
        ctx3 = self.right.eval(ctx2)

        self.val_cache = list(range(int(self.left.get_value()), int(self.right.get_value())))
        return ctx3
    
    def get_value(self):
        return self.val_cache
    
    def print(self, indent):
        print(indent_str("ArrayLiteral colon:", indent))
        print(indent_str("-left:", indent))
        self.left.print(indent + 1)
        print(indent_str("-right:", indent))
        self.right.print(indent + 1)

class MatrixRowInner_arr_vals(MatrixRowInner):
    arr_vals = None
    val_cache = None

    def __init__(self, arr_vals):
        self.arr_vals = arr_vals

    def eval(self, ctx):
        ctx2 = self.arr_vals.eval(ctx)
        self.val_cache = [self.arr_vals.get_values()]
        return ctx2
    
    def get_values(self):
        return self.val_cache
    
    def print(self, indent):
        print(indent_str("Matrix Row arr vals:", indent))
        print(indent_str("-arr vals:", indent))
        self.arr_vals.print(indent + 1)

class MatrixRowInner_mri_arr_vals(MatrixRowInner):
    mri_head = None
    arr_vals = None
    val_cache = None

    def __init__(self, head, arr_vals):
        self.arr_vals = arr_vals
        self.mri_head = head

    def eval(self, ctx):
        ctx2 = self.mri_head.eval(ctx)
        ctx3 = self.arr_vals.eval(ctx2)
        self.val_cache = self.mri_head.get_values() + [self.arr_vals.get_values()]
        return ctx3
    
    def get_values(self):
        return self.val_cache
    
    def print(self, indent):
        print(indent_str("Matrix Row mri arr vals:", indent))
        print(indent_str("-mri_head:", indent))
        self.mri_head.print(indent + 1)
        print(indent_str("-arr vals:", indent))
        self.arr_vals.print(indent + 1)
        

class MatrixLiteral:
    mri_head = None
    arr_vals = None
    val_cache = None

    def __init__(self, head, arr_vals):
        self.arr_vals = arr_vals
        self.mri_head = head

    def eval(self, ctx):
        ctx2 = self.mri_head.eval(ctx)
        ctx3 = self.arr_vals.eval(ctx2)
        self.val_cache = self.mri_head.get_values() + [self.arr_vals.get_values()]
        return ctx3
    
    def get_value(self):
        return self.val_cache
    
    def print(self, indent):
        print(indent_str("Matrix Row mri arr vals:", indent))
        print(indent_str("-mri_head:", indent))
        self.mri_head.print(indent + 1)
        print(indent_str("-arr vals:", indent))
        self.arr_vals.print(indent + 1)