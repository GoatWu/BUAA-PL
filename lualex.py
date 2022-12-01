import ply.yacc as yacc
import ply.lex as lex

keywords = (
    'PRINT', 'FUNCTION', 'IF', 'ELSE', 'THEN', 'RETURN', 'END',
)

tokens = keywords + (
    'EQUAL', 'EQUALS', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'POWER',
    'LPAREN', 'RPAREN', 'LT', 'LE', 'GT', 'GE', 'NE',
    'COMMA', 'INTEGER', 'FLOAT', 'STRING', 'ID', 'NEWLINE'
)

t_ignore = ' \t'

keywords_map = {}
for r in keywords:
    keywords_map[r.lower()] = r


def t_ID(t):
    r'[A-Za-z_][\w_]*'
    t.type = keywords_map.get(t.value, "ID")
    return t


t_EQUAL = r'='
t_EQUALS = r'=='
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_POWER = r'\^'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LT = r'<'
t_LE = r'<='
t_GT = r'>'
t_GE = r'>='
t_NE = r'-='
t_COMMA = r'\,'
t_INTEGER = r'\d+'
t_FLOAT = r'((\d*\.\d+)(E[\+-]?\d+)?|([1-9]\d*E[\+-]?\d+))'
t_STRING = r'(\".*?\")|(\'.*?\')'


def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    return t


def t_preprocessor(t):
    r'--(.*)\n'
    t.lexer.lineno += 1


def t_error(t):
    print("Illegal character %s" % repr(t.value[0]))
    t.lexer.skip(1)


lexer = lex.lex(debug=0)

if __name__ == "__main__":
    lex.runmain(lexer)
