# Pascal Processor Project
*Jackson Randolph: jrando13@students.kennesaw.edu*

*Kennesaw State University*

*College of Computing and Software Engineering*

*Department of Computer Science*

*CS 4308/W01 Concepts of Programming Languages*

## Problem
The study of compilers and interpreters is important to understanding the nature of programming languages, therefore this project aims to implement an interpreter for the Pascal language.

## Summary and Purpose
This report covers the implementation of a basic interpreter for Pascal that is used with the scanner and parser previously created that can run introductory programs with console input/output and arithmetic. Acceptable output for this interpreter would be the appropriate output for the input programs, which implement basic input/ouput and arithmetic.

## Solution
One way to write a new interpreter is to use “compiler generator” software. Lex and Yacc are two established tools to do this. Since Lex was used to build the scanner, Yacc was used for building the parser. Yacc takes in grammar rules and allows them to be associated with procedures. From these rules, it generates a set of parser rules and states which are used to parse input. This project uses a python version of these tools called Python Lex-Yacc (PLY). This generated parser was used as the basis of the interpreter.

In addition to the parser, an interpreter helper library was created that includes several key functions: the IO functions, Readln, Write, and Writeln, in addition to an expression evaluator and accessors for a symbol table that the interpreter class maintains. Also included is a symbol class designed to keep track of symbol types and data to help simulate strong typing.

The parser was modified from the second deliverable by including an instance of the interpreter class that was used inside of the grammar actions to execute the program. The majority of grammar actions were kept the same, however print statements were removed inside of them, and in some cases symbols now "bubble up" instead of strings or other objects. Symbols are also created inside some grammar actions, such as in the variable declaration action. In the assignment statement action, the parser calls the interpreter's evaluate method to evaluate the expression on the right side and uses the interpreter's setsym method to simulate assignment. In the function statement action, the function symbol is unwrapped from the function_designator rule and since the data property is a python function, it can be executed directly.

Some challenges were encountered with passing by reference. In Pascal, the Readln method takes in a variable as a pointer and assigns the output to the variable, in a manner like C#'s out keyword. Python doesn't allow pointers, so simulating this behavior required some experimentation. To tackle this, expressions are passed into the functions as expressions. Since only the IO methods are defined, I manually handled each expression inside the method: if a reference was needed, then the symbol was kept, if not, then the expression was passed to evaluate to dereference it. In another iteration, this behavior should be handled in a manner like how grammar rules are defined in the parser, and the dereferencing logic should be handled in another method, also a part of the interpreter class.
Testing was done with test.py and sends the input files to the parser/interpreter for execution.

## Conclusions
The interpreter works for the programs in the test-files directory without error, however if I were to re-do this project, I would want to use a lower level language or experiment with a functional language. Some initial research was done into building an interpreter with Haskell, a purely functional language, and it looked to be very elegant. The only issue is that I don't have a strong background with functional languages and therefore I didn't feel comfortable in doing this project in one. Additionally, pointers would have made things a lot cleaner, so while C++ may have been too much of a headache, I could have made do with C# (or maybe Java) by wrapping things in classes.
