from ast_abstract_classes import *
from std_lib import fn_table, fn_type_table

global_type_table = None

class TypeTable:

    def __init__(self):
        self.ttable = {}
        self.function_types = fn_type_table
    
    def get_function_types(self):
        return self.function_types

    def set_type(self, var, type_str):
        print("Setting variable {} to type {}".format(var, str(type_str)))
        
        if var in self.ttable.keys():
            print("old value {}".format(self.ttable[var]))
            if self.ttable[var] != type_str and self.ttable[var] != None:
                return False
                
        self.ttable[var] = type_str
        return True

    def type_compatible(self, var, type_str):
        return self.ttable[var] == type_str

    def get_type(self, var):
        return self.ttable[var]

    def has_type(self, var):
        return var in self.ttable

    def get_fn_parameter_type(self, name):
        return self.function_types.get_func_param_type(name)

    def get_fn_type(self, name):
        return self.function_types.get_func_res_type(name)

    def fn_type_compatible(self, fn_name, param_type, res_type):
        return param_type == self.get_fn_parameter_type(fn_name) \
                and res_type == self.get_fn_type(fn_name)
   
class Context:

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

    def __init__(self, statements: Statements):
        self.statements = statements
    
    def eval(self, ctx):
        global global_type_table
        final_ctx = self.statements.eval(ctx)
        print("FINAL TYPE TABLE:")
        print(global_type_table.ttable)
        return final_ctx

    def print(self):
        print("Program: ")
        self.statements.print(1)

    def typecheck(self, type_table):
        global global_type_table 
        global_type_table = self.statements.typecheck(type_table)
        return global_type_table

class Statements_stmt_stmts(Statements):

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

    def typecheck(self, type_table):
        tt2 = self.head.typecheck(type_table)
        if tt2 is None:
            return None
        return self.tail.typecheck(tt2)



class Statements_stmts_stmt(Statements):

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

    def typecheck(self, type_table):
        tt2 = self.head.typecheck(self, type_table)
        if tt2 is None:
            return None
        return self.tail.typecheck(tt2)

class Statements_stmt(Statements):

    def __init__(self, stmt: Statement):
        self.head = stmt
    
    def eval(self, ctx):
        return self.head.eval(ctx)
    
    def print(self, indent):
        print(indent_str("Statements:", indent))
        print(indent_str("-statement:", indent))
        self.head.print(indent + 1)
    
    def typecheck(self, type_table):
        return self.head.typecheck(type_table)

class Statement_empty(Statement):
    def __init__(self):
        pass

    def eval(self, ctx):
        return ctx

    def print(self, indent):
        pass
    
    def typecheck(self, type_table):
        return type_table

class Statement_expr(Statement):

    def __init__(self, expr: Expr):
        self.expr = expr

    def eval(self, ctx):
        #TODO: store result of last expr
        return self.expr.eval(ctx)

    def print(self, indent):
        print(indent_str("Statement_expr:", indent))
        print(indent_str("-expr:", indent))
        self.expr.print(indent + 1)
    
    def typecheck(self, type_table):
        return self.expr.typecheck(type_table)

class Statement_assign(Statement):
    
    def __init__(self, assign: Assign):
        self.assign = assign
    
    def eval(self, ctx):
        return self.assign.eval(ctx)

    def print(self, indent):
        print(indent_str("Statement:", indent))
        print(indent_str("-assign:", indent))
        self.assign.print(indent + 1)
    
    def typecheck(self, type_table):
        return self.assign.typecheck(type_table)

