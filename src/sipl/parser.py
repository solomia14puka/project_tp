from lark import Lark

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