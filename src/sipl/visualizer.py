import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from ast_nodes import *

class ASTVisualizer:
    def __init__(self):
        self.node_counter = 0
        self.dot_lines = []

    def get_new_id(self):
        self.node_counter += 1
        return f"node{self.node_counter}"

    def add_node(self, node_id, label):
        # Екрануємо лапки, щоб не зламати синтаксис DOT
        safe_label = str(label).replace('"', '\\"')
        self.dot_lines.append(f'    {node_id} [label="{safe_label}"];')

    def add_edge(self, from_id, to_id, label=""):
        if label:
            self.dot_lines.append(f'    {from_id} -> {to_id} [label="{label}"];')
        else:
            self.dot_lines.append(f'    {from_id} -> {to_id};')

    def generate_dot(self, node) -> str:
        """Головний метод генерації тексту DOT."""
        self.dot_lines = [
            "digraph AST {", 
            '    node [shape=box, style=rounded, fontname="Arial"];'
        ]
        self._traverse(node)
        self.dot_lines.append("}")
        return "\n".join(self.dot_lines)

    def _traverse(self, node) -> str:
        """Рекурсивно обходить дерево і повертає ID створеного вузла."""
        if hasattr(node, 'data') and node.data == 'start':
            return self._traverse(node.children[0])

        current_id = self.get_new_id()

        match node:
            case Program(statements=stmts):
                self.add_node(current_id, "Program")
                for stmt in stmts:
                    child_id = self._traverse(stmt)
                    self.add_edge(current_id, child_id)
            case Assign(var_name=name, expr=expr):
                self.add_node(current_id, f"Assign: {name}")
                child_id = self._traverse(expr)
                self.add_edge(current_id, child_id, "expr")
            case While(condition=cond, body=body):
                self.add_node(current_id, "While")
                cond_id = self._traverse(cond)
                self.add_edge(current_id, cond_id, "condition")
                body_id = self._traverse(body)
                self.add_edge(current_id, body_id, "body")
            case If(condition=cond, true_body=tb, false_body=fb):
                self.add_node(current_id, "If")
                cond_id = self._traverse(cond)
                self.add_edge(current_id, cond_id, "condition")
                tb_id = self._traverse(tb)
                self.add_edge(current_id, tb_id, "true")
                fb_id = self._traverse(fb)
                self.add_edge(current_id, fb_id, "false")
            case Skip():
                self.add_node(current_id, "Skip")
            case Number(value=val):
                self.add_node(current_id, f"Number: {val}")
            case Var(name=name):
                self.add_node(current_id, f"Var: {name}")
            case BinOp(left=l, op=op, right=r):
                self.add_node(current_id, f"BinOp: {op}")
                left_id = self._traverse(l)
                self.add_edge(current_id, left_id, "left")
                if r is not None: # Для унарних операторів right відсутній
                    right_id = self._traverse(r)
                    self.add_edge(current_id, right_id, "right")
            case _:
                self.add_node(current_id, f"Unknown: {type(node)}")

        return current_id