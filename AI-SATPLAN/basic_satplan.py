import sys
import time

from encoding_temp import encodingHandler
from dpll_solver import dpllHandler

def main():
	if sys.argv[0] == 'basic_satplan.py':
		file_name = sys.argv[1]
		encodingHandler(file_name)
	elif sys.arvg[0] == 'dpll_solver.py':
		file_name = sys.argv[1]
		dpllHandler(file_name)
	else:
		print('Unrecognizable file name. Please write "basic_satplan.py"')


main()