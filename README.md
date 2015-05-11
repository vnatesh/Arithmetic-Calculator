# Arithmetic-Calculator


This program is a simple symbolic calculator for arithmetic operations. Expressions need to be entered in fully-parenthetized format (expression, operator, expression). The program can be run in either the terminal or IDLE and is initialized by typeing "calc()". For this reason, negative numbers must be entered in as (0-2) instead of simply (-2). Variables can also be stored and then manipulated arithmetically since the calculator creates its own environment within the python interpreter. You can exit the program by typing "quit". 


example:

>>> calc()
$ (((0-3)/(5+3))*(3-6))
$ 1.125
   env = {}
$ (a=23)
$  None
   env = {'a': 23.0}
$ (b=(a*(((0-3)/(5+3))*(3-6))))
   None
   env = {'a': 23.0, 'b': 25.875}
$
