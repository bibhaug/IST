import time
import copy

from dimacs_to_dpll import readDimacsFile

def dpllHandler(): 
	clauses, nbvar, nbclauses = readDimacsFile()
	print(clauses)

	satisfiable = dpllAlgorithm(clauses)
	print('\nSatisfiability: ', satisfiable)

def dpllAlgorithm(clauses):
	print('\n\nEntered new instance of dpllAlgorithm')
	print('Current SAT-sentence is: ', clauses)
	if containsNoClauses(clauses):
		return True

	elif containsEmptyClause(clauses):
		print('EMPTY CLAUSE FOUND -------------------------------------------------------')
		print('Returning False because of empty clause')
		return False

	#"""
	#contains_pure_literal, pure_literal = containsPureLiteral(clauses, nbvar) #Need to re-add nbvar to dpllAlgorithm(clauses, nbvar) before this can be used
	#elif contains_pure_literal:
	#	literal = pure_literal
	#	return dpllAlgorithm(simplify(clauses, literal))
	#"""
	contains_unit_clause, unit_clause_literal = containsUnitClause(clauses)
	if contains_unit_clause:
		literal = unit_clause_literal
		print('Unit_clause literal to simplify is: ', literal)
		return dpllAlgorithm(simplify(clauses, literal))

	else:
		literal = selectRandomLiteral(clauses)
		print('Literal to simplify is: ', literal)
		if dpllAlgorithm(simplify(clauses, literal)):
			print('Returning True')
			return True
		else:
			print('Entered else-statement, trying with negated literal on CNF-sentence: ', clauses)
			returning = dpllAlgorithm(simplify(clauses, negateLiteral(literal)))
			print('Returning: ', returning, ' from within else-statement')
			return returning
	print('ERROR: Reached the end without returning anything.')

def containsNoClauses(clauses):
	if len(clauses) == 0:			#could also use 'if not clauses', but prefer len(x)==0 because it's more explicit, in that clauses is a list and not a boolean variable
		return True
	else:
		return False

def containsEmptyClause(clauses):
	for i in range(len(clauses)):
		if (len(clauses[i]) == 1):	#len(x) == 1 means there's only a 0 left in the clause, aka. it's 
			return True
	return False

"""
#for-løkkene under må sjekkes hvis implementasjonen skal virke (clauses[clause])
def containsPureLiteral(clauses, nbvar):	#literal that only occurs with one polarity
	#need to check all literals (naturally stop checking if we find a pure literal)
	#need to keep track of which literals we already checked
	checked_literals = []
	current_literal = 'initialize'
	polarity = 'initialize'
	for literal_number_i in range(1, nbvar+1):
		current_literal = literal_number_i
		for clause in range(0, len(clauses)):
			for literal in range(0, len(clause)):
				if literal == current_literal

	return True/False and literal
"""

def containsUnitClause(clauses):
	for i in range(len(clauses)):
		if (len(clauses[i])) == 2:
			print('UNIT Clause found. The unit clause is: ', clauses[i][0])
			return True, clauses[i][0]
	return False, 'foobar'

def selectRandomLiteral(clauses):
	return clauses[0][0]

def simplify(clauses, literal):
	clauses1 = removeClausesContainingLiteral(clauses, literal)
	clauses2 = removeNegatedLiteralFromClauses(clauses1, negateLiteral(literal))
	return clauses2

def removeClausesContainingLiteral(clauses, literal):
	indexes_to_remove = []
	for clause in range(len(clauses)):
		#print('Going through for-loop for the ', clause, ' time.')
		if clauseContainsLiteral(clauses[clause], literal):
			#print('Clause #', clause, ' contains literal ', literal)
			#removed_clause = clauses.pop(clause)	#can this mess with the for-loop and the len(clauses) statement??? #changed from list.remove(x) to list.pop(index)
			indexes_to_remove.append(clause)
	print('Indexes to remove: ', indexes_to_remove)

	index_correction_counter = 0
	copy_of_clauses = copy.deepcopy(clauses)
	for i in range(len(indexes_to_remove)):
		removed_clause = copy_of_clauses.pop(indexes_to_remove[i]-index_correction_counter)
		index_correction_counter+=1
	print('CNF-sentence after clause-removal: ', copy_of_clauses)
	return copy_of_clauses


def removeNegatedLiteralFromClauses(clauses, negated_literal):
	copy_of_clauses = copy.deepcopy(clauses)
	for clause in range(len(copy_of_clauses)):
		if clauseContainsLiteral(copy_of_clauses[clause], negated_literal):
			print('Removing negated_literal in clause #', clause)
			copy_of_clauses[clause].remove(negated_literal)	#here list.remove(x) is correct since we want to remove one specific object, not an entire list
	print('CNF-sentence after negated_literal-removal: ', copy_of_clauses)
	return copy_of_clauses

def negateLiteral(literal):
	print('Original literal was ', literal)
	if literal[0] == '-':
		negated_literal = literal.lstrip('-')
	#if literal[0] == '-':
	#	print('Negated literal is ', literal[1])
	#	return literal[1]
	else:
		negated_literal = '-' + literal
	print('Negated literal is ', negated_literal)
	return negated_literal

def clauseContainsLiteral(clause, literal):
	for l in range(len(clause)):
		if clause[l]==literal:
			return True
	return False

"""
function dpll (F : Formula) : (SAT, UNSAT)
begin
	if F is empty then
		return SAT
	else if there is an empty clause in F then
		return UNSAT
	else if there is a pure literal l in F then
		return dpll(F[l → ⊤])
	else there is a unit clause [l] in F then
		return dpll(F[l → ⊤])
	else begin
		select a literal l occurring in F
		if dpll(F[l → ⊤]) = SAT then
			 return SAT
		else
			return dpll(F[l → ⊥])
	end
end

simplify("@, literal")
	remove clauses in @ where literal is positive
	remove -literal from clauses where it appears
	return new alpha
"""
dpllHandler()