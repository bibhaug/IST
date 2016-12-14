import sys
import time

from encoding import encodingHandler
from dpll_solver import dpllHandler

def main():
	if sys.argv[0] == 'basic_satplan.py':
		file_name = sys.argv[1]
		encodingHandler(file_name)
	else:
		print('Unrecognizable file name. Please write "basic_satplan.py"')


main()