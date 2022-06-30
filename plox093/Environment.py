import Expr
import Stmt
from Token import Token
from TokenType import TokenType
from LoxRuntimeError import LoxRuntimeError

class Environment:
    def __init__(self, enclosing=None):
        self.enclosing = enclosing
        self.values = {}

    def define(self, name: str, value: dict):
        self.values[name] = value

    def get(self, name: Token):
        if (name.lexeme in self.values.keys()):
            return self.values[name.lexeme]

        if (self.enclosing != None):
            return self.enclosing.get(name)

        LoxRuntimeError(name, "Undefined variable '" + name.lexeme + "'.")

    def assign(self, name: Token, value: dict):
        if (name.lexeme in self.values.keys()):
            self.values[name.lexeme] = value
            return

        if (self.enclosing != None):
            self.enclosing.assign(name, value)
            return

        LoxRuntimeError(name, "Undefined variable '" + name.lexeme + "'.")