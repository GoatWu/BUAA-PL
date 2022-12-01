import ply.yacc as yacc
import ply.lex as lex
import lualex

tokens = lualex.tokens

precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('left', 'POWER'),
    ('right', 'UMINUS')
)


def p_program(p):
    '''program : program statement
               | statement'''

    if len(p) == 2 and p[1]:
        p[0] = []
        p[0].append(p[1])
    elif len(p) == 3:
        p[0] = p[1]
        if not p[0]:
            p[0] = []
        if p[2]:
            p[0].append(p[2])


def p_program_error(p):
    '''program : error'''
    p[0] = None
    p.parser.error = 1


def p_statement(p):
    '''statement : command NEWLINE'''
    if isinstance(p[1], str):
        print("%s %s %s" % (p[1], "AT LINE", p.lineno(1)))
        p[0] = None
        p.parser.error = 1
    else:
        p[0] = p[1]


def p_statement_bad(p):
    '''statement : error NEWLINE'''
    print("MALFORMED STATEMENT AT LINE %s" % p.lineno(1))
    p[0] = None
    p.parser.error = 1


def p_statement_newline(p):
    '''statement : NEWLINE'''
    p[0] = None


def p_command_print(p):
    '''command : PRINT LPAREN plist RPAREN'''
    p[0] = ('PRINT', p[3])


def p_command_print_bad(p):
    '''command : PRINT error'''
    p[0] = "MALFORMED PRINT STATEMENT"
    p.parser.error = 1


def p_command_if(p):
    '''command : IF relexpr THEN expr'''
    p[0] = ('IF', p[2], int(p[4]))


def p_command_if_bad(p):
    '''command : IF error THEN expr'''
    p[0] = "BAD RELATIONAL EXPRESSION"
    p.parser.error = 1


def p_command_if_bad2(p):
    '''command : IF relexpr THEN error'''
    p[0] = "INVALID LINE NUMBER IN THEN"
    p.parser.error = 1


def p_command_end(p):
    '''command : END'''
    p[0] = ('END',)


def p_command_else(p):
    '''command : ELSE'''
    p[0] = ('ELSE',)


def p_command_def(p):
    '''command : FUNCTION ID LPAREN idlist RPAREN'''
    p[0] = ('FUNC', p[2], p[4])


def p_commend_return(p):
    '''command : RETURN
               | RETURN pitem'''
    if len(p) == 2:
        p[0] = ('RETURN',)
    else:
        p[0] = ('RETURN', p[2])


def p_id_list(p):
    '''idlist : idlist COMMA ID
              | ID'''
    if len(p) > 3:
        p[0] = p[1]
        p[0].append(p[3])
    else:
        p[0] = [p[1]]


def p_plist(p):
    '''plist   : plist COMMA pitem
               | pitem'''
    if len(p) > 3:
        p[0] = p[1]
        p[0].append(p[3])
    else:
        p[0] = [p[1]]


def p_item_string(p):
    '''pitem : STRING'''
    p[0] = (p[1][1:-1], None)


def p_item_expr(p):
    '''pitem : expr'''
    p[0] = ("", p[1])


def p_expr_binary(p):
    '''expr : expr PLUS expr
            | expr MINUS expr
            | expr TIMES expr
            | expr DIVIDE expr
            | expr POWER expr'''

    p[0] = ('BINOP', p[2], p[1], p[3])


def p_expr_number(p):
    '''expr : INTEGER
            | FLOAT'''
    p[0] = ('NUM', eval(p[1]))


def p_expr_variable(p):
    '''expr : variable'''
    p[0] = ('VAR', p[1])


def p_expr_group(p):
    '''expr : LPAREN expr RPAREN'''
    p[0] = ('GROUP', p[2])


def p_expr_unary(p):
    '''expr : MINUS expr %prec UMINUS'''
    p[0] = ('UNARY', '-', p[2])


# Relational expressions


def p_relexpr(p):
    '''relexpr : expr LT expr
               | expr LE expr
               | expr GT expr
               | expr GE expr
               | expr EQUALS expr
               | expr NE expr'''
    p[0] = ('RELOP', p[2], p[1], p[3])


# Variables


def p_variable(p):
    '''variable : ID
              | ID EQUAL expr'''
    if len(p) == 2:
        p[0] = ('LET', p[1], None)
    else:
        p[0] = ('LET', p[1], p[3])


def p_error(p):
    if not p:
        print("SYNTAX ERROR AT EOF")


bparser = yacc.yacc()


def parse(data, debug=0):
    bparser.error = 0
    p = bparser.parse(data, debug=debug)
    # print(p)
    if bparser.error:
        return None
    return p


if __name__ == "__main__":
    parse('print("hello lua")\n')
