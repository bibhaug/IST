import time

class SAT_sentence:
	def __init__(self):
		self.clauses = []

	def add_clause(self, clause):
		self.clauses.append(clause)

	def __repr__(self):
		return "SAT_sentence: %s" % (self.clauses)

class Clause:
	def __init__(self):
		self.clause = []

def readDimacsFile():
	f = open('DIMACS_test2.dat', 'r')
	line = f.readline()
	#current_clause = Clause()
	#clauses = SAT_sentence()
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
				#clauses.add_clause(current_clause)
				clauses.append(current_clause)
		line = f.readline()
	return clauses, nbvar, nbclauses