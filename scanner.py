import ply.lex as lex

class Scanner(object):
    reserved = {
        'Program' : 'PROGRAM',
        'Var' : 'VAR',
        'Begin' : 'BEGIN',
        'End' : 'END',
        'Integer' : 'INTEGER'
    }

    tokens = [
        "BEGIN",
        "END",
        "IDENT",
        "STMT_END",
        "STRING",
        "L_PAREN",
        "R_PAREN",
        "OP_ASSIGN",
        "OP_ADD",
        "OP_SUBTR",
        "OP_MULT",
        "OP_DIV",
        "COMMENT",
        "COMMA",
        "COLON",
        "INT_TYPE",
        "PERIOD"
    ] + list(reserved)

    t_STMT_END = r';'
    t_STRING = r'\'(\\.|[^"\\])*\''
    t_L_PAREN = r'\('
    t_R_PAREN = r'\)'
    t_OP_ASSIGN = r':='
    t_OP_ADD = r'\+'
    t_OP_SUBTR = r'\-'
    t_OP_MULT = r'\*'
    t_OP_DIV = r'/'
    t_COMMENT = r'{.*}'
    t_COLON = r':'
    t_PERIOD = r'\.'
    t_COMMA = r','
    t_ignore = " \t"

    def t_IDENT(self, t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        t.type = self.reserved.get(t.value,'IDENT')    # Check for reserved words
        return t

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += t.value.count("\n")

    def t_error(self, t):
        print(f"Illegal character {t.value[0]!r}")
    
    def build(self,**kwargs):
        self.Lexer = lex.lex(module=self, **kwargs)