# /plox/RpnPrinter.py
# Isaac Braun
# CPTR-405

class RpnPrinter:
    def print(self, expr):
        return expr.accept(self)

    def visitBinary(self, expr):
        return self.push(expr.operator.lexeme, expr.left, expr.right)

    def visitGrouping(self, expr):
        return self.push("group", expr.expression)

    def visitLiteral(self, expr):
        if (expr.value == None): return "nil"
        return str(expr.value)

    def visitUnary(self, expr):
        return self.push(expr.operator.lexeme, expr.right)

    def push(self, name, *exprs):
        builder = ""
        for expr in exprs:
            builder += expr.accept(self)
            builder += " "
        builder += name
        return builder