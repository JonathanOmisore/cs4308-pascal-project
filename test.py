from scanner import Scanner

def printTokens(lex):
    while True:
        tok = lex.token()
        if not tok:
            break
        print(tok)

def readFile(fname, lex):
    file = open(fname, 'r')
    for line in file.readlines():
        lex.input(line)
        printTokens(lex)

def testFile(fname):
    lex = Scanner()
    lex.build()
    
    readFile(fname, lex.Lexer)

print("----------")
print("Testing helloworld.pas")
print("----------")
testFile("./test-files/helloworld.pas")
print()
print()

print("----------")
print("Testing helloworld_collapsed.pas")
print("----------")
testFile("./test-files/helloworld_collapsed.pas")
print()
print()

print("----------")
print("Testing io_example.pas")
print("----------")
testFile("./test-files/io_example.pas")
print()
print()