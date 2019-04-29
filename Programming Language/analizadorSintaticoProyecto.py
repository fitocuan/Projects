import ply.yacc as yacc
import os
import codecs
import re
from sys import stdin
import numpy as np


from analizadorLexicoProyecto import tokens


sym_table, operandos, quad, avail, saltos, saltos_exit, saltos_elsif = [],[],[],[],[],[],[]
inc = 0
cont = 0
cont_saltos=0
var = []
incremento = []
counter_sym = 0

def p_program(p):
	'''P : PROGRAM ID V S END PROGRAM sub'''



def p_V(p):
	'''V 	: data_type ID V
			| data_type ID LPARENT NUMBER COMMA NUMBER RPARENT V
			| data_type ID LPARENT NUMBER RPARENT V
		 	| empty
		 	'''
	global counter_sym

 	if len(p) == 4:
		sym_table.append({'count':counter_sym,'type':p[1], 'id' : p[2], 'dim' : 0,'base' : 1, 'value' : np.zeros(1)})
		counter_sym += 1

	if len(p) == 9:
		sym_table.append({'count':counter_sym,'type':p[1], 'id' : p[2], 'dim' : 2,'base' : p[4], 'value' : np.zeros((p[4]*p[6]))})

		counter_sym += p[4]*p[6]
	if len(p) == 7:
		sym_table.append({'count':counter_sym,'type':p[1], 'id' : p[2], 'dim' : 1,'base' : p[4], 'value' : np.zeros(p[4])})
		counter_sym += p[4]


def p_data_type(p):
	''' data_type 	: INTEGER
					| REAL
					'''
	p[0] = p[1]

def p_ea(p):
	''' EA	: EA SUMA EA2
			| EA RESTA EA2
			| EA2
	'''
	global cont
	global cont_saltos
	if len(p) == 4:
		op2 = operandos.pop()
		op1 = operandos.pop()
		quad.append({'1' : str(p[2]), '2' : op1, '3' : op2, '4' : 't'+str(cont)})
		operandos.append('t'+str(cont))
		cont_saltos+=1
		cont+=1

def p_ea2(p):
	''' EA2 : EA2 ASTERISCO EA3
			| EA2 DIV EA3
			| EA3
	'''
	global cont
	global cont_saltos
	if len(p) == 4:
		op2 = operandos.pop()
		op1 = operandos.pop()
		quad.append({'1' : str(p[2]), '2' : op1, '3' : op2, '4' : 't'+str(cont)})
		operandos.append('t'+str(cont))
		cont+=1
		cont_saltos+=1


def p_ea3(p):
	''' EA3 : ID
			| NUMBER
			| FLOAT
			| LPARENT EA RPARENT
			| ID LPARENT EA RPARENT
			| ID LPARENT EA COMMA EA RPARENT
	'''

	if len(p) == 2 and str(type(p[1])) == '<type \'unicode\'>':
		operandos.append(findInSystemTable(str(p[1]),0,0))
		
	if len(p) == 2 and str(type(p[1])) == '<type \'int\'>':
		operandos.append(str(p[1])+'c')
		
	if len(p) == 2 and str(type(p[1])) == '<type \'float\'>':
		operandos.append(str(p[1])+'c')
		
		
	if len(p) == 5:
		op1 = operandos.pop()
		
		if str(type(op1)) == '<type \'int\'>':
			op1 = (str(p[1]),str(op1) + 'v')
		else:
			op1 = findInSystemTable(str(p[1]),op1,0)
		
		operandos.append(op1)
		
	if len(p) == 7:
		op1 = operandos.pop()
		op2 = operandos.pop()
		
		
		
		if str(type(op1)) == '<type \'int\'>' or str(type(op2)) == '<type \'int\'>':
			op2 = (str(p[1]),str(op1) + 'v', str(op2) + 'v')
		else:
			op2 = findInSystemTable(str(p[1]),op1,op2)
		
		
		operandos.append(op2)

def p_el(p):
	''' EL	: EL OR EL2
			| EL2
	'''
	global cont
	global cont_saltos
	if len(p) == 4:
		quad.append({'1' : str(p[2]), '2' : operandos.pop(), '3' : operandos.pop(), '4' : 't'+str(cont)})
		operandos.append('t'+str(cont))
		cont+=1
		cont_saltos+=1

