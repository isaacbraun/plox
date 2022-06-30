# /plox/TokenType.py
# Isaac Braun
# CPTR-405

class TokenType():
    LiteralTokenTypes = {
        "L_PAREN" : "(",
        "R_PAREN" : ")",
        "L_BRACE" : "{",
        "R_BRACE" : "}",
        "COMMA" : ",",
        "COLON" : ":",
        "DOT" : ".",
        "MINUS" : "-",
        "PLUS" : "+",
        "SEMICOLON" : ";",
        "STAR" : "*",
        "BANG" : "!",
        "BANG_EQ" : "!=",
        "EQ" : "=",
        "IS_EQ" : "==",
        "GR" : ">",
        "GR_EQ" : ">=",
        "LT" : "<",
        "LT_EQ" : "<=",
        "QUESTION" : "?",
    }

    Keywords = {
        "and" : "AND",
        "case" : "CASE",
        "class" : "CLASS",
        "default" : "DEFAULT",
        "else" : "ELSE",
        "false" : "FALSE",
        "fun" : "FUN",
        "for" : "FOR",
        "if" : "IF",
        "nil" : "NIL",
        "or" : "OR",
        "print" : "PRINT",
        "return" : "RETURN",
        "switch" : "SWITCH",
        "super" : "SUPER",
        "this" : "THIS",
        "true" : "TRUE",
        "var" : "VAR",
        "while" : "WHILE",
    }

    RegexTokenTypes = {
        "IDENTIFIER" : "[A-Za-z][A-Za-z_0-9]*",
        "STRING" : '"[^"]*"',
        "NUMBER" : "[0-9]*(.[0-9]+)?",
    }