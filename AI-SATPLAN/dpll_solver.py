import time

from dimacs_to_dpll import read_DIMACS_file

def main():
	clauses, nbvar, nbclauses = read_DIMACS_file()
	print(clauses)
	time.sleep(2)

main()