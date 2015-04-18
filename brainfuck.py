#!/usr/bin/python

import sys

def instr_next_cell(ptr):
	# >
	ptr += 1
	if ptr >= 30000:
		raise ValueError, "Pointer error! Out of bounds (> 30000)"
	return ptr

def instr_prev_cell(ptr):	
	# >
	ptr -= 1
	if ptr < 0:
		raise ValueError, "Pointer error! Out of bounds (< 0)"
	return ptr

def instr_value_plus(val):
	# +
	val += 1
	return val % 255

def instr_value_minus(val):
	# -
	val -= 1
	return val % 255
	
def instr_out(val):
	# .
	sys.stdout.write(chr(val))

def instr_in():
	# ,
	return ord(raw_input())

def get_loops(code):
	loops, stack = {}, []	

	for i, x in enumerate(code):
		if x == "[":
			stack.append(i)
		elif x == "]":
			if len(stack) == 0:
				raise ValueError, "Parenthesis error!"
			begin = stack.pop()
			loops[begin] = i
			loops[i] = begin

	if len(stack) != 0:
		raise ValueError, "Parenthesis error!"
	
	return loops
	
def evaluate(code):
	cells, loops, ptr = ([0] * 30000), get_loops(code), 0
	i = 0	

	while i < len(code):
		if code[i] == ">":
			ptr = instr_next_cell(ptr)

		elif code[i] == "<":
			ptr = instr_prev_cell(ptr)

		elif code[i] == "+":
			cells[ptr] = instr_value_plus(cells[ptr])
		
		elif code[i] == "-":
			cells[ptr] = instr_value_minus(cells[ptr])
		
		elif code[i] == ".":
			instr_out(cells[ptr])
		
		elif code[i] == ",":
			cells[ptr] = instr_in()

		elif code[i] == "[" and cells[ptr] == 0:
			i = loops[i]

		elif code[i] == "]" and cells[ptr] != 0:
			i = loops[i]
 
		i += 1

def read_from_file(relative_path):
	dat = open(relative_path, "r")
	try: 
		evaluate(dat.read())
	except ValueError as ve:
		print ve,
	dat.close()
	
def Main():
	if len(sys.argv) == 2:
		read_from_file(sys.argv[1])
		print
	else:
		print("Legal call is: ./brainfuck.py file.bf")

Main()

