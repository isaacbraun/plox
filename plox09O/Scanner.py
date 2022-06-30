# /plox/Scanner.py
# Isaac Braun
# CPTR-405

from TokenType import TokenType
from Token import Token

class Scanner(object):
    def __init__(self, source: str, lox):
        self.source = source
        self.tokens = []
        self.start = 0
        self.current = 0
        self.line = 1
        self.lox = lox

    def scanTokens(self):
        while (not self.isAtEnd()):
            self.start = self.current
            self.scanToken()
        
        self.tokens.append(Token("EOF", "", None, self.line))
        return self.tokens

    def scanToken(self):
        c = self.advance()
        
        # Check for newline char
        if (c == '\n'):
            self.line += 1
        # Handle SLASH with check for comment
        elif (c == '/'):
            if self.match('/'):
                while ( (self.peek() != '\n') and (not self.isAtEnd()) ):
                    self.advance()
            else:
                self.addSingleToken("SLASH")
        # Check for String Literal
        elif (c == '"'):
            self.string()
        # Check for Number Literal
        elif self.isDigit(c):
            self.number()
        # IF statement ignores meaningless chars
        elif ((c == '\t') or (c == '\r') or (c == ' ')):
            pass
        else:
            # find maximal munch of chars in LiteralTokenTypes
            possible_token = None
            for token_type in TokenType.LiteralTokenTypes:
                lexeme = TokenType.LiteralTokenTypes[token_type]
                if (lexeme.startswith(c)):
                    if ( (possible_token is None) or self.match(lexeme[1]) ):
                        possible_token = (token_type, lexeme)
            if (possible_token is not None):
                self.addSingleToken(possible_token[0])
            # If not Literal, check for Alpha
            elif (self.isAlpha(c)):
                self.identifier()
            # Else: unexpected character
            else:
                self.lox.error(self.line, "Unexpected character.")

    def identifier(self):
        while (self.isAlphaNumeric(self.peek())):
            self.advance()

        text = self.source[self.start : self.current]
        tempType = None
        if text in TokenType.Keywords:
            tempType = TokenType.Keywords[text]
        if (tempType == None):
            tempType = "IDENTIFIER"
        self.addSingleToken(tempType)

    def string(self):
        while ( (self.peek() != '"') and (not self.isAtEnd()) ):
            if (self.peek() == '\n'):
                self.line += 1
            self.advance()

        if (self.isAtEnd()):
            self.lox.error(self.line, "Unterminated string.")
            return
        
        self.advance()

        value = self.source[self.start + 1 : self.current - 1]
        self.addToken("STRING", value)

    def number(self):
        while (self.isDigit(self.peek())):
            self.advance()
        
        # Look for a fractional part.
        if ( (self.peek() == '.') and (self.isDigit(self.peekNext())) ):
            # Consume the "."
            self.advance()

            while (self.isDigit(self.peek())) :
                self.advance()

        self.addToken("NUMBER", float(self.source[self.start : self.current]))

    def isDigit(self, c):
        return '0' <= c <= '9'

    def match(self, expected):
        if self.isAtEnd():
            return False
        elif (self.source[self.current] != expected):
            return False

        self.current += 1
        return True
    
    def peek(self):
        if self.isAtEnd():
            return '\0'
        return self.source[self.current]

    def peekNext(self):
        if ( (self.current + 1) >= len(self.source) ):
            return '\0'
        return self.source[self.current + 1]

    def isAlpha(self, c):
        return (c >= 'a' and c <= 'z') or (c >= 'A' and c <= 'Z') or (c == '_')

    def isAlphaNumeric(self, c):
        return self.isAlpha(c) or self.isDigit(c)

    def isAtEnd(self):
        return self.current >= len(self.source)

    def advance(self):
        nextChar = self.source[self.current]
        self.current += 1
        return nextChar

    def addSingleToken(self, tempType):
        self.addToken(tempType, None)

    def addToken(self, tempType, literal):
        text = self.source[self.start : self.current]
        self.tokens.append(Token(tempType, text, literal, self.line))