import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from ast_nodes import *


class Interpreter:
    def __init__(self):
        # Словник
        self.env = {}

    def evaluate(self, node):
        """Рекурсивно обходить дерево і виконує операції."""
        
        if hasattr(node, 'data') and node.data == 'start':
            return self.evaluate(node.children[0])
            
        match node:
            case Program(statements=stmts):
                for stmt in stmts:
                    self.evaluate(stmt)
                return self.env
                
            case Assign(var_name=name, expr=expr):
                self.env[name] = self.evaluate(expr)
                
            case While(condition=cond, body=body):
                while self.evaluate(cond):
                    self.evaluate(body)
                    
            case If(condition=cond, true_body=tb, false_body=fb):
                if self.evaluate(cond):
                    self.evaluate(tb)
                else:
                    self.evaluate(fb)
                    
            case Skip():
                pass # Нічого не робимо
                
            case Number(value=val):
                return val
                
            case Var(name=name):
                if name not in self.env:
                    raise ValueError(f"Помилка виконання: змінна '{name}' не ініціалізована")
                return self.env[name]
                
            case BinOp(left=l, op=op, right=r):
                left_val = self.evaluate(l)
                
                # Обробка унарного оператора 'not'
                if op == 'not':
                    return not left_val
                    
                # Обчислюємо праву частину для бінарних операторів
                right_val = self.evaluate(r)
                
                # Математика та логіка
                if op == '+': return left_val + right_val
                elif op == '-': return left_val - right_val
                elif op == '*': return left_val * right_val
                elif op == 'div': return left_val // right_val
                elif op == '>': return left_val > right_val
                elif op == '=': return left_val == right_val
                else:
                    raise ValueError(f"Невідомий оператор: {op}")
                    
            case _:
                # Запобіжник: якщо потрапить невідомий вузол, програма видасть чітку помилку, а не впаде мовчки
                raise ValueError(f"Інтерпретатор не знає, як виконати вузол: {type(node)} -> {node}")