def p_el2(p):
	''' EL2	: EL3
			| EL2 AND EL3
	'''
	global cont
	global cont_saltos
	if len(p) == 4:
		quad.append({'1' : str(p[2]), '2' : operandos.pop(), '3' : operandos.pop(), '4' : 't'+str(cont)})
		operandos.append('t'+str(cont))
		cont+=1
		cont_saltos+=1

def p_el3(p):
	''' EL3 : NOT EL4
			| NOT EL3
			| EL4
	'''
	global cont
	global cont_saltos
	if len(p) == 3:
		quad.append({'1' : str(p[1]), '2' : operandos.pop(), '3' : None , '4' : 't'+str(cont)})
		operandos.append('t'+str(cont))
		cont+=1
		cont_saltos+=1


def p_el4(p):
	''' EL4	: EL5 LESS EL5
			| EL5 MORE EL5
			| EL5 LESSEQUAL EL5
			| EL5 MOREEQUAL EL5
			| EL5 NOTEQUAL EL5
			| EL5 EQUAL EL5
			| LPARENT EL RPARENT
	'''
	global cont
	global cont_saltos
	if len(p) == 4:
		op2 = operandos.pop()
		op1 = operandos.pop()
		quad.append({'1' : str(p[2]), '2' : op1, '3' : op2, '4' : 't'+str(cont)})
		operandos.append('t'+str(cont))
		cont+=1
		cont_saltos+=1

def p_el5(p):
	''' EL5	: ID
			| NUMBER
			| FLOAT
			| LPARENT EA RPARENT
			| ID LPARENT EA RPARENT
			| ID LPARENT EA COMMA EA RPARENT
	'''
	if len(p) == 2 and str(type(p[1])) == '<type \'unicode\'>':
		operandos.append(findInSystemTable(str(p[1]),0,0))
		
	if len(p) == 2 and str(type(p[1])) == '<type \'int\'>':
		operandos.append(str(p[1])+'c')
		
	if len(p) == 2 and str(type(p[1])) == '<type \'float\'>':
		operandos.append(str(p[1])+'c')
		
		
	if len(p) == 5:
		op1 = operandos.pop()
		
		if str(type(op1)) == '<type \'int\'>':
			op1 = (str(p[1]),str(op1) + 'v')
		else:
			op1 = findInSystemTable(str(p[1]),op1,0)
		
		operandos.append(op1)
		
	if len(p) == 7:
		op1 = operandos.pop()
		op2 = operandos.pop()
		
		
		
		if str(type(op1)) == '<type \'int\'>' or str(type(op2)) == '<type \'int\'>':
			op2 = (str(p[1]),str(op1) + 'v', str(op2) + 'v')
		else:
			op2 = findInSystemTable(str(p[1]),op1,op2)
		
		
		operandos.append(op2)


def findNum(num):
	c = 0
	c2 = 0
	for idx,item in enumerate(sym_table):		
		for i in item['value']:
			if c == num:
				return idx, c-c2
			c += 1
		c2 += item['value'].size

def p_s(p):
	''' S	: ass S
			| assmat1 S
			| assmat2 S
			| READ read_r S
			| PRINT print_r S
			| CALL ID LPARENT RPARENT S
			| DO LPARENT loop2 loop3 COMMA EL loop1 loop6 RPARENT S loop7 enddo1 S
			| DO loop4 S END DO loop5 S
			| IF if4 else else2 END IF if3 S
			| EXIT exit S
			| empty
	'''

def p_assmat1(p):
	'''assmat1 : ID LPARENT EA RPARENT ASSIGN EA
	'''
	global cont_saltos
	op1 = operandos.pop()
	op2 = operandos.pop()


	if str(type(op2)) == '<type \'int\'>':
		op2 = (str(p[1]),str(op2) + 'v')
	else:
		op2 = findInSystemTable(str(p[1]),op2,0)

	
	quad.append({'1' : str(p[5]), '2' : op2, '3' : op1, '4' : None})
	cont_saltos+=1
	#var.append(findInSystemTable(str(p[1]),op2,0))

