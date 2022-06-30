[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-f059dc9a6f8d3a56e377f745f24479a46679e63a5d9fe6f495e02850cd0d8118.svg)](https://classroom.github.com/online_ide?assignment_repo_id=6870652&assignment_repo_type=AssignmentRepo)

# Plox - Isaac Braun
Python implementation of a Lox interpreter based on [Bob Nystrom's](https://github.com/munificent) implementation in his [Crafting Interpreters](http://www.craftinginterpreters.com/)
book.

# Testing
The 'manual-tests' directory contain other .lox files that can be used to test certain aspects of the plox system. Expected outputs are located in the 'test-output-files' directory.

# Challenges
- Challenge 8.1 (challenge081): Start with the interpreter at the end of Chapter 8. Make the REPL more flexible, so if the user enters a statement, you execute it, but if they enter an expression instead, you evaluate it and display the results value.
- Challenge 8.O (challenge08O): Extend the interpreter at the end of Chapter 8 (or 9) to add an exit statement that immediately quits the interpreter. (This one isn't in the book--it's my own addition.)
- Challenge 9.3 (challenge093): Add break and continue statements to the Lox interpreter at the end of Chapter 9. Each of those statements consist of just the keyword followed by a semicolon--it's the semantics that are interesting. Make sure they work (like they would in C) with both while and for loops. Having either one outside of a loop is a syntax error.
- Challenge 9.O (challenge09O): Enrich your Lox interpreter from the end of Chapter 9 with a switch-case construct. Like the C equivalent, the switch keyword is followed by an expression that will be compared for equality with the expression following each case in  its body. Unlike the C family of languages, this will not support case fall-through. Instead, each case will control a single statement (possibly a block), so the break statement at the end of the case is unnecessary (and may be a syntax error, depending on its placement). Don't forget the optional default alternative at the end! Will you de-sugar this into an if-else if...-else ladder? Or will you add a new AST node type?