class Assign_ref_exp(Assign):
    
    def __init__(self, ref: RefExpr, expr: Expr):
        self.ref = ref
        self.expr = expr
        self.ref_cache = None
        self.expr_cache = None


    def eval(self, ctx):
        global global_type_table
        ctx2 = self.ref.eval(ctx)
        self.ref_cache = self.ref.get_name()
        ctx3 = self.expr.eval(ctx2)
        self.expr_cache = self.expr.get_value()
        ctx4 = self.ref.set_value(ctx3, self.expr_cache)
        global_type_table.set_type(self.ref.get_name(), self.expr.get_type(global_type_table))
        return ctx4
    
    def get_ref(self):
        if self.ref_cache == None:
            print("ERROR, GET REF RUN FOR ASSIGN THAT HASNT BEEN EVALD YET")
            return None

        return self.ref_cache

    def get_value(self):
        if self.expr_cache == None:
            print("ERROR, GET VALUE RUN FOR ASSIGN THAT HASNT BEEN EVALD YET")
            return None
        
        return self.expr_cache

    def print(self, indent):
        print(indent_str("Assign:", indent))
        print(indent_str("-ref:", indent))
        self.ref.print(indent + 1)
        print(indent_str("-expr:", indent))
        self.expr.print(indent + 1)

    def typecheck(self, type_table):
        self.expr.typecheck(type_table)
        if type_table.set_type(self.ref.get_name(), self.expr.get_type(type_table)):
            return type_table
        else:
            print("ASSIGN ERROR (TODO: WRITE OUT ERROR)")
            return None


class Statement_for(Statement):

    def __init__(self, assign: Assign, stmts: Statements):
        self.index_var = None
        self.range_vals = None
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

    def __init__(self, val):
        self.val = val

    def eval(self, ctx):
        return ctx

    def get_value(self):
        return self.val

    def print(self, indent):
        print(indent_str("NAME: "+self.val, indent))

    def typecheck(self, type_table):
        return type_table
    
    def get_type(self, type_table):
        return type_table.get_type(self.val)

class Expr_number(Expr):
    
    def __init__(self, val):
        if "." in val:
            self.val = float(val)
            self.v_type = (1, 1, "FLOAT")

        elif "." not in val:
            self.val = int(val)
            self.v_type = (1, 1, "INT")

    def eval(self, ctx):
        return ctx

    def get_value(self):
        return self.val

    def print(self, indent):
        print(indent_str("NUMBER: "+str(self.val), indent))

    def typecheck(self, type_table):
        return type_table
    
    def get_type(self, type_table):
        return self.v_type

class Expr_string(Expr):
    
    def __init__(self, val):
        self.val = str(val)
        self.v_type = (1, 1, "STRING")

    def eval(self, ctx):
        return ctx

    def get_value(self):
        return self.val

    def print(self, indent):
        print(indent_str("STRING: "+self.val, indent))

    def typecheck(self, type_table):
        return type_table
    
    def get_type(self, type_table):
        return self.v_type

