from dataclasses import dataclass
from typing import List, Optional

@dataclass
class ASTNode:
    line: int = 0
    column: int = 0

@dataclass(kw_only=True)
class Number(ASTNode):
    value: int

@dataclass(kw_only=True)
class Var(ASTNode):
    name: str

@dataclass(kw_only=True)
class BinOp(ASTNode):
    left: ASTNode
    op: str
    right: Optional[ASTNode]  # Optional для унарного "not"

@dataclass(kw_only=True)
class Assign(ASTNode):
    var_name: str
    expr: ASTNode

@dataclass(kw_only=True)
class While(ASTNode):
    condition: ASTNode
    body: ASTNode

@dataclass(kw_only=True)
class If(ASTNode):
    condition: ASTNode
    true_body: ASTNode
    false_body: ASTNode

@dataclass(kw_only=True)
class Skip(ASTNode):
    pass

@dataclass(kw_only=True)
class Program(ASTNode):
    statements: List[ASTNode]