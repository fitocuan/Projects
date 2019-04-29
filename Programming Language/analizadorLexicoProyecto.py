import ply.lex as lex



tokens = [ 'COMMENT','ID', 'ASSIGN', 'LPARENT', 'RPARENT', 'NUMBER', 'COMMA',  'ASTERISCO', 'STRING', 'SUMA', 'RESTA', 'DIV', 'OR', 'AND', 'NOT', 'LESS', 'MORE', 'LESSEQUAL', 'MOREEQUAL', 'NOTEQUAL', 'EQUAL','FLOAT']

reserved = {
	'integer' : 'INTEGER',
	'real' : 'REAL',
	'program' : 'PROGRAM',
	'end' : 'END',
	'read' : 'READ',
	'print': 'PRINT',
	'call': 'CALL',
	'if': 'IF',
	'then': 'THEN',
	'else': 'ELSE',
	'do': 'DO',
	'exit': 'EXIT',
	'subroutine': 'SUBROUTINE',
	'elsif': 'ELSIF'

}

tokens += reserved.values()


t_ASSIGN 	= r'='
t_LPARENT 	= r'\('
t_RPARENT 	= r'\)'
t_COMMA 	= r','
t_ASTERISCO = r'\*'
#t_COMILLAS 	= r'"'


t_SUMA 		= r'\+'
t_RESTA	 	= r'\-'
t_DIV 		= r'/'

t_OR 		= r'\.or\.'
t_AND 		= r'\.and\.'
t_NOT 		= r'\.not\.'

t_LESS 		= r'<'
t_MORE 		= r'>'
t_LESSEQUAL = r'<='
t_MOREEQUAL = r'>='
t_NOTEQUAL 	= r'<>'
t_EQUAL 	= r'=='


def t_STRING(t):
     r'("[^"]*")|(\'[^\']*\')'
     return t

def t_ID(t):
	r'[a-zA-Z_][a-zA-Z0-9_]*'
	if t.value in reserved:
		t.type = reserved[ t.value ]
	return t


def t_FLOAT(t):
	r'\d+(\.\d+)'
	t.value = float(t.value)
	return t

def t_NUMBER(t):
	r'\d+'
	t.value = int(t.value)
	return t



def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore_COMMENT = r'(\!(.|\n)*?\!)'


t_ignore = ' \t'



def t_error(t):
     print("Illegal character '%s'" % t.value[0])
     t.lexer.skip(1)

lexer = lex.lex()


data = ''' 2 2.0 '''

# Give the lexer some input
lexer.input(data)

# Tokenize
while True:
 	tok = lexer.token()
 	if not tok:
 		break      # No more input
 	print(tok)