class Expr_binop(Expr):
    op_types = {        'comparison' : set(["<", "<=", ">", ">=", "~=", "=="]),
                        'arithmetic' : set(["+", "-", "*", "/"]),
                           'logical' : set(["||", "&&"]),
                'matrix_commutative' : set(["+", "-", ".*", "./"])}
    
    def __init__(self, left: Expr, op, right: Expr):
        self.left = left
        self.right = right
        self.op = op
        self.result = None
        self.v_type = None
    
    def eval(self, ctx):
        global global_type_table
        ctx2 = self.left.eval(ctx)
        ctx3 = self.right.eval(ctx2)

        scalar_ops = {
            '+': (lambda a,b: a + b),
            '-': (lambda a,b: a - b),
            '*': (lambda a,b: a * b),
            '/': (lambda a,b: a / b),
            '<': (lambda a,b: 1 if a < b else 0),
            '>': (lambda a,b: 1 if a > b else 0),
            '<=': (lambda a,b: 1 if a <= b else 0),
            '>=': (lambda a,b: 1 if a >= b else 0),
            '==': (lambda a,b: 1 if a == b else 0),
            '~=': (lambda a,b: 1 if a != b else 0),
            '||': (lambda a,b: 1 if a == 1 or b == 1 else 0),
            '&&': (lambda a,b: 1 if a == 1 and b == 1 else 0)
        }

        scalar_matrix_ops = {
             '+': (lambda a,B: [[a + B[i][j] for j in range(len(B[0]))] for i in range(len(B))]),
            '.+': (lambda a,B: [[a + B[i][j] for j in range(len(B[0]))] for i in range(len(B))]),
             '-': (lambda a,B: [[a - B[i][j] for j in range(len(B[0]))] for i in range(len(B))]),
            '.-': (lambda a,B: [[a - B[i][j] for j in range(len(B[0]))] for i in range(len(B))]),
             '*': (lambda a,B: [[a * B[i][j] for j in range(len(B[0]))] for i in range(len(B))]),
            '.*': (lambda a,B: [[a * B[i][j] for j in range(len(B[0]))] for i in range(len(B))]),
             '/': (lambda a,B: [[a / B[i][j] for j in range(len(B[0]))] for i in range(len(B))]),
            './': (lambda a,B: [[a / B[i][j] for j in range(len(B[0]))] for i in range(len(B))]),
            
        }

        matrix_scalar_ops = {
             '+': (lambda A,b: [[A[i][j] + b for j in range(len(A[0]))] for i in range(len(A))]),
            '.+': (lambda A,b: [[A[i][j] + b for j in range(len(A[0]))] for i in range(len(A))]),
             '-': (lambda A,b: [[A[i][j] - b for j in range(len(A[0]))] for i in range(len(A))]),
            '.-': (lambda A,b: [[A[i][j] - b for j in range(len(A[0]))] for i in range(len(A))]),
             '/': (lambda A,b: [[A[i][j] / b for j in range(len(A[0]))] for i in range(len(A))]),
            './': (lambda A,b: [[A[i][j] / b for j in range(len(A[0]))] for i in range(len(A))]),
             '*': (lambda A,b: [[A[i][j] * b for j in range(len(A[0]))] for i in range(len(A))]),
            '.*': (lambda A,b: [[A[i][j] * b for j in range(len(A[0]))] for i in range(len(A))]),
        }

        matrix_ops = {
             '+': (lambda A,B: [[A[i][j] + B[i][j] for j in range(len(A[0]))] for i in range(len(A))]),
             '-': (lambda A,B: [[A[i][j] - B[i][j] for j in range(len(A[0]))] for i in range(len(A))]),
             '*': (lambda A,B: [[sum([x*y for (x, y) in zip(row, col)]) for col in zip(*B)] for row in A]),
            '.*': (lambda A,B: [[A[i][j] * B[i][j] for j in range(len(A[0]))] for i in range(len(A))]),
            './': (lambda A,B: [[A[i][j] / B[i][j] for j in range(len(A[0]))] for i in range(len(A))]),
             '<': (lambda A,B: [[(1 if A[i][j] < B[i][j] else 0) for j in range(len(A[0]))] for i in range(len(A))]),
             '>': (lambda A,B: [[(1 if A[i][j] > B[i][j] else 0) for j in range(len(A[0]))] for i in range(len(A))]),
            '<=': (lambda A,B: [[(1 if A[i][j] <= B[i][j] else 0) for j in range(len(A[0]))] for i in range(len(A))]),
            '>=': (lambda A,B: [[(1 if A[i][j] >= B[i][j] else 0) for j in range(len(A[0]))] for i in range(len(A))]),
            '==': (lambda A,B: [[(1 if A[i][j] == B[i][j] else 0) for j in range(len(A[0]))] for i in range(len(A))]),
            '~=': (lambda A,B: [[(1 if A[i][j] != B[i][j] else 0) for j in range(len(A[0]))] for i in range(len(A))]),
            '||': (lambda A,B: [[(1 if A[i][j] == 1 or B[i][j] == 1 else 0) for j in range(len(A[0]))] for i in range(len(A))]),
            '&&': (lambda A,B: [[(1 if A[i][j] == 1 and  B[i][j] == 1 else 0) for j in range(len(A[0]))] for i in range(len(A))])
        }

        # unpack dimensions and type from left and right expressions    
        print("GLOBAL TYPE TABLE")
        print(global_type_table)
        print("LEFT ", self.left.get_value(), "TYPE ", self.left.get_type(global_type_table))
        print("RIGHT ", self.right.get_value(), "TYPE ", self.right.get_type(global_type_table))

        left_m, left_n, left_type = self.left.get_type(global_type_table)
        right_m, right_n, right_type = self.right.get_type(global_type_table)

        # Scalar to scalar operations
        if left_m == left_n == right_m == right_n == 1:
            self.result = scalar_ops[self.op](self.left.get_value(), self.right.get_value())
            self.v_type = (left_m, left_n, self.v_type[2])      
            
        
        # Commutative matrix operations
        elif left_m == right_m \
            and left_n == right_n \
            and self.op not in ["*", "/"]:

            self.result = matrix_ops[self.op](self.left.get_value(), self.right.get_value())
            self.v_type = (left_m, left_n, self.v_type[2])        

        # Matrix multiplication
        elif left_n == right_m \
            and self.op == "*":

            self.result = matrix_ops[self.op](self.left.get_value(), self.right.get_value())
            self.v_type = (left_m, right_n, self.v_type[2])        

        # Scalar/matrix math
        elif left_n == right_n == 1:
            self.result = scalar_matrix_ops[self.op](self.left.get_value(), self.right.get_value())
            self.v_type = (right_m, right_n, self.v_type[2])        

        # matrix/scalar math
        elif right_m == right_n == 1:
            self.result = matrix_scalar_ops[self.op](self.left.get_value(), self.right.get_value())
            self.v_type = (left_m, left_n, self.v_type[2])
        
        else:
            print("TYPE ERROR, cannot compute operation: {} on {}x{} {} with {}x{} {}".format(self.op, left_m, left_n, left_type, right_m, right_n, right_type))
        
        if self.op in self.op_types['comparison'] or self.op in self.op_types['logical']:
            self.v_type = (1, 1, "INT")

        print("V_TYPE")
        print(self.v_type)  
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

    def typecheck(self, type_table):
        
        left_type = self.left.get_type(global_type_table)
        right_type = self.right.get_type(global_type_table)

        # Make sure we don't mix string and numeric types.
        if left_type is not None and right_type is not None:
            if left_type[2] == "FLOAT" or right_type[2] == "FLOAT":
                if left_type[2] == "STRING" or right_type[2] == "STRING":
                    return None
                else:
                    self.v_type = (1, 1, "FLOAT")
                    return self.v_type

            elif left_type[2] == "INT" or right_type[2] == "INT":
                self.vtype = (1, 1, "INT")
                return self.vtype

        # If one arg is None, cast the result as the known type. 
        elif left_type is None or right_type is None:
            if left_type[2] == "FLOAT" or right_type[2] == "FLOAT":
                self.vtype = (1, 1, "FLOAT")
                return self.vtype

            elif left_type[2] == "INT" or right_type[2] == "INT":
                self.vtype = (1, 1, "INT")
                return self.vtype

            elif left_type[2] == "STRING" or right_type[2] == "STRING":
                self.vtype = (1, 1, "STRING")
                return self.vtype

        # If both types are unknown cast as (1, 1, "INT")
        else: # Left and Right are None
            self.vtype = (1, 1, "INT")
            return self.vtype
    
    def get_type(self, type_table):
        return self.v_type

    def typecheck(self, type_table):
        left_type = self.left.get_type(type_table)
        right_type = self.right.get_type(type_table)
        if left_type is not None and right_type is not None:
            if left_type[2] == "FLOAT" or right_type[2] == "FLOAT":
                if left_type[2] == "STRING" or right_type[2] == "STRING":
                    print("INCOMPATIBLE TYPES IN BINOP {} {} {}", left_type[2], self.op, right_type[2])
                    return None
                else:
                    return (1, 1, "FLOAT")
            if left_type[2] == "INT" or right_type[2] == "INT":
                return (1, 1, "INT")
        elif left_type is None or right_type is None:
            if left_type[2] == "FLOAT" or right_type[2] == "FLOAT":
                return (1, 1, "FLOAT")
            elif left_type[2] == "INT" or right_type[2] == "INT":
                return (1, 1, "INT")
            elif left_type[2] == "STRING" or right_type[2] == "STRING":
                return (1, 1, "STRING")
        else: # Left and Right are None
            return (1, 1, "INT")


