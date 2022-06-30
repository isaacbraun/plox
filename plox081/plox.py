# /plox/plox.py
# Isaac Braun
# CPTR-405

from cmath import exp
import sys
from Parser import Parser
from Scanner import Scanner
from AstPrinter import AstPrinter
from Interpreter import Interpreter

class Lox:
    def __init__(self):
        self.hadError = False
        self.hadRuntimeError = False
        self.interpreter = Interpreter(self)

    # https://www.tutorialspoint.com/python/python_command_line_arguments.htm
    def main(self, args):
        if (len(args) > 2):
            print( "Usage: plox [script]")
            sys.exit(64)
        elif (len(args) == 2):
            self.runFile(args[1])
        else:
            self.runPrompt()

    def runFile(self, path):
        with open(path, 'r') as f:
            source = f.read()
            self.run(source)

            if (self.hadError): sys.exit(0)
            if (self.hadRuntimeError): sys.exit(0)

    def runPrompt(self):
        try:
            while True:
                # print("> ", end = '')
                line = str(input())
                self.run(line)
                self.hadError = False
        except KeyboardInterrupt:
            print("\nExited Plox")
        except EOFError:
            pass
        
    def run(self, source):
        scanner = Scanner(source, self)
        tokens = scanner.scanTokens()
        # Stop if there was a scanning error
        if (self.hadError): return

        # UNCOMMENT for loop to test scanning - COMMENT OUT interpreter function call
        # for token in tokens:
        #     print(token)
        
        parser = Parser(tokens, self)

        statements = parser.parse()

        # Stop if there was a syntax error
        if (self.hadError): return

        self.interpreter.interpret(statements)

    def error(self, line, message):
        self.report(line, "", message)

    def runtimeError(self, error):
        print(error.getMessage() + "\n[line " + str(error.token.line) + "]")
        self.hadRuntimeError = True

    def parserError(self, token, message):
        if (token.token_type == "EOF"):
            self.report(token.line, " at end", message)
        else:
            self.report(token.line, " at '" + token.lexeme + "'", message)

    def report(self, line, where, message):
        print("[line " + str(line) + "] Error" + str(where) + ": " + str(message))
        self.hadError = True

if __name__ == "__main__":
    lox = Lox()
    lox.main(sys.argv)