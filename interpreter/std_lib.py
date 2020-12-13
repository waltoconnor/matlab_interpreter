from random import randrange

fn_table = {}

part of mclass FuncTypeTable:
    def __init__(self):
        self.func_ttable = {}

    def set_type(self, var, arg_type_str, res_type_str):
    def set_type(self, var, arg_type_str, res_type_str):
        if var in self.func_ttable:
            if self.func_ttable[var][0] != arg_type_str or self.func_ttable[var][1] != restype_str:
                return False

        self.func_ttable[var][0] = arg_type_str
        self.func_ttable[var][1] = res_type_str
        return True

    def get_func_param_type(self, var):
        return self.func_ttable[var][0]

    def get_func_res_type(self, var):
        return self.func_ttable[var][1]


fn_type_table = FuncTypeTable()

print_fn = lambda x: print(x[0])
fn_table['print'] = print_fn
fn_type_table.set_type('print', (1, 1, "STRING"), (1, 1, "STRING"))

sum_fn = lambda x: sum(x[0])
fn_table['sum'] = sum_fn
# TODO: need to differentiate for FLOAT
fn_type_table.set_type('sum', (1, 1, "INT"), (1, 1, "INT"))

str_fn = lambda x: str(x[0])
fn_table['str'] = str_fn
fn_type_table.set_type('print', (1, 1, "STRING"), (1, 1, "STRING"))

randi_fn = lambda x: randrange(x[0], x[1])
fn_table['randi'] = randi_fn
fn_type_table.set_type('sum', (1, 2, "INT"), (1, 1, "INT"))

size_fn = lambda x: len(x[0])
fn_table['size'] = size_fn
fn_type_table.set_type('sum', (1, 1, "INT"), (1, 1, "INT"))
