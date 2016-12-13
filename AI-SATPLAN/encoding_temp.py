import copy

from hebrand_base import hebrandBase
from hebrand_base import actionNames
from read_pddl_domain_file import info_from_file

def encodingHandler():
        initial_sat_set_atoms, initial_sat_set_numbers = createConversionDicts()
        #print('Initial sat_set is: ', initial_sat_set)
        all_actions, init_atoms, goal_state = info_from_file()
        initial_state_CNF = createInitialStateCnfSentence(initial_sat_set_atoms, init_atoms)
        print('Initial cnf is: ', initial_state_CNF)
        print('Length of initial CNF is: ', len(initial_state_CNF))

        goal_state_CNF = createGoalStateCnfSentence(goal_state, '0')
        print('Goal states: ', goal_state_CNF)

# def linear_encoder(horizon): #lager final sat_sentence for hver horizon, og returner til encoding_handler som kaller opp dpll() og slikt
#         #rekkefølgen ting må gjøres i for å lage sat_sentence, bruker mange av hjelpefunksjonene under
#         #har ikke tenkt gjennom hvilken rekkefølge som er helt riktig, men tar utgangspunkt i oppgaveteksten
#         goal_states = createGoalStateCnfSentence(goal_states, horizon)
#         actions = extendActions(sat_set, horizon)
#         fame_axioms = extendFrameAxioms(sat_set, horizon)
#         at_least_one_axioms = extendAtLeastOneAxioms(sat_set, horizon)

#         return sat_sentence


def createConversionDicts():
        #I had to use lists to change the names (since you can't iterate through a set)
        #In case we want the values in the dictionary to be integers instead of strings: dict_with_ints = dict((k,int(v)) for k,v in dict_with_strs.iteritems())
        #Atoms_to_numbers_dict
        action_names = actionNames()
        for i in range(0, len(action_names)):
                action_names[i] = action_names[i] + '0'
        hebrand_base_set = hebrandBase()
        print('Hebrand base is: ', hebrand_base_set)
        print('Length of Hebrand base: ', len(hebrand_base_set))
        hebrand_base_list = list(hebrand_base_set)
        for i in range (0, len(hebrand_base_list)):
                hebrand_base_list[i] = hebrand_base_list[i] + '0'
        hebrand_base_dict = dict.fromkeys(hebrand_base_list, 0)
        for i in range (0, len(action_names)):
                hebrand_base_dict[action_names[i]] = 0
        value = 1
        atoms_to_numbers_dict = {}
        numbers_to_atoms_dict = {}
        for key, val in hebrand_base_dict.items():
                val1 = str(value)
                val2 = '-' + str(value)
                if key.startswith('-'):
                        key1 = key
                        key2 = key[1:]
                        if key1 not in atoms_to_numbers_dict or key2 not in atoms_to_numbers_dict:
                                atoms_to_numbers_dict[key2] = val1
                                atoms_to_numbers_dict[key1] = val2
                                numbers_to_atoms_dict[val1] = key2
                                numbers_to_atoms_dict[val2] = key1
                                value += 1 
                else:
                        key1 = key
                        key2 = '-' + key
                        if key1 not in atoms_to_numbers_dict or key2 not in atoms_to_numbers_dict:
                                atoms_to_numbers_dict[key1] = val1
                                atoms_to_numbers_dict[key2] = val2
                                numbers_to_atoms_dict[val1] = key1
                                numbers_to_atoms_dict[val2] = key2

                                value += 1 
        #print('SAT_DICTIONARY: ', atoms_to_numbers_dict)
        #print('NUM_DiCTIONARY: ', numbers_to_atoms_dict)


        return atoms_to_numbers_dict, numbers_to_atoms_dict

