# /plox/Expr.py
# Isaac Braun
# CPTR-405

class Expr:
     pass

class Assign(Expr):
     def __init__(self, name, value):
          self.name = name
          self.value = value

     def accept(self, visitor):
          return visitor.visitAssign(self)

class Binary(Expr):
     def __init__(self, left, operator, right):
          self.left = left
          self.operator = operator
          self.right = right

     def accept(self, visitor):
          return visitor.visitBinary(self)

class Grouping(Expr):
     def __init__(self, expression):
          self.expression = expression

     def accept(self, visitor):
          return visitor.visitGrouping(self)

class Literal(Expr):
     def __init__(self, value):
          self.value = value

     def accept(self, visitor):
          return visitor.visitLiteral(self)

class Logical(Expr):
     def __init__(self, left, operator, right):
          self.left = left
          self.operator = operator
          self.right = right

     def accept(self, visitor):
          return visitor.visitLogical(self)

class Unary(Expr):
     def __init__(self, operator, right):
          self.operator = operator
          self.right = right

     def accept(self, visitor):
          return visitor.visitUnary(self)

class Variable(Expr):
     def __init__(self, name):
          self.name = name

     def accept(self, visitor):
          return visitor.visitVariable(self)

class Ternary(Expr):
     def __init__(self, condition, ifTrue, ifFalse):
          self.condition = condition
          self.ifTrue = ifTrue
          self.ifFalse = ifFalse

     def accept(self, visitor):
          return visitor.visitTernary(self)