class Args_args_expr(Args):
    
    def __init__(self, args: Args, expr: Expr):
        self.args = args
        self.expr = expr
        self.cached_value = None

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
    
    def __init__(self, expr: Expr):
        self.expr = expr
        self.cached_value = None

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

    def typecheck(self, type_table):
        return self.expr.typecheck(type_table)

class RefExpr_function_call(RefExpr):

    def __init__(self, name: Name, args: Args):
        self.ref_id = name
        self.args = args
        self.args_val_cache = None
        self.is_array = False

    def eval(self, ctx):
        ctx2 = self.args.eval(ctx) if self.args != None else ctx
        self.args_val_cache = self.args.get_values()
        #look up function of name self.name in ctx function table
        
        if ctx2.has_fn(self.ref_id):
            fn = ctx2.get_fn(self.ref_id)
            self.result_cache = fn(self.args_val_cache)
            self.is_array = False
            
        else:
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

    def typecheck(self, type_table):
        fn_types = type_table.get_function_types()

        if self.ref_id in fn_types:
            type_table.set_type(self.ref_id, type_table.get_fn_type(self.ref_id))
            return type_table
        else: 
            ## TODO, assign get array dimensions and add to the type table.

            type_table.set_type(self.ref_id, ())

            indexes = self.args_val_cache
            cur_arr = ctx.search_stack(self.ref_id)
            temp_arr = cur_arr
            for i in range(0, len(indexes) - 1):
                temp_arr = temp_arr[int(indexes[i])]

            self.result_cache = temp_arr[int(indexes[-1])]


