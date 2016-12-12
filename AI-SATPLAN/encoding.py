import copy

from hebrand_base import hebrandBase
from hebrand_base import actionNames
from read_pddl_domain_file import info_from_file

def encodingHandler():
		initial_sat_set = createSatDict()
		#print('Initial sat_set is: ', initial_sat_set)
		all_actions, init_atoms, goal_state = info_from_file()
		initial_state_CNF = createInitialStateCnfSentence(initial_sat_set, init_atoms)
		print('Initial cnf is: ', initial_state_CNF)
		#print('Length of initial CNF is: ', len(initial_state_CNF))

#         her kommer en while løkke som kaller dpll og slikt

# def linear_encoder(horizon): #lager final sat_sentence for hver horizon, og returner til encoding_handler som kaller opp dpll() og slikt
#         #rekkefølgen ting må gjøres i for å lage sat_sentence, bruker mange av hjelpefunksjonene under
#         #har ikke tenkt gjennom hvilken rekkefølge som er helt riktig, men tar utgangspunkt i oppgaveteksten
#         goal_states = createGoalStateCnfSentence(goal_states, horizon)
#         actions = extendActions(sat_set, horizon)
#         fame_axioms = extendFrameAxioms(sat_set, horizon)
#         at_least_one_axioms = extendAtLeastOneAxioms(sat_set, horizon)

#         return sat_sentence

def createSatDict():
        #I had to use lists to change the names (since you can't iterate through a set)
        #In case we want the values in the dictionary to be integers instead of strings: dict_with_ints = dict((k,int(v)) for k,v in dict_with_strs.iteritems())

		action_names = actionNames()
		for i in range(0, len(action_names)):
				action_names[i] = action_names[i] + '0'
		hebrand_base_set = hebrandBase()
		hebrand_base_list = list(hebrand_base_set)
		for i in range (0, len(hebrand_base_list)):
				hebrand_base_list[i] = hebrand_base_list[i] + '0'
		hebrand_base_dict = dict.fromkeys(hebrand_base_list, 0)
		for i in range (0, len(action_names)):
				hebrand_base_dict[action_names[i]] = 0
		value = 1
		hebrand_base_dict_copy = {}
		for key, val in hebrand_base_dict.items():
				if key.startswith('-'):
						key1 = key
						key2 = key[1:]
						if key1 not in hebrand_base_dict_copy or key2 not in hebrand_base_dict_copy:
								hebrand_base_dict_copy[key2] = str(value)
								hebrand_base_dict_copy[key1] = '-' + str(value)
								value += 1 
				else:
						key1 = key
						key2 = '-' + key
						if key1 not in hebrand_base_dict_copy or key2 not in hebrand_base_dict_copy:
								hebrand_base_dict_copy[key1] = str(value)
								hebrand_base_dict_copy[key2] = '-' + str(value)
								value += 1 
		print('SAT_DICTIONARY: ', hebrand_base_dict_copy)
		return hebrand_base_dict_copy

def extendSatSet(horizon, old_sat_set):
		#utvid med ett timestep
		#return sat_set_dict
		h = horizon
		sat_dict = old_sat_set
		new_keys = []
		max_values_key = max(sat_dict, key = sat_dict.get)
		max_value = sat_dict[max_values_key]
		for key, val in sat_dict.items():
				new_key = key[:-1] + str(h)
				new_keys.append(new_key)
		for i in range(0,len(new_keys)):
				sat_dict[new_keys[i]] = max_value + (i + 1)
		return new_sat_dict



def createInitialStateCnfSentence(sat_set_dict, init_states):
		init_cnf = []
		single_object_clause = ['init']
		copy_sat_set_dict = copy.deepcopy(sat_set_dict)
		copy_init_states = copy.deepcopy(init_states)
		#print('Copy of sat_set_dict: ', copy_sat_set_dict)
		print('Init states: ', init_states)
		for atom in range(len(copy_init_states)):
				copy_init_states[atom] = copy_init_states[atom] + '0'
				for key, val in copy_sat_set_dict.items():
						print('Copy_init_states[atom]: ', copy_init_states[atom])				
						if key == copy_init_states[atom]:
								print('ATOM MATCH FOUND')
								single_object_clause = key
								print('Single_object_clause match is: ', single_object_clause)
								init_cnf.append(single_object_clause)
								print('Init_CNF after match append: ', init_cnf)
						else:
								#print('Atom match not found')
								single_object_clause = '-' + key
								#print('Single object clause is: ', single_object_clause)
								init_cnf.append(single_object_clause)
		print('Init_CNF: ', init_cnf)
		return init_cnf
		# def createGoalStateCnfSentence(goal_states, horizon):
#         Vil ha det på liste-form
#         return goal_states_list

# def extendActions(sat_set, horizon):

#         actions_cnf = satToCnf(actions_sat_sentence)
#         return actions_cnf

# def extendFrameAxioms(sat_set, horizon):

#         frame_axioms_cnf = satToCnf(frame_axioms_sat_sentence)
#         return frame_axioms_cnf

# def extendAtLeastOneAxioms(sat_set, horizon):

#         at_least_one_axioms_cnf = satToCnf(at_least_one_axioms_sat_sentence)
#         return at_least_one_axioms_cnf


#def satToCnf(sat_sentence): sat_sentence = [[action], [preconds], [effects]] der [action] er et tall, [preconds] og [effects] er på formen [1,2,8,..] (der komma tilsvarer "or")
#def actionSatToCnf():
def actionSatToCnf(sat_sentence):
        #sat_sentence = [['23'], ['2','15', '36'], ['-3', '2', '-36']]
        action = sat_sentence[0]
        negated_action = '-' + action[0]
        preconds = sat_sentence[1]
        effects = sat_sentence[2]
        cnf_expression = []
        for i in range(0, len(preconds)):
                disjunction = [negated_action, preconds[i]]
                cnf_expression.append(disjunction)
        for i in range(0, len(effects)):
                disjunction = [negated_action, effects[i]]
                cnf_expression.append(disjunction)
        print('CNF-expression: ',cnf_expression)
#         return cnf_expression #cnf-expression er en liste i liste  [[1,2,8],[-3,-4,-6]] der komma tilsvarer "and"


# #for løkke der i er tidssteget
# #dpll inni forløkken og sjekke for cnf setningen du har der og da.



#statene endres i DPLL?

#def createSATsentence():


# def ConvertToDIMACSsyntax():
# 		#SAT_sentence = createSATsentence()
# 		#list_SAT = SAT_sentence on list form [clause1, clause2, clause3] (der clause1 = a, b, c (der komma er OR))
# 		number_of_clauses = 4 # telle hvor mange '^' det er og plusse på 1?
# 		number_of_variables = 3 # 
# 		f = open('cnf.txt', 'w')
# 		f.write('p cnf' + ' '+ str(number_of_variables) + ' ' + str(number_of_clauses))
# 		values = #splitLine? mellom hver '^' også splitte den igjen ved V ? 
# 		f.write(value


#ConvertToDIMACSsyntax()
#extendSatSet(2, createSATDict())
#createSATDict()
#actionSatToCnf()
encodingHandler()
