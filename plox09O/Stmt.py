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

class If(Stmt):
     def __init__(self, condition, thenBranch, elseBranch):
          self.condition = condition
          self.thenBranch = thenBranch
          self.elseBranch = elseBranch

     def accept(self, visitor):
          return visitor.visitIf(self)

class Print(Stmt):
     def __init__(self, expression):
          self.expression = expression

     def accept(self, visitor):
          return visitor.visitPrint(self)

class Switch(Stmt):
     def __init__(self, value, cases, default):
          self.value = value
          self.cases = cases
          self.default = default

     def accept(self, visitor):
          return visitor.visitSwitch(self)

class Var(Stmt):
     def __init__(self, name, initializer):
          self.name = name
          self.initializer = initializer

     def accept(self, visitor):
          return visitor.visitVar(self)

class While(Stmt):
     def __init__(self, condition, body):
          self.condition = condition
          self.body = body

     def accept(self, visitor):
          return visitor.visitWhile(self)

