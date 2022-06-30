# /plox/Expr.py
# Isaac Braun
# CPTR-405

class Stmt:
     pass

class Block(Stmt):
     def __init__(self, statements):
          self.statements = statements

     def accept(self, visitor):
          return visitor.visitBlock(self)

class Expression(Stmt):
     def __init__(self, expression):
          self.expression = expression

     def accept(self, visitor):
          return visitor.visitExpression(self)

class Print(Stmt):
     def __init__(self, expression):
          self.expression = expression

     def accept(self, visitor):
          return visitor.visitPrint(self)

class Var(Stmt):
     def __init__(self, name, initializer):
          self.name = name
          self.initializer = initializer

     def accept(self, visitor):
          return visitor.visitVar(self)