def extendConversionDicts(horizon, old_atoms_to_num_dict, old_num_to_atoms_dict):
        #utvid med ett timestep
        #return sat_set_dict
        h = horizon
        atom_dict = old_atoms_to_num_dict
        num_dict = old_num_to_atoms_dict
        new_keys = []
        max_values_key = max(atom_dict, key = atom_dict.get)
        max_value = atom_dict[max_values_key]
        for key, val in atom_dict.items():
                new_key = key[:-1] + str(h)
                new_keys.append(new_key)
        for i in range(0,len(new_keys)):
                val1 = int(max_value) + (i + 1)
                val2 = -val1
                if new_keys[i].startswith('-'):
                        key1 = new_keys[i]
                        key2 = new_keys[i][1:]
                        if key1 not in atom_dict or key2 not in atom_dict:
                                atom_dict[key1] = str(val2)
                                atom_dict[key2] = str(val1)
                                num_dict[str(val1)] = key2
                                num_dict[str(val2)] = key1
                else:
                        key1 = key
                        key2 = '-' + key
                        if key1 not in atom_dict or key2 not in atom_dict:
                                atom_dict[key1] = str(val1)
                                atom_dict[key2] = str(val2)
                                num_dict[str(val1)] = key1
                                num_dict[str(val2)] = key2
        #print('This is Atom Dict: ', atom_dict)
        #print('This is Num Dict: ', num_dict)
        return atom_dict, num_dict

def createInitialStateCnfSentence(sat_set_dict, init_states):
        
        action_names = actionNames()
        for name in range(len(action_names)):
                action_names[name] = '-' + action_names[name] + '0'
        print('Updated action_names: ', action_names)
        print('SAT_SET_DICT')

        init_cnf = set()
        single_object_clause = ['init']
        copy_sat_set_dict = copy.deepcopy(sat_set_dict)
        copy_init_states = copy.deepcopy(init_states)
        #print('Copy of sat_set_dict: ', copy_sat_set_dict)
        #print('Init states: ', init_states)
        for atom in range(len(copy_init_states)):
                copy_init_states[atom] = copy_init_states[atom] + '0'
                for key, val in copy_sat_set_dict.items():
                        #print('Copy_init_states[atom]: ', copy_init_states[atom])                               
                        if key == copy_init_states[atom]:
                                #print('ATOM MATCH FOUND')
                                single_object_clause = key
                                #print('Single_object_clause match is: ', single_object_clause)
                                init_cnf.add(single_object_clause)
                                #print('Init_CNF after match append: ', init_cnf)
                        elif key[0] == '-':
                                if key not in action_names: 
                                        single_object_clause = key
                                        init_cnf.add(single_object_clause)
        #print('Init_CNF: ', init_cnf)
        return list(init_cnf) #DETTE ER ENKELTLISTE; MÅ VÆRE LISTE-I-LISTE???

def createGoalStateCnfSentence(goal_states, horizon):
        #Vil ha det på liste-form
        #goal_states_list = []
        current_goal_states = []
        for state in range(len(goal_states)):
                current_goal_states.append(goal_states[state] + horizon)
        return current_goal_states

# def extendActions(sat_set, horizon):

#         actions_cnf = satToCnf(actions_sat_sentence)
#         return actions_cnf

# def extendFrameAxioms(sat_set, horizon):

#         frame_axioms_cnf = satToCnf(frame_axioms_sat_sentence)
#         return frame_axioms_cnf

# def extendAtLeastOneAxioms(sat_set, horizon):

#         at_least_one_axioms_cnf = satToCnf(at_least_one_axioms_sat_sentence)
#         return at_least_one_axioms_cnf


#def satToCnf(sat_sentence): sat_sentence = [[action], [preconds], [effects]] der [action] er et tall, [preconds] og [effects] er på formen [1,2,8,..] (der komma tilsvarer "and")
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
#         return cnf_expression #cnf-expression er en liste i liste  [[1,2,8],[-3,-4,-6]] der komma tilsvarer "or"

# def frameAxiomSatToCnf(sat_sentence, current_atom_dict, current_num_dict):
#         #sat_sentence = [['23'], ['30']] (der 23 er et atom fra hebrand base og 30 er en action)
#         atom = sat_sentence[0]
#         atom_negated = '-' + atom[0]
#         action = sat_sentence[1]
#         action_negated = '-' + action[0]
#         atom_value_increased_time_step = atom[0]
#         for key, val in current_sat_dict:



#         cnf_expression = []



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
#atom_to_num, num_to_atom = createConversionDicts()
#extendConversionDicts(2, atom_to_num, num_to_atom)
#createConversionDicts()
#actionSatToCnf()
encodingHandler()