def p_assmat2(p):
	'''assmat2 : ID LPARENT EA COMMA EA RPARENT ASSIGN EA
	'''
	global cont_saltos

	
	op1 = operandos.pop()
	op2 = operandos.pop()
	op3 = operandos.pop()
	
	if str(type(op2)) == '<type \'int\'>' or str(type(op3)) == '<type \'int\'>':
		op2 = (str(p[1]),str(op2) + 'v', str(op3) + 'v')
	else:
		op2 = findInSystemTable(str(p[1]),op2,op3)
	
	
	quad.append({'1' : str(p[7]), '2' : op2, '3' : op1, '4' : None})
	cont_saltos+=1
	#var.append(findInSystemTable(str(p[1]),op2,op3))

def p_ass(p):
	'''ass : ID ASSIGN EA
	'''
	global cont_saltos

	
	quad.append({'1' : str(p[2]), '2' : findInSystemTable(str(p[1]),0,0), '3' : operandos.pop(), '4' : None})
	cont_saltos+=1
	#var.append(findInSystemTable(str(p[1]),0,0))

def p_loop6(p):
	'''loop6	:	COMMA EA loop8
				|	empty
	'''


def p_loop8(p):
	'''loop8	:	empty
	'''
	global inc
	global incremento
	incremento.append(operandos.pop())
	inc +=1


def p_loop7(p):
	'''loop7	:	empty
	'''
	global inc
	global cont
	
	if inc > 0:
		var1 = var.pop()
		global cont_saltos
		quad.append({'1' : '+', '2' : var1, '3' : incremento.pop(), '4' : 't'+str(cont)})
		quad.append({'1' : '=', '2' : var1, '3' : 't'+str(cont), '4' : ' '})
		cont_saltos+=2
		inc -= 1
		cont+=1




def p_else(p):
	'''else	: EL if1 THEN S if5 ELSIF else
			| EL if1 THEN S
			| empty
	'''

def p_else2(p):
	'''else2	: ELSE if2 S
			| empty

	'''

def p_if4(p):
	'''if4	:	empty'''
	global cont_saltos
	saltos_elsif.append('x')

def p_if5(p):
	'''if5	:	empty'''
	global cont_saltos
	quad.append({'1' : 'GoTo', '2' : ' ', '3' : ' ', '4' : ' '})
	cont_saltos+=1
	saltos_elsif.append(cont_saltos-1)
	dir = saltos.pop()
	rellenar(dir,cont_saltos)
	saltos.append(cont_saltos-1)

def p_if1(p):
	'''if1	:	empty'''
	e = operandos.pop()
	global cont_saltos
	quad.append({'1' : 'GoToF', '2' : e, '3' : 'x', '4' : ' '})
	cont_saltos+=1
	saltos.append(cont_saltos-1)

def p_if2(p):
	'''if2	:	empty'''
	global cont_saltos
	quad.append({'1' : 'GoTo', '2' : ' ', '3' : 'x', '4' : ' '})
	cont_saltos+=1
	dir = saltos.pop()
	rellenar(dir,cont_saltos)
	saltos.append(cont_saltos-1)

def p_if3(p):
	'''if3	:	empty'''
	global cont_saltos
	dir = saltos.pop()
	rellenar(dir,cont_saltos)

	while(saltos_elsif[-1]  != 'x'):
		dir = saltos_elsif.pop()
		rellenar(dir,cont_saltos)
		if len(saltos_elsif) == 1:
			saltos_elsif.pop()
			break





def p_loop5(p):
	'''loop5	:	empty
	'''
	print("loop5")
	global cont_saltos
	dir = saltos.pop()
	quad.append({'1' : "GoTo", '2' : ' ', '3' : str(dir), '4' : ' '})
	cont_saltos+=1
	while(saltos_exit[-1]  != 'x'):
		dir = saltos_exit.pop()
		rellenar(dir,cont_saltos)
		if len(saltos_exit) == 1:
			saltos_exit.pop()
			break

def p_exit(p):
	'''exit : empty
	'''
	print("exit")
	global cont_saltos
	saltos_exit.append(cont_saltos)
	quad.append({'1' : "GoTo", '2' : ' ', '3' : "x", '4' : ' '})
	cont_saltos+=1

