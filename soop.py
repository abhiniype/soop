from sys import *
import re

tokens = []
num_stack = []

keywords = ['write', 'explain', 'describe', 'suppose', 'orif', 'otherwise', 'give_back', 'with','yes', 'no', 'nothing', 'do', '...until', '...while', 'forevery', 'count', 'starting', 'skipping', 'till']

symbols = {}

def open_file(filename):
    data = open(filename, "r").read()
    data += "<EOF>"
    return data
    
def lex(filecontents):
    token = ""
    state = 0 # 0 = outside a string, 1 = inside a string
    string = ""
    varStarted = 0
    var = ""
    isexpr = 0
    expr = "" #numerical expresions
    n = ""
    filecontents = list(filecontents)
    for char in filecontents:
        token += char
        if token == " ": #Takes Care of Spaces
            
            if state == 0:
                token = ""
            else:
                token = " "
                
                
        elif token == "\n" or token == "<EOF>": #Takes care of Newline and the End of File 
            
            if expr != "" and isexpr == 1:
                tokens.append("EXPR:" + expr)
                expr = ""
                
            elif expr != "" and isexpr == 0:
                tokens.append("NUM:" + expr)
                expr = ""
                
            elif var != "":
                tokens.append("VAR:" + var)
                var = ""
                varStarted = 0
            token = ""
        
        elif token == "=" and state == 0: 
            if var != "":
                tokens.append("VAR:" + var)
                var = ""
                varStarted = 0
            tokens.append("EQUALS")
            token = ""
          
        elif token == "$" and state == 0:
            varStarted = 1
            var += token
            token = ""
        
        elif varStarted == 1:
            if token == "<" or token == ">":
                if var != "":
                    tokens.append("VAR:" + var)
                    var = ""
                    varStarted = 0

            var += token
            token = ""
            
            
        elif token == "write":
            tokens.append("PRINT")
            token = ""
            
        elif token == "ask":
            tokens.append("INPUT")
            token = ""

        elif re.search('^[0-9]+$', token):
            expr += token
            token = ""
            
            
        elif token == "+" or token == "-" or token == "*" or token == "/" or token == "(" or token == ")" or token == "%" :
            isexpr = 1
            expr += token
            token = ""
            
            
        elif token == "\"" or token == " \"":
            
            if state == 0:
                state = 1
            elif state == 1:
                tokens.append("STRING:" + string + "\"")
                string = ""
                state = 0
                token = ""
                
                
        elif state == 1:
            string += token
            token = ""
            
    #print(tokens)
    return tokens
    #return ''


def assignVar(varName, varValue):
    symbols[varName[4:]] = varValue
    
def getVar(varName):

    varName = varName[4:]
    if varName in symbols:
        varValue = symbols[varName]
        if varValue[0:6] == "STRING":
            varValue = varValue[8:-1]
        elif varValue[0:3] == "NUM":
            varValue = varValue[4:]
        elif varValue[0:4] == "EXPR":
            varValue = varValue[5:]
        return varValue
    else:
        return "\n\nWHAT !!!!?!!!?!!!?!!! \n\t We have never heard of the variable " + varName+ " in Our Lives!"
        exit()

def getInput(string, varName):
    i = input(string[1:-1])
    symbols[varName] = "STRING:" + "\"" + i + "\""

def parse(toks):
    i = 0
    while(i < len(toks)):
        
        if toks[i] + " " + toks[i+1][0:6] == "PRINT STRING" or toks[i] + " " + toks[i+1][0:3] == "PRINT NUM" or toks[i] + " " + toks[i+1][0:4] == "PRINT EXPR" or toks[i] + " " + toks[i+1][0:3] == "PRINT VAR":
            if  toks[i+1][0:6] == "STRING":
                print(toks[i+1][8:-1])
                i+=2
                
            elif  toks[i+1][0:3] == "NUM":
                print( toks[i+1][4:])
                i+=2
            
            elif toks[i+1][0:3] == "VAR":
                print(getVar(toks[i+1]))
                i+=2

            elif  toks[i+1][0:4] == "EXPR": 
                print( eval(toks[i+1][5:]))
                 
                i+=2
        elif toks[i][0:3] + " " + toks[i+1] + " " + toks[i+2][0:6] == "VAR EQUALS STRING" or toks[i][0:3] + " " + toks[i+1] + " " + toks[i+2][0:3] == "VAR EQUALS NUM" or toks[i][0:3] + " " + toks[i+1] + " " + toks[i+2][0:4] == "VAR EQUALS EXPR" or toks[i][0:3] + " " + toks[i+1] + " " + toks[i+2][0:3] == "VAR EQUALS VAR":
            
            
            if  toks[i+2][0:6] == "STRING":
                assignVar(toks[i], toks[i+2])
                #i+=2
            
            elif  toks[i+2][0:3] == "NUM":
                assignVar(toks[i], toks[i+2])
                #i+=2

            elif  toks[i+2][0:3] == "VAR":
                assignVar(toks[i], getVar(toks[i+2]))
                #i+=2
            
            elif  toks[i+2][0:4] == "EXPR":
                assignVar(toks[i], "NUM:" + str(eval(toks[i+2][5:])))
            

            i+=3
        elif toks[i] + " " + toks[i+1][0:6] + " " + toks[i+2][0:3] == "INPUT STRING VAR":
            getInput(toks[i+1][7:], toks[i+2][4:])
            
            i += 3
    #print(symbols)
    
def run():
    data = open_file(argv[1])
    toks = lex(data)
    parse(toks)
    
    
run()