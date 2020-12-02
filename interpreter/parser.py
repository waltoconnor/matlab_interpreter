import sys
import sly
from lexer import MatlabLexer
import fileinput
from ast_impl_classes import *


#this file is derived from https://github.com/jol-jol/pymatlabparser/blob/master/pymatlabparser/matlab_parser.py
class Parser(sly.Parser):
    debugfile = 'parser_debug.out'

    tokens = MatlabLexer.tokens

    # The official operator precedence for MATLAB is found at
    # https://www.mathworks.com/help/matlab/matlab_prog/operator-precedence.html
    precedence = (
        ('left', ASSIGN),
        ('left', COMMA),
        ('left', OROR),
        ('left', ANDAND),
        ('left', OR),
        ('left', AND),
        ('left', LT, LE, GT, GE, EQ, NE),
        ('left', COLON),
        ('left', PLUS, MINUS),
        ('left', MTIMES, MRDIVIDE, MLDIVIDE, TIMES, RDIVIDE, LDIVIDE),
        ('left', NOT),
        ('left', TRANSPOSE, POWER, CTRANSPOSE, MPOWER),
        ('left', DOT),
    )

    @_("statements")
    def program(self, p):
        return Program(p[0])

    @_("statement statements")
    def statements(self, p):
        return Statements_stmt_stmts(p[0], p[1])

    @_("statements statement")
    def statements(self, p):
        return Statement_stmts_stmt(p[0], p[1])

    @_("statement")
    def statements(self, p):
        return Statements_stmt(p[0])

    @_("statement SEMICOLON", "statement NEWLINE")
    def statement(self, p):
        return p[0]

    @_("SEMICOLON", "NEWLINE")
    def statement(self, p):
        return Statement_empty()

    @_("expr SEMICOLON", "expr NEWLINE")
    def statement(self, p):
        return Statement_expr(p[0])

    @_("FOR assign statements END")
    def statement(self, p):
        return Statement_for(p[1], p[2])
    
    @_("assign")
    def statement(self, p):
        return Statement_assign(p[0])
    
    @_("ref_expr ASSIGN expr")
    def assign(self, p):
        return Assign_ref_exp(p[0], p[2])

    @_("expr COLON expr")
    def expr(self, p):
        return ('array_colon', (('head', p[0]), ('tail', p[2])))

    @_("ref_expr")
    def expr(self, p):
        return p[0]

    @_("NAME")
    def ref_expr(self, p):
        return RefExpr_name(Name(p[0]))

    @_("function_call")
    def ref_expr(self, p):
        return p[0]

    @_("NUMBER")
    def expr(self, p):
        return Expr_number(p[0])

    @_("STRING")
    def expr(self, p):
        return Expr_string(p[0])
    
    @_("PLUS expr", "MINUS expr", "NOT expr")
    def expr(self, p):
        return ('UNARY_PREFIX', (('op', p[0]), ('operand', p[1])))

    @_("NAME LPAREN args RPAREN")
    def function_call(self, p):
        return RefExpr_function_call(p[0], p[2])

    @_("expr LPAREN RPAREN")
    def function_call(self, p):
        return RefExpr_function_call(p[0], None)
    
    @_("args COMMA expr")
    def args(self, p):
        return Args_args_expr(p[0], p[2])
    
    @_("expr")
    def args(self, p):
        return Args_expr(p[0])

    @_('expr OROR expr',    'expr ANDAND expr',     'expr OR expr',     'expr AND expr',
       'expr LT expr',      'expr LE expr',         'expr GT expr',     'expr GE expr',
       'expr EQ expr',      'expr NE expr',         'expr PLUS expr',   'expr MINUS expr',
       'expr MTIMES expr',  'expr MRDIVIDE expr',   'expr MLDIVIDE expr',   'expr TIMES expr',
       'expr RDIVIDE expr', 'expr LDIVIDE expr',    'expr POWER expr',  'expr MPOWER expr',) #list of binary ops copied from github
    def expr(self, p):
        return Expr_binop(p[0], p[1], p[2])
    
    @_('LPAREN expr RPAREN')
    def expr(self, p):
        return p[1]

    @_('expr DOT NAME')
    def expr(self, p):
        return ('member_access', (('obj', p[0]), ('mem_name', p[2])))

    @_('expr COMMA array_vals')
    def array_vals(self, p):
        return ArrayVals_expr_array_vals(p[0], p[2])
    
    @_('expr array_vals')
    def array_vals(self, p):
        return ArrayVals_expr_array_vals(p[0], p[1])
    
    @_('expr')
    def array_vals(self, p):
        return ArrayVals_expr(p[0])

    @_('LSQR array_vals RSQR')
    def array_literal(self, p):
        return ArrayLiteral(p[1])

    @_('array_vals SEMICOLON')
    def matrix_row_inner(self, p):
        return ('matrix_row_inner', p[0])
    
    @_('matrix_row_inner array_vals SEMICOLON')
    def matrix_row_inner(self, p):
        return ('matrix_row_inner', (('head', p[0]), ('tail', p[1])))
    
    @_('LSQR matrix_row_inner array_vals RSQR')
    def matrix_literal(self, p):
        return ('matrix_literal', (('head', p[1]), ('tail', p[2])))
    
    @_('matrix_literal')
    def expr(self, p):
        return p[0]
    
    @_('array_literal')
    def expr(self, p):
        return p[0]

    @_('command')
    def statement(self, p):
        return ('statement', p[0])

    @_('COMMAND')
    def command(self, p):
        return ('command', p[0]) #stolen directly from github parser as they use a special lexer construct to handle this

    @_('IF expr NEWLINE statements END')
    def if_block(self, p):
        return ('if', (('cond', p[1]), ('body', p[3])))
    
    @_('IF expr NEWLINE statements elseif_block')
    def if_block(self, p):
        return ('if', (('cond', p[1]), ('body', p[3]), ('elseif'), p[4]))
    
    @_('IF expr NEWLINE statements ELSE statements END')
    def if_block(self, p):
        return ('if', (('cond', p[1]), ('body', p[3]), ('else', p[5])))

    @_('ELSEIF expr NEWLINE statements elseif_block')
    def elseif_block(self, p):
        return ('elseif', (('cond', p[1]), ('body', p[3]), ('elseif', p[4])))
    
    @_('ELSEIF expr NEWLINE statements ELSE NEWLINE statements END')
    def elseif_block(self, p):
        return ('elseif', (('cond', p[1]), ('body', p[3]), ('else_body', p[6])))

    @_('if_block')
    def statement(self, p):
        return ('statement', p[0])

    @_('NAME COMMA return_vars')
    def return_vars(self, p):
        return ('return_vars', (('head', p[0]), ('tail', p[2])))

    @_('NAME')
    def return_vars(self, p):
    	return ('return_vars', p[0])


    @_('FUNCTION LSQR return_vars RSQR ASSIGN NAME LPAREN args RPAREN statements END NEWLINE')
    def statement(self, p):
    	return ('function_def', (('name', p[5]), ('return_vars', p[2]), ('args', p[7]), ('body', p[9])))
    
    #needed to parse provided test code
    @_('expr TRANSPOSE')
    def expr(self, p):
        return ('transpose', p[1])

    @_('expr CTRANSPOSE')
    def expr(self, p):
        return ('ctranspose', p[1])

#TODO:
#while
#switch
#try/catch
#anonymous functions
#unary postfix ops (transpose implemented)


if __name__ == '__main__':
    lexer = MatlabLexer()
    parser = Parser()

    text = ""
    for line in fileinput.input():
        text += line

    print("INPUT TEXT:")
    print(text)
    print("END")
    
    tokens = lexer.tokenize(text)

    
    result = parser.parse(tokens)
        

    result.print()

    ctx = Context()
    print("===== BEGIN PROGRAM =====")
    final_ctx = result.eval(ctx)
    print("====== END PROGRAM ======")
    print(final_ctx)
    final_ctx.print()
