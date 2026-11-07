import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from lark import Lark, Transformer
from ast_nodes import *

# Формальна специфікація граматики SIPL (EBNF)
sipl_grammar = """
?start: program

program: "begin" statement_list "end"

statement_list: statement (";" statement)*

?statement: assign
          | loop
          | cond
          | program
          | skip

assign: CNAME ":=" aexpr
loop: "while" bexpr "do" statement
cond: "if" bexpr "then" statement "else" statement
skip: "skip"

// Логічні вирази (Boolean expressions)
?bexpr: aexpr ">" aexpr  -> gt
      | aexpr "=" aexpr  -> eq
      | "not" bexpr      -> not_op
      | "(" bexpr ")"

// Арифметичні вирази (Arithmetic expressions)
?aexpr: aexpr "+" term   -> add
      | aexpr "-" term   -> sub
      | term

?term: term "*" factor   -> mul
     | term "div" factor -> div
     | factor

?factor: NUMBER          -> number
       | CNAME           -> var
       | "(" aexpr ")"

// Імпорт стандартних правил для імен змінних, чисел та пробілів
%import common.CNAME
%import common.NUMBER
%import common.WS
%ignore WS
"""

# Ініціалізація парсера
sipl_parser = Lark(sipl_grammar, parser='lalr')

def parse_source(code: str):
    """Функція для розбору тексту програми на SIPL."""
    return sipl_parser.parse(code)

if __name__ == "__main__":
    # Тестовий запуск прямо у файлі
    test_code = """
    begin
        R := 1;
        while Y > 0 do
        begin
            R := R * X;
            Y := Y - 1
        end
    end
    """
    print(parse_source(test_code).pretty())

    sipl_parser = Lark(sipl_grammar, parser='lalr', propagate_positions=True)

class SIPLTransformer(Transformer):
    
    def number(self, args):
        tok = args[0]
        return Number(value=int(tok.value), line=tok.line, column=tok.column)

    def var(self, args):
        tok = args[0]
        return Var(name=str(tok.value), line=tok.line, column=tok.column)

    # Арифметичні та логічні операції
    def add(self, args): return BinOp(left=args[0], op='+', right=args[1], line=args[0].line)
    def sub(self, args): return BinOp(left=args[0], op='-', right=args[1], line=args[0].line)
    def mul(self, args): return BinOp(left=args[0], op='*', right=args[1], line=args[0].line)
    def div(self, args): return BinOp(left=args[0], op='div', right=args[1], line=args[0].line)
    def gt(self, args):  return BinOp(left=args[0], op='>', right=args[1], line=args[0].line)
    def eq(self, args):  return BinOp(left=args[0], op='=', right=args[1], line=args[0].line)
    
    def not_op(self, args): 
        return BinOp(left=args[0], op='not', right=None, line=args[0].line)
    
    # Оператори (Statements)
    def assign(self, args):
        tok = args[0] # CNAME
        return Assign(var_name=str(tok.value), expr=args[1], line=tok.line, column=tok.column)
        
    def loop(self, args):
        return While(condition=args[0], body=args[1], line=args[0].line)

    def cond(self, args):
        return If(condition=args[0], true_body=args[1], false_body=args[2], line=args[0].line)
        
    def skip(self, args):
        return Skip()
        
    def statement_list(self, args):
        return args

    def program(self, args):
        return Program(statements=args[0])

# Ініціалізуємо трансформер
transformer = SIPLTransformer()

def parse_source(code: str) -> Program:
    raw_tree = sipl_parser.parse(code)
    return transformer.transform(raw_tree)

if __name__ == "__main__":
    # Тестовий запуск
    test_code = """
    begin
        R := 1;
        while Y > 0 do
            R := R * X
    end
    """
    ast_tree = parse_source(test_code)
    
    import pprint
    pprint.pprint(ast_tree)