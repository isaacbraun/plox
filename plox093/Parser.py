# /plox/Parser.py
# Isaac Braun
# CPTR-405

import Expr
import Stmt
from Token import Token
from TokenType import TokenType

class ParserError(BaseException):
    def __init__(self, token, message):
        self.token = token
        self.message = message

class Parser:
    def __init__(self, tokens, lox):
        self.tokens = tokens
        self.current = 0
        self.loopDepth = 0
        self.lox = lox

    def parse(self):
        try:
            statements = []
            
            while (not self.isAtEnd()):
                statements.append(self.declaration())

            return statements
        except ParserError:
            return None

    def error(self, token: Token, message: str):
        self.lox.parserError(token, message)
        raise ParserError(token, message)

    def declaration(self):
        try:
            if (self.match("VAR")):
                return self.varDeclaration()
            else:
                return self.statement()
            
        except ParserError:
            self.synchronize()
            return None

    def statement(self):
        if (self.match("FOR")):
            return self.forStatement()
        elif (self.match("IF")):
            return self.ifStatement()
        elif (self.match("PRINT")):
            return self.printStatement()
        elif (self.match("WHILE")):
            return self.whileStatement()
        elif (self.match("L_BRACE")):
            return Stmt.Block(self.block())
        elif (self.match("EXIT")):
            return self.exitStatement()
        elif (self.match("BREAK")):
            return self.breakStatement()
        elif (self.match("CONTINUE")):
            return self.continueStatement()
        else:
            return self.expressionStatement()

    def forStatement(self):
        try:
            self.loopDepth += 1
            self.consume("L_PAREN", "Expect '(' after 'for'.")

            if (self.match("SEMICOLON")):
                initializer = None
            elif (self.match("VAR")):
                initializer = self.varDeclaration()
            else:
                initializer = self.expressionStatement()

            condition = None
            if (not self.check("SEMICOLON")):
                condition = self.expression()

            self.consume("SEMICOLON", "Expect ';' after loop condition.")

            increment = None
            if (not self.check("R_PAREN")):
                increment = self.expression()
            
            self.consume("R_PAREN", "Expect ')' after for clauses.")

            body = self.statement()

            if (condition == None):
                condition = Expr.Literal(True)

            return Stmt.For(initializer, condition, increment, body)
        finally:
            self.loopDepth -= 1

    def ifStatement(self):
        self.consume("L_PAREN", "Expect '(' after 'if'.")
        condition = self.expression()
        self.consume("R_PAREN", "Expect ')' after if condition.")

        thenBranch = self.statement()
        elseBranch = None

        if (self.match("ELSE")):
            elseBranch = self.statement()

        return Stmt.If(condition, thenBranch, elseBranch)


    def varDeclaration(self):
        name = self.consume("IDENTIFIER", "Expect variable name.")

        initializer = None
        if (self.match("EQ")):
            initializer = self.expression()

        self.consume("SEMICOLON", "Expect ';' after variable declaration.")
        return Stmt.Var(name, initializer)

    def whileStatement(self):
        try:
            self.loopDepth += 1
            self.consume("L_PAREN", "Expect '(' after 'while'.")
            condition = self.expression()
            self.consume("R_PAREN", "Expect ')' after condition.")
            body = self.statement()

            return Stmt.While(condition, body)
        finally:
            self.loopDepth -= 1

    def printStatement(self):
        value = self.expression()
        self.consume("SEMICOLON", "Expect ';' after value.")
        return Stmt.Print(value)

    def expressionStatement(self):
        expr = self.expression()
        self.consume("SEMICOLON", "Expect ';' after expression.")
        return Stmt.Expression(expr)

    def block(self):
        statements = []

        while (not self.check("R_BRACE") and not self.isAtEnd()):
            statements.append(self.declaration())

        self.consume("R_BRACE", "Expect '}' after block.")
        return statements

    def exitStatement(self):
        self.consume("SEMICOLON", "Expect ';' after 'exit'.")
        return Stmt.Exit()

    def breakStatement(self):
        if (self.loopDepth == 0):
            self.error(self.previous(), "'break' is only allowed in a loop.")
            if (self.check("SEMICOLON")): self.advance()
        else:
            self.consume("SEMICOLON", "Expect ';' after 'break'.")
            return Stmt.Break()

    def continueStatement(self):
        if (self.loopDepth == 0):
            self.error(self.previous(), "'continue' is only allowed in a loop.")
            if (self.check("SEMICOLON")): self.advance()
        else:
            self.consume("SEMICOLON", "Expect ';' after 'continue'.")
            return Stmt.Continue()

    def expression(self):
        return self.assignment()

    def assignment(self):
        expr = self.ternary()

        if (self.match("EQ")):
            equals = self.previous()
            value = self.assignment()

            if (isinstance(expr, (Expr.Variable))):
                name = expr.name
                return Expr.Assign(name, value)

            self.error(equals, "Invalid assignment target.")

        return expr

    def ternary(self):
        expr = self.OR()
        
        while (self.match("QUESTION")):
            ifTrue = self.expression()
            self.consume("COLON", "Expect '?' to have matching ':'.")
            ifFalse = self.expression()
            expr = Expr.Ternary(expr, ifTrue, ifFalse)

        return expr

    def OR(self):
        expr = self.AND()

        while (self.match("OR")):
            operator =self. previous()
            right = self.AND()
            expr = Expr.Logical(expr, operator, right)

        return expr

    def AND(self):
        expr = self.equality()

        while (self.match("AND")):
            operator = self.previous()
            right = self.equality()
            expr = Expr.Logical(expr, operator, right)

        return expr

    def equality(self):
        expr = self.comparison()

        while (self.match("BANG_EQ", "IS_EQ")):
            operator = self.previous()
            right = self.comparison()
            expr = Expr.Binary(expr, operator, right)

        return expr

    def comparison(self):
        expr = self.term()

        while (self.match("GR", "GR_EQ", "LT", "LT_EQ")):
            operator = self.previous()
            right = self.term()
            expr = Expr.Binary(expr, operator, right)

        return expr

    def term(self):
        expr = self.factor()

        while (self.match("MINUS", "PLUS")):
            
            operator = self.previous()
            right = self.factor()
            expr = Expr.Binary(expr, operator, right)

        return expr

    def factor(self):
        expr = self.unary()

        while (self.match("SLASH", "STAR")):
            operator = self.previous()
            right = self.unary()
            expr = Expr.Binary(expr, operator, right)

        return expr

    def unary(self):
        if (self.match("BANG", "MINUS")):
            operator = self.previous()
            right = self.unary()
            return Expr.Unary(operator, right)
        
        return self.primary()
    
    def primary(self):
        if (self.match("FALSE")): return Expr.Literal('false')
        elif (self.match("TRUE")): return Expr.Literal('true')
        elif (self.match("NIL")): return Expr.Literal('nil')

        elif (self.match("NUMBER", "STRING")):
            return Expr.Literal(self.previous().literal)

        elif (self.match("IDENTIFIER")):
            return Expr.Variable(self.previous())

        elif (self.match("L_PAREN")):
            expr = self.expression()
            self.consume("R_PAREN", "Expect ')' after expression.")
            return Expr.Grouping(expr)

        else:
            self.error(self.peek(), "Expect expression.")

    def match(self, *tokenTypes):
        for tkType in tokenTypes:
            if (self.check(tkType)):
                self.advance()
                return True

        return False

    def consume(self, tkType: str, message: str):
        if (self.check(tkType)): return self.advance()

        self.error(self.peek(), message)
    
    def check(self, tkType: str):
        if (self.isAtEnd()): return False
        return self.peek().token_type == tkType

    def advance(self) -> Token:
        if (not self.isAtEnd()):
            self.current += 1
        return self.previous()

    def isAtEnd(self):
        return self.peek().token_type == "EOF"

    def peek(self) -> Token:
        return self.tokens[self.current]

    def previous(self) -> Token:
        return self.tokens[self.current - 1]

    def synchronize(self):
        self.advance()

        while (not self.isAtEnd()):
            if (self.previous().token_type == "SEMICOLON"): return

            tk_type = self.peek().token_type
            if (tk_type == "CLASS"): pass
            elif (tk_type == "CLASS"): pass
            elif (tk_type == "FUN"): pass
            elif (tk_type == "VAR"): pass
            elif (tk_type == "FOR"): pass
            elif (tk_type == "IF"): pass
            elif (tk_type == "WHILE"): pass
            elif (tk_type == "PRINT"): pass
            elif (tk_type == "RETURN"): return

            self.advance()