class RefExpr_name(RefExpr):
    # Variable access 

    def __init__(self, name: Name):
        self.ref_id = name
        self.val = None
        self.v_type = None

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

    def get_type(self, type_table):
        print("Searching type table for: ", self.ref_id.get_value())
        if type_table.has_type(self.ref_id.get_value()):
            print("Found ", self.ref_id.get_value(), "type is ", type_table.get_type(self.ref_id.get_value()))
            return type_table.get_type(self.ref_id.get_value())
        else:
            print("Could not Find ", self.ref_id.get_value())
            return None

    def typecheck(self, type_table):
        return type_table



        

class ArrayVals_expr(ArrayVals):
    
    def __init__(self, expr: Expr):
        self.expr = expr
        self.result_cache = None
        self.array_type = None
            
    def eval(self, ctx):
        ctx2 = self.expr.eval(ctx)
        self.result_cache = self.expr.get_value()

        return ctx2
    
    def get_values(self):
        return [self.result_cache]

    def get_width(self):
        return 1

    def get_head_type(self, type_table):
        return self.expr.get_type(type_table)
    
    def print(self, indent):
        print(indent_str("ArrayVal expr:", indent))
        self.expr.print(indent + 1)
    
    def typecheck(self, type_table):
        return type_table

class ArrayVals_expr_array_vals(ArrayVals):
    
    def __init__(self, expr: Expr, array_vals: ArrayVals):
        self.expr = expr 
        self.array_vals = array_vals
        self.array_type = None
        self.result_cache = []
    
    def eval(self, ctx):
        ctx2 = self.expr.eval(ctx)
        ctx3 = self.array_vals.eval(ctx2)

        self.result_cache = [self.expr.get_value()] + self.array_vals.get_values()

        return ctx3
    
    def get_values(self):
        return self.result_cache

    def get_width(self):
        return 1 + self.array_vals.get_width()

    def get_head_type(self, type_table):
        return self.expr.get_type(type_table)
    
    def print(self, indent):
        print(indent_str("ArrayVal expr:", indent))
        print(indent_str("-head:", indent))
        self.expr.print(indent + 1)
        print(indent_str("-tail:", indent))
        self.array_vals.print(indent + 1)
    
    def typecheck(self, type_table):
        tt1 = self.expr.typecheck(type_table)
        return self.array_vals.typecheck(tt1)

