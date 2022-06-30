# /plox/Interpreter.py
# Isaac Braun
# CPTR-405

import Expr
import Stmt
from Environment import Environment
from LoxRuntimeError import LoxRuntimeError

class Interpreter:
    def __init__(self, lox) -> None:
        super().__init__()
        self.lox = lox
        self.environment = Environment()

    def interpret(self, statements):
        try:
            for statement in statements:
                self.execute(statement)
        except LoxRuntimeError():
            self.lox.RuntimeError()

    def visitTernary(self, expr):
        condition = self.evaluate(expr.condition)
        
        if (str(condition) == '0.0'):
            condition = True
        
        if (self.isTruthy(condition)):
            return self.evaluate(expr.ifTrue)
        else:
            return self.evaluate(expr.ifFalse)

    def visitLiteral(self, expr):
        return expr.value

    def visitLogical(self, expr):
        left = self.evaluate(expr.left)

        if (expr.operator.token_type == "OR"):
            if (self.isTruthy(left)):
                return left
        else:
            if (not self.isTruthy(left)):
                return left

        return self.evaluate(expr.right)

    def visitUnary(self, expr):
        right = self.evaluate(expr.right)

        if (expr.operator.token_type == "BANG"):
            return not self.isTruthy(right)
        elif (expr.operator.token_type == "MINUS"):
            self.checkNumberOperand(expr.operator, right)
            return -right

        return None

    def visitVariable(self, expr):
        return self.environment.get(expr.name)
    
    def checkNumberOperand(self, operator, operand):
        if (isinstance(operand, (int, float))): return
        LoxRuntimeError(operator, "Operand must be a number.")

    def checkNumberOperands(self, operator, left, right):
        if (isinstance(left, (int, float)) and isinstance(right, (int, float))): return
        LoxRuntimeError(operator, "Operands must be numbers.")

    def isTruthy(self, object):
        if (object == None or object == "nil" or object == "false"): return False
        if (isinstance(object, bool)): return bool(object)
        return True

    def isEqual(self, a, b):
        if (a == None and b == None): return True
        if (a == None):
            return False
        
        return a == b

    def stringify(self, object):
        if (object == None): return "nil"

        if (isinstance(object, float)):
            text = str(object)
            if (text.endswith(".0")):
                text = text[0 : (len(text) - 2)]
            
            return text

        output = str(object)

        if (output == 'True'):
            output = 'true'
        elif (output == 'False'):
            output = 'false'

        return output

    def visitGrouping(self, expr):
        return self.evaluate(expr.expression)

    def evaluate(self, expr):
        return expr.accept(self)

    def execute(self, stmt):
        stmt.accept(self)

    def executeBlock(self, statements, environment):
        previous = self.environment;
        try:
            self.environment = environment;

            for statement in statements:
                self.execute(statement)

        finally:
            self.environment = previous

    def visitBlock(self, stmt):
        self.executeBlock(stmt.statements, Environment(self.environment))
        return None

    def visitExpression(self, stmt):
        self.evaluate(stmt.expression)

    def visitIf(self, stmt):
        if (self.isTruthy(self.evaluate(stmt.condition))):
            self.execute(stmt.thenBranch)
        elif (stmt.elseBranch != None):
            self.execute(stmt.elseBranch)

        return None

    def visitPrint(self, stmt):
        value = self.evaluate(stmt.expression)
        print(self.stringify(value))

    def visitVar(self, stmt):
        value = None
        if (stmt.initializer != None):
            value = self.evaluate(stmt.initializer)

        self.environment.define(stmt.name.lexeme, value)
        return None

    def visitWhile(self, stmt):
        while (self.isTruthy(self.evaluate(stmt.condition))):
            self.execute(stmt.body)

        return None

    def visitAssign(self, expr):
        value = self.evaluate(expr.value)
        self.environment.assign(expr.name, value)
        return value

    def visitBinary(self, expr):
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)

        if (expr.operator.token_type == "GR"):
            if (isinstance(left, (int, float)) and isinstance(right, (int, float))):
                return left > right
            elif (isinstance(left, str) and isinstance(right, str)):
                return str(left) > str(right)
        elif (expr.operator.token_type == "GR_EQ"):
            if (isinstance(left, (int, float)) and isinstance(right, (int, float))):
                return left >= right
            elif (isinstance(left, str) and isinstance(right, str)):
                return str(left) >= str(right)
        elif (expr.operator.token_type == "LT"):
            if (isinstance(left, (int, float)) and isinstance(right, (int, float))):
                return left < right
            elif (isinstance(left, str) and isinstance(right, str)):
                return str(left) < str(right)
        elif (expr.operator.token_type == "LT_EQ"):
            if (isinstance(left, (int, float)) and isinstance(right, (int, float))):
                return left <= right
            elif (isinstance(left, str) and isinstance(right, str)):
                return str(left) <= str(right)
        elif (expr.operator.token_type == "BANG_EQ"):
            return not self.isEqual(left, right)
        elif (expr.operator.token_type == "IS_EQ"):
            return self.isEqual(left, right)
        elif (expr.operator.token_type == "MINUS"):
            self.checkNumberOperands(expr.operator, left, right)
            return float(left) - float(right)
        elif (expr.operator.token_type == "PLUS"):
            if (isinstance(left, (int, float)) and isinstance(right, (int, float))):
                return left + right
            elif (isinstance(left, str) and isinstance(right, str)):
                return str(left) + str(right)
            LoxRuntimeError(expr.operator, "Operands must be two numbers or two strings.")
        elif (expr.operator.token_type == "SLASH"):
            self.checkNumberOperands(expr.operator, left, right)
            return float(left) / float(right)
        elif (expr.operator.token_type == "STAR"):
            self.checkNumberOperands(expr.operator, left, right)
            return float(left) * float(right)

        return None