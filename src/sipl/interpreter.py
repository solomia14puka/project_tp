import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from ast_nodes import *

class Interpreter:
    def __init__(self, trace=False):
        self.env = {}
        self.trace = trace

    def log_event(self, message: str):
        if self.trace:
            print(f"[TRACE] {message}")

    def evaluate(self, node):
        if hasattr(node, 'data') and node.data == 'start':
            return self.evaluate(node.children[0])
            
        if self.trace and hasattr(node, 'line') and getattr(node, 'line', 0) > 0:
            if isinstance(node, (Assign, While, If, Skip)):
                self.log_event(f"Перехід на рядок {node.line}: інструкція {node.__class__.__name__}")
                
        match node:
            case Program(statements=stmts):
                for stmt in stmts:
                    self.evaluate(stmt)
                return self.env
                
            case Assign(var_name=name, expr=expr):
                val = self.evaluate(expr)
                self.env[name] = val
                self.log_event(f"Подія: змінна '{name}' отримала нове значення {val}")
                
            case While(condition=cond, body=body):
                while self.evaluate(cond):
                    self.evaluate(body)
                    
            case If(condition=cond, true_body=tb, false_body=fb):
                if self.evaluate(cond):
                    self.evaluate(tb)
                else:
                    self.evaluate(fb)
                    
            case Skip():
                pass
                
            case Number(value=val):
                return val
                
            case Var(name=name):
                if name not in self.env:
                    raise ValueError(f"Помилка виконання: змінна '{name}' не ініціалізована")
                return self.env[name]
                
            case BinOp(left=l, op=op, right=r):
                left_val = self.evaluate(l)
                if op == 'not':
                    return not left_val
                    
                right_val = self.evaluate(r)
                if op == '+': return left_val + right_val
                elif op == '-': return left_val - right_val
                elif op == '*': return left_val * right_val
                elif op == 'div': return left_val // right_val
                elif op == '>': return left_val > right_val
                elif op == '=': return left_val == right_val
                else:
                    raise ValueError(f"Невідомий оператор: {op}")
                    
            case _:
                raise ValueError(f"Інтерпретатор не знає, як виконати вузол: {type(node)} -> {node}")