class ArrayLiteral(Expr):
    
    def __init__(self, values: ArrayVals):
        self.array_vals = values
        self.result_cache = None

    def eval(self, ctx):
        ctx2 = self.array_vals.eval(ctx)
        self.result_cache = self.array_vals.get_values()
        return ctx2
    
    def get_value(self):
        return self.result_cache

    def get_size(self):
        return (self.v_type[0], self.v_type[1])

    def print(self, indent):
        print(indent_str("ArrayLiteral:", indent))
        self.array_vals.print(indent + 1)

    def get_type(self, type_table):
        return (1, self.array_vals.get_width(), self.array_vals.get_head_type(type_table)[2])

    def typecheck(self, type_table):
        return self.array_vals.typecheck(type_table)

class IfStatement_no_else(IfStatement):

    def __init__(self, cond, tblock):
        self.cond = cond
        self.tblock = tblock
    
    def eval(self, ctx):
        global global_type_table
        ctx2 = self.cond.eval(ctx)
        ctx3 = ctx2
        cond_type = self.cond.get_type(global_type_table)
        if cond_type is not "INT":
            print("If statement provided with {} instead of conditional returning an integer".format(cond_type))
            return None

        if self.cond.get_value() > 0: #0 is false, other is true
            ctx3 = self.tblock.eval(ctx2)
        
        return ctx3
    
    def print(self, indent):
        print(indent_str("If no else:", indent))
        print(indent_str("-condition:", indent))
        self.cond.print(indent + 1)
        print(indent_str("-true block:", indent))
        self.tblock.print(indent + 1)

    def typecheck(self, type_table):
        tt1 = self.cond.typecheck(type_table)
        return self.tblock.typecheck(tt1)
        

class IfStatement_else(IfStatement):

    def __init__(self, cond, tblock, fblock):
        self.cond = cond
        self.tblock = tblock
        self.fblock = fblock
    
    def eval(self, ctx):
        global global_type_table
        ctx2 = self.cond.eval(ctx)
        ctx3 = ctx2
        cond_type = self.cond.get_type(global_type_table)
        if cond_type is not "INT":
            print("If statement provided with {} instead of conditional returning an integer".format(cond_type))
            return None

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

    def typecheck(self, type_table):
        tt1 = self.cond.typecheck(type_table)
        tt2 = self.tblock.typecheck(tt1)
        return self.fblock.typecheck(tt2)

class IfStatement_elseif(IfStatement):

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

    def typecheck(self, type_table):
        tt1 = self.cond.typecheck(type_table)
        cond_type = self.cond.get_type(tt1)
        if cond_type is not "INT":
            print("If statement provided with {} instead of conditional returning an integer".format(cond_type))
            return None
        else:
            tt2 = self.tblock.typecheck(tt1)
            return self.elseif.typecheck(tt2)

class Elseif_elseif:

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

    def typecheck(self, type_table):
        tt1 = self.cond.typecheck(type_table)
        cond_type = self.cond.get_type(tt1)
        if cond_type is not "INT":
            print("Elseif statement provided with {} instead of conditional returning an integer".format(cond_type))
            return None
        else:
            tt2 = self.tblock.typecheck(tt1)
            return self.elseif.typecheck(tt2)

class Elseif_else:

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

    def typecheck(self, type_table):
        tt1 = self.cond.typecheck(type_table)
        cond_type = self.cond.get_type(tt1)
        if cond_type is not "INT":
            print("Elseif statement provided with {} instead of conditional returning an integer".format(cond_type))
            return None
        else:
            tt2 = self.tblock.typecheck(tt1)
            return self.fblock.typecheck(tt2)

