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

class Break(Stmt):
     def accept(self, visitor):
          return visitor.visitBreak(self)

class Continue(Stmt):
     def accept(self, visitor):
          return visitor.visitContinue(self)

class Exit(Stmt):
     def accept(self, visitor):
          return visitor.visitExit(self)

class Expression(Stmt):
     def __init__(self, expression):
          self.expression = expression

     def accept(self, visitor):
          return visitor.visitExpression(self)

class For(Stmt):
     def __init__(self, initializer, condition, increment, body):
          self.initializer = initializer
          self.condition = condition
          self.increment = increment
          self.body = body

     def accept(self, visitor):
          return visitor.visitFor(self)

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