def p_loop4(p):
	'''loop4	:	empty
	'''
	print("loop4")
	global cont_saltos
	saltos.append(cont_saltos)
	saltos_exit.append('x')


def p_loop3(p):
	'''loop3	:	 ID ASSIGN EA
	'''
	global cont_saltos
	quad.append({'1' : str(p[2]), '2' : findInSystemTable(str(p[1]),0,0), '3' : operandos.pop(), '4' : None})
	cont_saltos+=1
	var.append(findInSystemTable(str(p[1]),0,0))


def p_enddo1(p):
	'''enddo1 : END DO'''
	global cont_saltos
	dir1 = saltos.pop()
	dir2 = saltos.pop()
	quad.append({'1' : "GoTo", '2' : ' ', '3' : str(dir2+1), '4' : ' '})
	cont_saltos+=1
	rellenar(dir1,cont_saltos)

def p_loop1(p):
	'''loop1	: empty'''
	global cont_saltos
	e = operandos.pop()
	quad.append({'1' : "GoToF", '2' : e, '3' : "x", '4' : ' '})
	cont_saltos+=1
	saltos.append(cont_saltos-1)

def p_loop2(p):
	'''loop2	: empty'''
	global cont_saltos
	saltos.append(cont_saltos)






def p_read_r(p):
	'''read_r	: ID 
				| ID LPARENT EA COMMA EA RPARENT 
				| ID LPARENT EA RPARENT
	'''
	global cont_saltos
	
	if len(p) == 2:
		num = findInSystemTable(str(p[1]),0,0)
	elif len(p) == 7:
		op1 = operandos.pop()
		op2 = operandos.pop()
		num = findInSystemTable(str(p[1]),op1,op2)
	elif len(p) == 5:
		op1 = operandos.pop()
		num = findInSystemTable(str(p[1]),op1,0)
	elif len(p) == 3:
		num = p[1]
		
	quad.append({'1' : "read", '2' : ' ', '3' : num, '4' : ' '})
	cont_saltos+=1
	
	
	
def p_a(p):
	'''a	: empty'''

def p_print_r(p):
	'''print_r	: ID 
				| STRING a
				| ID LPARENT EA COMMA EA RPARENT 
				| ID LPARENT EA RPARENT
	'''
	global cont_saltos
	
	if len(p) == 2:
		num = findInSystemTable(str(p[1]),0,0)
	elif len(p) == 7:
		op1 = operandos.pop()
		op2 = operandos.pop()
		
		if str(type(op1)) == '<type \'int\'>' or str(type(op2)) == '<type \'int\'>':
			num = (str(p[1]),str(op1) + 'v', str(op2) + 'v')
		else:
			num = findInSystemTable(str(p[1]),op1,op2)	

	elif len(p) == 5:
		op1 = operandos.pop()
		if str(type(op1)) == '<type \'int\'>':
			num = str(op1) + 'v'
		else:
			num = findInSystemTable(str(p[1]),op1,0)
		
	elif len(p) == 3:
		num = p[1]
		
	quad.append({'1' : "print", '2' : ' ', '3' : num, '4' : ' '})
	cont_saltos+=1

def p_sub(p):
	''' sub	: SUBROUTINE ID S END SUBROUTINE sub
			| empty
	'''

def p_empty(p):
	'''empty :'''
	pass


def rellenar(dire, conts):
	quad[dire]['3'] = conts


def buscarFicheros(directorios):
	ficheros = []
	numArchivos = ''
	respuesta = False
	cont = 1

	for base, dirs, files in os.walk(directorios):
		ficheros.append(files)

	for f in files:
		print str(cont) + ". " + f
		cont = cont + 1

	while respuesta == False:
		numArchivo = raw_input('\nNumero del test: ')
		for f in files:
			if f == files[int(numArchivo)-1]:
				respuesta = True
				break

	print "Has escogido \"%s\ \n" % files[int(numArchivo)-1]
	return files[int(numArchivo)-1]



