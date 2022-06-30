# /plox/AstPrinter.py
# Isaac Braun
# CPTR-405

import Expr
from Token import Token

class AstPrinter:
    def print(self, expr):
        return expr.accept(self)

    def visitBinary(self, expr):
        return self.parenthesize(expr.operator.lexeme, expr.left, expr.right)

    def  visitGrouping(self, expr):
        return self.parenthesize("group", expr.expression)

    def visitLiteral(self, expr):
        if (expr.value == None): return "nil"
        return str(expr.value)

    def visitUnary(self, expr):
        return self.parenthesize(expr.operator.lexeme, expr.right)

    def parenthesize(self, name, *exprs):
        builder = "(" + name
        for expr in exprs:
            builder += " "
            builder += expr.accept(self)
        builder += ")"
        return builder