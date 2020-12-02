

fn_table = {}

print_fn = lambda x: print(x[0])
fn_table['print'] = print_fn

sum_fn = lambda x: sum(x[0])
fn_table['sum'] = sum_fn

str_fn = lambda x: str(x[0])
fn_table['str'] = str_fn