def findInSystemTable(var,i,i2):
	for item in (sym_table):
		if item['id'] == var:

			if i != 0 and i2 != 0:
				return item['count']+(int(i[:-1])-1)*item['base']+int(i2[:-1]) -1 
			elif i != 0:
				
				return item['count']+(int(i[:-1])-1)
			else :
				return item['count']
	print('NO SE DECLARO LA VARIABLE \'{}\''.format(var))

directorio = '/home/fitocuan/Documents/ITESM/6/AnalizadorLex/ply-3.11/test2/'
archivo = buscarFicheros(directorio)
test = directorio+archivo
fp = codecs.open(test,"r","utf-8")
cadena = fp.read()
fp.close()

parser = yacc.yacc()
result = parser.parse(cadena)
print('\n')
print(result)
#print(operandos)

print(saltos_elsif)

print('\n')



print('\n')


		
		
			
def printSymTable():
	print('\n')
	print("TABLA DE SIMBOLOS")
	for item in (sym_table):
		print('{}){} \t {} \t {} \t value : \n{} '.format(item['count'], item['id'], item['type'], item['dim'],item['value']))
	print('\n')
	
	
def printQuad():
	print('\n')
	print("CODIGO INTERMEDIO")
	for idx,item in enumerate(quad):
		print('{}) \t {} \t {} \t {} \t {}'.format(idx, item['1'], item['2'], item['3'], item['4']))
	print('\n')
	
					
printSymTable()
printQuad()



import operator
avail = [0]*cont
operator = {'+' : operator.add,
        '-' : operator.sub,
        '*' : operator.mul,
        '/' : operator.div,
        '<' : operator.lt,
        '>' : operator.gt,
        '>=' : operator.ge,
        '<=' : operator.le,
        '==' : operator.eq,
        '<>' : operator.ne}

print('\nOUTPUT DE PROGRAMA')


cp = 0