class ArrayColon(Expr):
    
    def __init__(self, left, right):
        self.left = left
        self.right = right
        self.val_cache = []
        self.v_type = (1, 1, "INT")

    def eval(self, ctx):
        ctx2 = self.left.eval(ctx)
        ctx3 = self.right.eval(ctx2)

        self.val_cache = list(range(int(self.left.get_value()), int(self.right.get_value())))
        self.v_type = (1, len(self.val_cache), "INT")
        return ctx3
    
    def get_value(self):
        return self.val_cache

    def get_width(self):
        return len(self.val_cache)
    
    def print(self, indent):
        print(indent_str("ArrayLiteral colon:", indent))
        print(indent_str("-left:", indent))
        self.left.print(indent + 1)
        print(indent_str("-right:", indent))
        self.right.print(indent + 1)

    def get_type(self, type_table):
        return self.v_type

    def typecheck(self, type_table):
        tt1 = self.left.typecheck(type_table)
        return self.right.typecheck(tt1)

class MatrixRowInner_arr_vals(MatrixRowInner):
    
    def __init__(self, arr_vals):
        self.arr_vals = arr_vals
        self.val_cache = None

    def eval(self, ctx):
        ctx2 = self.arr_vals.eval(ctx)
        self.val_cache = [self.arr_vals.get_values()]
        return ctx2
    
    def get_values(self):
        return self.val_cache
    
    def get_height(self):
        return 1
    
    def print(self, indent):
        print(indent_str("Matrix Row arr vals:", indent))
        print(indent_str("-arr vals:", indent))
        self.arr_vals.print(indent + 1)

    def typecheck(self, type_table):
        return self.arr_vals.typecheck(type_table)


class MatrixRowInner_mri_arr_vals(MatrixRowInner):

    def __init__(self, head, arr_vals):
        self.arr_vals = arr_vals
        self.mri_head = head
        self.val_cache = None

    def eval(self, ctx):
        ctx2 = self.mri_head.eval(ctx)
        ctx3 = self.arr_vals.eval(ctx2)
        self.val_cache = self.mri_head.get_values() + [self.arr_vals.get_values()]
        return ctx3
    
    def get_values(self):
        return self.val_cache

    def get_height(self):
        return 1 + self.mri_head.get_height()
    
    def print(self, indent):
        print(indent_str("Matrix Row mri arr vals:", indent))
        print(indent_str("-mri_head:", indent))
        self.mri_head.print(indent + 1)
        print(indent_str("-arr vals:", indent))
        self.arr_vals.print(indent + 1)

    def typecheck(self, type_table):
        tt1 = self.mri_head.typecheck(type_table)
        return self.arr_vals.typecheck(tt1)
        

class MatrixLiteral:

    def __init__(self, head, arr_vals):
        self.arr_vals = arr_vals
        self.mri_head = head
        self.val_cache = None
        self.v_type = (1,1,"INT")

    def eval(self, ctx):
        ctx2 = self.mri_head.eval(ctx)
        ctx3 = self.arr_vals.eval(ctx2)
        self.val_cache = self.mri_head.get_values() + [self.arr_vals.get_values()]
        return ctx3
    
    def get_value(self):
        return self.val_cache

    def get_type(self, type_table):
        self.v_type = ((self.mri_head.get_height() + 1), self.arr_vals.get_width(), self.arr_vals.expr.get_type(type_table)[2])
        return self.v_type
        
    
    def print(self, indent):
        print(indent_str("Matrix Row mri arr vals:", indent))
        print(indent_str("-mri_head:", indent))
        self.mri_head.print(indent + 1)
        print(indent_str("-arr vals:", indent))
        self.arr_vals.print(indent + 1)

    def typecheck(self, type_table):
        tt1 = self.mri_head.typecheck(type_table)
        return self.arr_vals.typecheck(type_table)