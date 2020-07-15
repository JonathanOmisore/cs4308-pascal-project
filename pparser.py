# Kennesaw State University
# College of Computing and Software Engineering
# Department of Computer Science
# CS 4308/W01 Concepts of Programming Languages
# 2nd Project Deliverable: pparser.py
# Jackson Randolph: jrando13@students.kennesaw.edu
# July 2nd, 2020

import ply.yacc as yacc
from scanner import Scanner
from interp import Interpreter

class PascalParser(object):
    #precedence rules for operators
    precedence = (
        ('left', '+', '-'),
        ('left', '*', '/')
    )

    #Each parser action is defined as the following:
    #def p_<name>(self, p):
    #    """Grammar rule"""
    #    <action code>

    #p is a list object that contains objects that represent the symbols in the grammar rule
    #For example:
    #""" assign : ident ASSIGN_OP expression"""
    #     p[0]    p[1]    p[2]      p[3] 

    #data can be bubbled up to parent rules by assignment to p[0]

    #region Actions
    def p_program(self, p):
        """program : program_decl"""
        p[0] = p[1]
        print(p[1])

    def p_program_decl(self, p):
        """program_decl : program_ident compound_statement '.' """
        p[0] = p[1]
    
    def p_program_decl_err(self, p):
        """program_decl : program_ident error '.' """
        p[0] = p[1]
    
    def p_program_decl_wvar(self, p):
        """program_decl : program_ident variable_decl_sec compound_statement '.'"""
        p[0] = p[1]
    
    def p_program_decl_wvar_err_a(self, p):
        """program_decl : program_ident error compound_statement '.'"""
        print(f"Err line {p.lineno(2)}")
        for s in p[3]:
            print('\t' + s + ';')
        p[0] = p[1]
    
    def p_program_decl_wvar_err_b(self, p):
        """program_decl : program_ident variable_decl_sec error '.'"""
        print("Compund statement error")
        p[0] = p[1]
    
    def p_program_ident(self, p):
        """program_ident : PROGRAM identifier ';'"""
        p[0] = str(p[1]) + " " + p[2]

    def p_program_ident_error(self, p):
        """program_ident : PROGRAM error ';'"""
        print("Program Identifier Error")

    def p_variable_decl_sec(self, p):
        """variable_decl_sec : VAR variable_decl_sec_inner"""
    
    def p_variable_decl_sec_err(self, p):
        """variable_decl_sec : VAR error"""
        print("Variable inner error")
    
    def p_variable_decl_sec_inner(self, p):
        """variable_decl_sec_inner : variable_declaration ';'
            | variable_decl_sec_inner variable_declaration ';'"""
    
    def p_variable_declaration(self, p):
        """variable_declaration : identifier_list ':' type"""
        s_type = "none"
        s_data = None

        if p[3] == "Integer":
            s_type = "int"
            s_data = 1

        for s in p[1]:
            self.interpreter.newsym(s, s_type, s_data)
    
    def p_identifier(self, p):
        """identifier : NAME"""
        p[0] = p[1]
    
    def p_identifier_list(self, p):
        """identifier_list : identifier
            | identifier_list ',' identifier"""
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            if p[1] is None:
                p[0] = [p[3]]
            else:
                p[0] = p[1]
                p[0].append(p[3])
    
    def p_type(self, p):
        """type : INTEGER"""
        p[0] = p[1]
    
    def p_compound_statement(self, p):
        """compound_statement : BEGIN statement_list END"""
        p[0] = p[2]
    
    def p_compound_statement_err(self, p):
        """compound_statement : BEGIN error END"""
        print("Compund Statement Error")
    
    def p_statement_list(self, p):
        """statement_list : statement
            | statement_list statement"""
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            if p[1] is None:
                p[0] = [p[2]]
            else:
                p[0] = p[1]
                p[0].append(p[2])
    
    def p_statement(self, p):
        """statement : assignment_statement
            | function_statement
            | compound_statement"""
        p[0] = p[1]
    
    def p_assignment_statement(self, p):
        """assignment_statement : identifier OP_ASSIGN actual_value ';'"""
        up = f"{p[1]} := {p[3]}"
        p[0] = up

    def p_assignment_err(self, p):
        """assignment_statement : identifier OP_ASSIGN error ';'"""
        print(f"Syntax error line {p.lineno(3)}: Malformed expression")
    
    def p_function_statement(self, p):
        """function_statement : function_designator ';'"""
        param = []
        name = ''
        desig = p[1]
        if(len(desig) == 2):
            name, param = desig
        else:
            name = desig
        sym = self.interpreter.getsym(name)
        sym.data(*param)
    
    def p_function_designator(self, p):
        """function_designator : identifier
            | identifier actual_parameter_list"""
        if len(p) == 2:
            p[0] = (p[1])
        else:
            p[0] = (p[1], p[2])

    def p_actual_parameter_list(self, p):
        """actual_parameter_list : '(' actual_parameter_list_inner ')'"""
        up = p[2]
        p[0] = up
    
    def p_actual_parameter_list_inner(self, p):
        """actual_parameter_list_inner : actual_parameter
            | actual_parameter_list_inner ',' actual_parameter"""
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            if p[1] is None:
                p[0] = [p[3]]
            else:
                p[0] = p[1]
                p[0].append(p[3])
    
    def p_actual_parameter(self, p):
        """actual_parameter : actual_value"""
        p[0] = p[1]
    
    def p_actual_value(self, p):
        """actual_value : expression"""
        up = p[1]
        exp = ''.join(p[1])
        p[0] = eval(exp)
    
    def p_expression(self, p):
        """expression : term
            | '-' term
            | '+' term
            | expression addition_operator term"""
        up = None

        if len(p) == 2:
            up = p[1]
        elif len(p) == 3:
            up = [p[1], *p[2]]
        else:
            up = p[1] + [p[2], *p[3]]
        
        p[0] = up

    
    def p_expression_err_a(self, p):
        """expression : error addition_operator term"""
        print("Expression error type A")
    
    def p_expression_err_b(self, p):
        """expression : expression error term"""
        print("Expression error type B")
    
    def p_expression_err_c(self, p):
        """expression : expression addition_operator error"""
        print("Expression error type C")
    
    def p_addition_operator(self, p):
        """addition_operator : '+'
            | '-'"""
        p[0] = p[1]
    
    def p_term(self, p):
        """term : factor
            | term multiplication_operator factor"""
        up = None
        if len(p) == 2:
            up = [p[1]]
        else:
            up = p[1] + [p[2], p[3]]
        p[0] = up
    
    def p_multiplication_operator_m(self, p):
        """multiplication_operator : '*'
            | '/'"""
        up = p[1]
        if up == '/':
            up = '//'
        p[0] = up
    
    def p_factor_str(self, p):
        """factor : STRING"""
        p[0] = p[1]

    def p_factor_exp(self, p):
        """factor : '(' expression ')'"""
        p[0] = p[1]
    
    def p_factor_ident(self, p):
        """factor : identifier"""
        p[0] = str(self.interpreter.getsym(p[1]).data)
    
    def p_error(self, p):
        print("Syntax error in input!")
        print(p)
    #endregion

    #Helper methods
    def Parse(self, text):
        self.interpreter = Interpreter()
        self.Yacc.parse(text, lexer=self.Lexer.Lexer, tracking=True)

    def build(self,**kwargs):
        self.Lexer = Scanner()
        self.Lexer.build()
        self.tokens = self.Lexer.tokens
        self.Yacc = yacc.yacc(module=self, **kwargs)

if __name__ == "__main__":
    p = PascalParser()
    p.build()
    print("Parser built")