while cp != len(quad):

	item = quad[cp]
	if item['1'] == '=':

		if str(type(item['3'])) == '<type \'int\'>':
			x,y = findNum(item['3'])
			num2 = int(sym_table[x]['value'][y])
		elif str(type(item['3'])) == '<type \'float\'>':
			x,y = findNum(item['3'])
			num2 = float(sym_table[x]['value'][y])
		elif str(type(item['3'])) == '<type \'tuple\'>' and len(item['3']) == 3:
			x,y = findNum(int(item['3'][1][:-1]))
			val1 = (sym_table[x]['value'][y])
			x,y = findNum(int(item['3'][2][:-1]))
			val2 = (sym_table[x]['value'][y])
			
			val3 = findInSystemTable(item['3'][0],str(int(val1))+'c',str(int(val2))+'c')
			
			x,y = findNum(val3)	
			num2 = (sym_table[x]['value'][y])
		
		else:
			if item['3'][0] == 't':
				num2 = avail[int(item['3'][1:])]
			elif item['3'][-1] == 'c':
				num2 = (item['3'][:-1])
			else:

				x,y = findNum(int(item['3'][1][:-1]))
				val = (sym_table[x]['value'][y])
				val = findInSystemTable(item['3'][0],str(int(val))+'c',(0))
				x,y = findNum(val)
				num2 = (sym_table[x]['value'][y])
			
		num = num2
		num = str(num)

		num = int(num) if num.find('.') == -1 else float(num)
		

		
		if str(type(item['2'])) != '<type \'int\'>' and str(type(item['2'])) == '<type \'tuple\'>' and len(item['2']) == 2:
		
			x,y = findNum(int(item['2'][1][:-1]))
			val = (sym_table[x]['value'][y])
			
			val2 = findInSystemTable(item['2'][0],str(int(val)) + 'c',0)

			x,y = findNum(val2)
		
		elif str(type(item['2'])) == '<type \'tuple\'>':
		

			
			x,y = findNum(int(item['2'][1][:-1]))
			val1 = (sym_table[x]['value'][y])
			x,y = findNum(int(item['2'][2][:-1]))
			val2 = (sym_table[x]['value'][y])
			
			val3 = findInSystemTable(item['2'][0],str(int(val1))+'c',str(int(val2))+'c')
			
			x,y = findNum(val3)
			
		else:
			
			x,y = findNum(item['2'])


			
		
		sym_table[x]['value'][y] = num

		
	if item['1'] == '+' or item['1'] == '-' or item['1'] == '*' or item['1'] == '/' :
	

	
		if str(type(item['2'])) == '<type \'int\'>':
			x,y = findNum(item['2'])
			num1 = int(sym_table[x]['value'][y])
		elif str(type(item['2'])) == '<type \'float\'>':
			x,y = findNum(item['2'])
			num1 = float(sym_table[x]['value'][y])
			
			
		elif str(type(item['2'])) == '<type \'tuple\'>' and len(item['2']) == 3:
		
		
			x,y = findNum(int(item['2'][1][:-1]))
			val1 = (sym_table[x]['value'][y])
			x,y = findNum(int(item['2'][2][:-1]))
			val2 = (sym_table[x]['value'][y])
			
			val3 = findInSystemTable(item['2'][0],str(int(val1))+'c',str(int(val2))+'c')
			
			x,y = findNum(val3)	
			num1 = (sym_table[x]['value'][y])
			
			num1 = (num1)
			
			
		else:
			if item['2'][0] == 't':
				num1 = avail[int(item['2'][1:])]
			elif item['2'][-1] == 'c':
				num1 = (item['2'][:-1])
			else:
				
				x,y = findNum(int(item['2'][1][:-1]))

				val = (sym_table[x]['value'][y])
				val = findInSystemTable(item['2'][0],str(int(val))+'c',(0))
				x,y = findNum(val)
				num1 = (sym_table[x]['value'][y])
				
				

			
			
		if str(type(item['3'])) == '<type \'int\'>':
			x,y = findNum(item['3'])
			num2 = int(sym_table[x]['value'][y])
		elif str(type(item['3'])) == '<type \'float\'>':
			x,y = findNum(item['3'])
			num2 = float(sym_table[x]['value'][y])
		elif str(type(item['3'])) == '<type \'tuple\'>' and len(item['2']) == 3:
			x,y = findNum(int(item['3'][1][:-1]))
			val1 = (sym_table[x]['value'][y])
			x,y = findNum(int(item['3'][2][:-1]))
			val2 = (sym_table[x]['value'][y])
			
			val3 = findInSystemTable(item['3'][0],str(int(val1))+'c',str(int(val2))+'c')
			
			x,y = findNum(val3)	
			num2 = (sym_table[x]['value'][y])
		
		else:
			if item['3'][0] == 't':
				num2 = avail[int(item['3'][1:])]
			elif item['3'][-1] == 'c':
				num2 = (item['3'][:-1])
			else:

				x,y = findNum(int(item['3'][1][:-1]))
				val = (sym_table[x]['value'][y])
				val = findInSystemTable(item['3'][0],str(int(val))+'c',(0))
				x,y = findNum(val)
				num2 = (sym_table[x]['value'][y])
				


		num1 = str(num1)
		num2 = str(num2)
		num1 = int(num1) if num1.find('.') == -1 else float(num1)
		num2 = int(num2) if num2.find('.') == -1 else float(num2)
				
		
				
		avail[int(item['4'][1:])] = operator[item['1']]((num1),(num2))
		
		
	if item['1'] == '<' or item['1'] == '>' or item['1'] == '==' or item['1'] == '<=' or item['1'] == '>='or item['1'] == '<>':
		if str(type(item['2'])) == '<type \'int\'>':
			x,y = findNum(item['2'])
			num1 = int(sym_table[x]['value'][y])
		elif str(type(item['2'])) == '<type \'float\'>':
			x,y = findNum(item['2'])
			num1 = float(sym_table[x]['value'][y])
			
			
		elif str(type(item['2'])) == '<type \'tuple\'>' and len(item) == 3:
		
		
			x,y = findNum(int(item['2'][1][:-1]))
			val1 = (sym_table[x]['value'][y])
			x,y = findNum(int(item['2'][2][:-1]))
			val2 = (sym_table[x]['value'][y])
			
			val3 = findInSystemTable(item['2'][0],str(int(val1))+'c',str(int(val2))+'c')
			
			x,y = findNum(val3)	
			num1 = (sym_table[x]['value'][y])
			
			num1 = (num1)
			
		else:
			if item['2'][0] == 't':
				num1 = avail[int(item['2'][1:])]
			elif item['2'][-1] == 'c':
				num1 = (item['2'][:-1])
			else:
				
				x,y = findNum(int(item['2'][1][:-1]))

				val = (sym_table[x]['value'][y])
				val = findInSystemTable(item['2'][0],str(int(val))+'c',(0))
				x,y = findNum(val)
				num1 = (sym_table[x]['value'][y])
				
		
		if str(type(item['3'])) == '<type \'int\'>':
			x,y = findNum(item['3'])
			num2 = int(sym_table[x]['value'][y])
		elif str(type(item['3'])) == '<type \'float\'>':
			x,y = findNum(item['3'])
			num2 = float(sym_table[x]['value'][y])
		elif str(type(item['3'])) == '<type \'tuple\'>' and len(item) == 3:
			x,y = findNum(int(item['3'][1][:-1]))
			val1 = (sym_table[x]['value'][y])
			x,y = findNum(int(item['3'][2][:-1]))
			val2 = (sym_table[x]['value'][y])
			
			val3 = findInSystemTable(item['3'][0],str(int(val1))+'c',str(int(val2))+'c')
			
			x,y = findNum(val3)	
			num2 = (sym_table[x]['value'][y])
		
		else:
			if item['3'][0] == 't':
				num2 = avail[int(item['3'][1:])]
			elif item['3'][-1] == 'c':
				num2 = (item['3'][:-1])
			else:

				x,y = findNum(int(item['3'][1][:-1]))
				val = (sym_table[x]['value'][y])
				val = findInSystemTable(item['3'][0],str(int(val))+'c',(0))
				x,y = findNum(val)
				num2 = (sym_table[x]['value'][y])
		
		num1 = str(num1)
		num2 = str(num2)
		num1 = int(num1) if num1.find('.') == -1 else float(num1)
		num2 = int(num2) if num2.find('.') == -1 else float(num2)
		
		avail[int(item['4'][1:])] = 1 if operator[item['1']]((num1),(num2)) == True else 0
		
	
	if item['1'] == 'print':
		if str(type(item['3'])) == '<type \'int\'>' :
			x,y = findNum(item['3'])
			num1 = (sym_table[x]['value'][y])
			

			num1 = str(num1)
			num1 = int(num1) if num1.find('.') == -1 else float(num1)
			print((num1))
			
		elif str(type(item['3'])) != '<type \'int\'>' and str(type(item['3'])) != '<type \'tuple\'>' and str(type(item['3'])) != '<type \'unicode\'>':	

			x,y = findNum(int(item['3'][:-1]))
			val = (sym_table[x]['value'][y])
			x,y = findNum(val-1)
			num1 = (sym_table[x]['value'][y])
			

			num1 = str(num1)
			num1 = int(num1) if num1.find('.') == -1 else float(num1)
			print((num1))
		
		elif str(type(item['3'])) == '<type \'tuple\'>':
			
			x,y = findNum(int(item['3'][1][:-1]))
			val1 = (sym_table[x]['value'][y])
			x,y = findNum(int(item['3'][2][:-1]))
			val2 = (sym_table[x]['value'][y])
			
			val3 = findInSystemTable(item['3'][0],str(int(val1))+'c',str(int(val2))+'c')
			
			x,y = findNum(val3)	
			num1 = (sym_table[x]['value'][y])
			

			
			print((num1))
	
		else:
			print(item['3'][1:-1])
			
			
	if item['1'] == 'read':

		x,y = findNum(item['3'])
		(sym_table[x]['value'][y]) =  raw_input()
			
		
	
	if item['1'] == 'GoToF':
		
		if str(type(item['2'])) == '<type \'int\'>':
			x,y = findNum(item['2'])
			num = int(sym_table[x]['value'][y])
		else:	
			if item['2'][0] == 't':
				
				num = avail[int(item['2'][1:])]
			else:
				num = int(item['2'][:-1])
						
		if num == 0:
			cp = int(item['3'])
		else:
			cp += 1
	elif item['1'] == 'GoTo':
		cp = int(item['3'])
				
	else:
		cp += 1
	
	
	
printSymTable()
	
	
	

	
	
	
	
	
	
	
	
	
	

