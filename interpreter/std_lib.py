from random import randrange

fn_table = {}

print_fn = lambda x: print(x[0])
fn_table['print'] = print_fn

sum_fn = lambda x: sum(x[0])
fn_table['sum'] = sum_fn

str_fn = lambda x: str(x[0])
fn_table['str'] = str_fn

randi_fn = lambda x: randrange(x[0], x[1])
fn_table['randi'] = randi_fn

size_fn = lambda x: len(x[0])
fn_table['size'] = size_fn
