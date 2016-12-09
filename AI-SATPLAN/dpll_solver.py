import time
import copy

from dimacs_to_dpll import readDimacsFile

NBVAR = 'undefined'

def dpllHandler(): 
	clauses, nbvar, nbclauses = readDimacsFile()
	print(clauses)
	global NBVAR
	NBVAR = nbvar
	print('NBVAR = ', NBVAR)
	validated_literals = []
	previous_literal = 'initialize'

	satisfiability, polarity_of_literals = dpllAlgorithm(clauses, validated_literals, previous_literal)
	print('jrslufhrikh')
	duplicate_literal = polarity_of_literals.pop(0)	#the first polarity to be assigned gets assigned twice, so just removing a duplicate listing (treating symptom rather than cause :P)
	print('\nSatisfiability: ', satisfiability)
	print('Polarity of literals: ', polarity_of_literals)
	print('# of literals with assigned values: ', len(polarity_of_literals))

	#return satisfiability, polarity_of_literals

def dpllAlgorithm(clauses, validated_literals, previous_literal):
	print('\n\nEntered new instance of dpllAlgorithm')
	print('Current SAT-sentence is: ', clauses)
	checkIfClausesAreValid(clauses)	#Can be removed? Needed when we had a problem with unvalid literals (literals out of range)
	if containsNoClauses(clauses):
		validated_literals.append(previous_literal)
		return True, validated_literals

	elif containsEmptyClause(clauses):
		print('EMPTY CLAUSE FOUND -------------------------------------------------------')
		print('Returning False because of empty clause')
		return False, validated_literals

	#contains_pure_literal, pure_literal = containsPureLiteral(clauses)
	#if contains_pure_literal:
	#	literal = pure_literal
	#	print('Pure_literal to simplify is: ', literal)
	#	satisfiable, temp_validated_literals_list = dpllAlgorithm(simplify(clauses, literal), validated_literals, literal)
	#	if satisfiable:
	#		temp_validated_literals_list.append(literal)
	#		print('Returning True from pure_literal')
	#		return True, temp_validated_literals_list
	#	else:
	#		return False, temp_validated_literals_list

	contains_unit_clause, unit_clause_literal = containsUnitClause(clauses)
	if contains_unit_clause:
		literal = unit_clause_literal
		print('Unit_clause literal to simplify is: ', literal)
		satisfiable, temp_validated_literals_list = dpllAlgorithm(simplify(clauses, literal), validated_literals, literal)
		if satisfiable:
			temp_validated_literals_list.append(literal)
			print('Returning True from unit_clause')
			return True, temp_validated_literals_list
		else:
			return False, temp_validated_literals_list

	else:
		literal = selectRandomLiteral(clauses)
		print('Literal to simplify is: ', literal)
		satisfiability, temp_validated_literals_list = dpllAlgorithm(simplify(clauses, literal), validated_literals, literal)
		if satisfiability == True:
			temp_validated_literals_list.append(literal)
			print('Returning True')
			return True, temp_validated_literals_list
		else:
			print('Entered else-statement, trying with negated literal on CNF-sentence: ', clauses)
			negated_literal = negateLiteral(literal)
			satisfiability, temp_validated_literals_list = dpllAlgorithm(simplify(clauses, negated_literal), validated_literals, negated_literal)
			print('Returning: ', satisfiability, ' from within else-statement')
			if satisfiability == True:
				temp_validated_literals_list.append(negated_literal)
				return True, temp_validated_literals_list
			else:
				return False, temp_validated_literals_list
	print('ERROR: Reached the end without returning anything.')

def checkIfClausesAreValid(clauses):
	for clause in range(len(clauses)):
		for literal in range(len(clauses[clause])):
			if int(clauses[clause][literal]) > int(NBVAR):
				print('Invalid literal is: ', clauses[clause][literal])
				raise Exception('Clauses contains invalid literals (literals out of range). Range: 0 - ', NBVAR)

def containsNoClauses(clauses):
	if len(clauses) == 0:			#could also use 'if not clauses', but prefer len(x)==0 because it's more explicit, in that clauses is a list and not a boolean variable
		return True
	else:
		return False

def containsEmptyClause(clauses):
	for i in range(len(clauses)):
		if (len(clauses[i]) == 1):	#len(x) == 1 means there's only a 0 left in the clause, aka. it's empty 
			return True
	return False

CHECKED_LITERALS = []

def containsPureLiteral(clauses):	#literal that only occurs with one polarity
	#need to check all literals (naturally stop checking if we find a pure literal)
	#need to keep track of which literals we already checked. 
	if len(CHECKED_LITERALS) == int(NBVAR):	#If all literals have been checked, there's no point in continue checking
		return False, 'nopureliteral'

	for literal_to_check in range(1, (int(NBVAR)+1)):
		if literalNotCheckedBefore(literal_to_check):
			CHECKED_LITERALS.append(literal_to_check)
			negated_literal_to_check = negateLiteral(str(literal_to_check))
			if literalExistsInClauses(clauses, literal_to_check):
				for clause in range(len(clauses)):
					for literal in range(len(clauses[clause])):
						if clauses[clause][literal] == negated_literal_to_check:
							return False, 'nopureliteral'
				return True, literal_to_check
			elif literalExistsInClauses(clauses, negated_literal_to_check):
				for clause in range(len(clauses)):
					for literal in range(len(clauses[clause])):
						if clauses[clause][literal] == literal_to_check:
							return False, 'nopureliteral'
				return True, negated_literal_to_check

	return False, 'nopureliteral'

def literalExistsInClauses(clauses, literal):
	for clause in range(len(clauses)):
		for i in range(len(clauses[clause])):
			if clauses[clause][i] == literal:
				return True
	return False

def literalNotCheckedBefore(literal):
	if literal in CHECKED_LITERALS: #Er dette en gyldig command???
		return False
	else:
		return True

def containsUnitClause(clauses):
	for i in range(len(clauses)):
		if (len(clauses[i])) == 2:
			print('UNIT Clause found. The unit clause is: ', clauses[i][0])
			return True, clauses[i][0]
	return False, 'foobar'

def selectRandomLiteral(clauses):
	return clauses[0][0]	#the randomness of this function can be heavily critized

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
			copy_of_clauses[clause].remove(negated_literal)
	print('CNF-sentence after negated_literal-removal: ', copy_of_clauses)
	return copy_of_clauses

def negateLiteral(literal):
	print('Original literal was ', literal)
	if literal[0] == '-':
		negated_literal = literal.lstrip('-')
	else:
		negated_literal = '-' + literal
	print('Negated literal is ', negated_literal)
	return negated_literal

def clauseContainsLiteral(clause, literal):
	for l in range(len(clause)):
		if clause[l]==literal:
			return True
	return False

dpllHandler()