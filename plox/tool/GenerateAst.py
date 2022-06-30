# /plox/tool/GenerateAst.py
# Isaac Braun
# CPTR-405

import sys

def main(args):
    if (len(args) != 2):
        print("Usage: generate_ast <output directory>")
        sys.exit(64)
    outputDir = args[1]
    defineAst(outputDir, "Expr", [
        "Assign   : Token name, Expr value",
        "Binary   : Expr left, Token operator, Expr right",
        "Grouping : Expr expression",
        "Literal  : Object value",
        "Logical  : Expr left, Token operator, Expr right",
        "Unary    : Token operator, Expr right",
        "Variable : Token name",
        "Ternary  : Expr condition, Expr ifTrue, Expr ifFalse",
    ])

    defineAst(outputDir, "Stmt", [
        "Block      : List<Stmt> statements",
        "Expression : Expr expression",
        "If         : Expr condition, Stmt thenBranch, Stmt elseBranch",
        "Print      : Expr expression",
        "Var        : Token name, Expr initializer",
        "While      : Expr condition, Stmt body",
    ])

def defineAst(outputDir, baseName, types):
    # https://www.pythontutorial.net/python-basics/python-write-text-file/
    path = outputDir + "/" + baseName + ".py"

    # Visitor Base Class
    lines = []
    lines.append("# /plox/Expr.py\n# Isaac Braun\n# CPTR-405\n")
    lines.append("class " + baseName + ":")
    lines.append((5 * " ") + "pass")
    lines.append("\n")

    for exprType in types:
        className = exprType.split(":")
        fields = className[1].strip()
        className = className[0].strip()

        fields = fields.split(",")
        for i, field in enumerate(fields):
            fields[i] = field.strip()
            fields[i] = fields[i].split(" ")
            fields[i] = fields[i][1]

        defineType(lines, baseName, className, fields)
        lines.append("\n")

    with open(path, 'w') as f:
        for line in lines:
            f.write(line)
            if (line != '\n'):
                f.write('\n')

def defineType(lines, baseName, className, fieldList):
    lines.append("class " + className + "(" + baseName + "):")

    # Constructor
    lines.append((5 * " ") + "def __init__(self, " + ", ".join(fieldList) + "):")
    for field in fieldList:
        lines.append((10 * " ") + "self." + field + " = " + field)
    lines.append("\n")

    # Visitor
    lines.append((5 * " ") + "def accept(self, visitor):")
    lines.append((10 * " ") + "return visitor.visit" + className + "(self)")

# https://www.geeksforgeeks.org/visitor-method-python-design-patterns/

if __name__ == "__main__":
    main(sys.argv)