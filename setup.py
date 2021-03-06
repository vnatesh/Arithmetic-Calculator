# created by Vikas Natesh


#!/usr/bin/env python


#######--------- SYMBOLIC CALCULATOR -----------#######


import string
import operator
import itertools


## The classes below define what data types/operators our tokens are and also the result of
## eager evaluation of instances of binary expressions


## BinaryOp defines out binary expression structure...there is a left and right
## value and we can use operator subclass instances to return the eagerly evaluated
## answer when two data type subclasses are operated on

class BinaryOp:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        return self.opStr + '(' + \
               str(self.left) + ', ' +\
               str(self.right) + ')'
    __repr__ = __str__



## Operators
    
class Sum(BinaryOp):
    opStr = 'Sum'
    def eval(self,env):
        return operator.__add__(self.left.eval(env),self.right.eval(env))
    
class Prod(BinaryOp):
    opStr = 'Prod'
    def eval(self,env):
        return operator.__mul__(self.left.eval(env),self.right.eval(env))
    
class Quot(BinaryOp):
    opStr = 'Quot'
    def eval(self,env):
        return operator.__div__(self.left.eval(env),self.right.eval(env))
    
class Diff(BinaryOp):
    opStr = 'Diff'
    def eval(self,env):
        return operator.__sub__(self.left.eval(env),self.right.eval(env))
    
class Assign(BinaryOp):
    opStr = 'Assign'
    def eval(self,env):
        a=self.right.eval(env)
        b=self.left.name
        env[b]=a



# Data types 

class Number:
    def __init__(self, val):
        self.value = val
    def eval(self,env):
        return self.value
    def __str__(self):
        return 'Num('+str(self.value)+')'
    __repr__ = __str__


class Variable:
    def __init__(self, name):
        self.name = name
    def eval(self,env):
        return env[self.name]
    def __str__(self):
        return 'Var('+self.name+')'
    __repr__ = __str__



## Lexical Analyzer (aka Lexer or tokenizer)...takes an expression and extracts the useful characters i.e.
## it converts an expression into a sequence of tokens...specifically, the program
## creates a sequences  of tokens by appending only certain types of token to the new list
## in our case, it ignores spaces...this means that the lexer takes in a regular grammar
## (in our case a seq of tokens) meaning that a lexer can be automated by a finite
## state machine (FSA, NFA, DFA) 



seps=['(',')','+','-','*','/','=']

def tokenize(inputString):
    list1=[]
    i=0
    while i<len(inputString):
        try:
            if inputString[i] in seps:
                list1.append(inputString[i])
                i+=1
            elif inputString[i]==' ':
                i+=1
            else:
                s=''
                x=0
                while inputString[i+x] not in seps and inputString[i+x]!=' ':
                    x+=1
                    s+=inputString[i+x-1]
                    if x>=len(inputString): break
                    
                    
                list1.append(s)                   
                i+=x
        except IndexError: break
    return [filter(lambda inp: inp!=' ',i) for i in list1]
                


## Parser...the parser takes the sequences of tokens (that were generated by
## the lexical analyser) and, using the rules of a particular context-free grammar,
## generates a syntax or parse tree...specifically, it takes the sequence and uses
## the classes we made to assign each token to its respective class (which is based
## on data type i.e. whether the token is a number, operator character, variable,
## or parentheses)...the parser takes in the token sequence and uses a top down, recursive
## descent algorithm to recursively assign tokens to classes. Once all the branches
## are made, the parser combines the new classes to create a parsed version of
## the original expression...in our case, our parser is structured such that it combines
## the newly generated objects according to our rule that input expressions are
## fully parenthetized i.e. there can only be a seq of (expression,operator,expression)
## for example: (1+(2*3))...here we have (1 , + , (2*3) ) as our complex expression
## and within the complex expression, there is a subexpression (2,*,3)...in other
## words, expressions can only be combined in a binary fashion (specifying binary operations between experssions)
## for example: (1+2*3+(4/5)) is not a valid expression input because subexpressions always must
## be enclosed in parens...the correct input would be (1+((2*3)+(4/5))
## Regular languages cannot specifiy nested syntax (in out case, subexpressions within larger complex expressions),
## so the parser cannot be implemented by a finite state machine
## (since we need to account for the fact that there can be infinite nesting
## of syntax and a finite state machine wouldn't be able to account for all
## states in the tree)...thus, parsers must be implemented as stacks, i.e. a context-free grammar
## This stack is used to represent the nesting level of the syntax. In practice,
## they're usually implemented as a top-down, recursive-descent parser which uses
## computer's procedure call stack to track the nesting level, and use recursively
## called procedures/functions for every non-terminal symbol in their syntax (i.e. all tokens except parens).


# token is a string
# returns True if contains only digits

def numberTok(token):
    for char in token:
        if not char in string.digits:
            if char!='.':
                return False
    return True

# token is a string
# returns True its first character is a letter

def isNum(thing):
    return type(thing) == int or type(thing) == float



def variableTok(token):
    for char in token:
        if char in string.letters: return True
    return False


def parse(tokens):
    def parseExp(index):
        if numberTok(tokens[index]):
            return (Number(float(tokens[index])),index+1)
        elif variableTok(tokens[index]):
            return (Variable(tokens[index]),index+1)
        else:
            leftTree=parseExp(index+1)
            index=leftTree[1]
            op=tokens[index]
            rightTree=parseExp(index+1)
            index=rightTree[1]
            if op=='+':
                return (Sum(leftTree[0],rightTree[0]),index+1)
            elif op=='-':
                return (Diff(leftTree[0],rightTree[0]),index+1)
            elif op=='*':
                return (Prod(leftTree[0],rightTree[0]),index+1)
            elif op=='/':
                return (Quot(leftTree[0],rightTree[0]),index+1)
            elif op=='=':
                return (Assign(leftTree[0],rightTree[0]),index+1)
    (parsedExp, nextIndex) = parseExp(0)
    return parsedExp


# Run calculator interactively in a "command-line" style with its own environment


def calc():
    env={}
    while True:
        e = raw_input('$ ')
        if e=='quit': break
        try:
            print '$ ', str(parse(tokenize(e)).eval(env))
            print '   env =', env
        except KeyError:
            print 'you entered a new variable without assigning it first'



### Tokenizing State Machine
# Implements the tokenize function as a state machine instead of an imperative procedure
# The lexer here is a finite state machine


class SM:
    def start(self):
        self.state = self.startState
    def step(self,inp):
        (s,o) = self.getNextValues(self.state,inp)
        self.state = s
        return o
    
    def transduce(self,inputs):
        self.start()
        return list(itertools.chain(*[self.step(inp) for inp in inputs]))

    def current_state(self):
        return self.state



class Tokenizer(SM):
    startState='off'
    m=''
    s=''
    def getNextValues(self,state,inp):
        if state=='off':
            if inp in seps:
                return ('off',[inp])
            elif inp==' ':
                return ('off',[self.m])
            else:
                self.m+=inp
                return ('on',[''])
        elif state=='on':
            if inp in seps:
                a=self.m
                self.m=''
                return ('off',[a,inp])
            elif inp==' ':
                a=self.m
                self.m=''
                return ('off',[a])
            else:
                self.m+=inp
                return ('on',[''])


def tokenize(inputString):
    inputString+=' '
    return filter(lambda x: x!='', Tokenizer().transduce(inputString))
    

    
