import time
#Reads DIMACS-file and put the data into a list of lists

def readDimacsFile(file_name): #file_name must be on the form dimacs_files/*filename*.dat
	f = open(file_name, 'r')
	line = f.readline()
	current_clause = []
	clauses = []

	while line:
		if line != '\n':
			splitLine = line.split()
			if line.startswith('p'):
				nbvar = splitLine[2]
				nbclauses = splitLine[3]
			elif not line.startswith('c'):
				current_clause = splitLine
				clauses.append(current_clause)
		line = f.readline()
	return clauses, nbvar, nbclauses
