import copy

from hebrand_base import hebrandBase
from hebrand_base import actionNames
from hebrand_base import allVariationsOfActionNames
from hebrand_base import setFileName
from read_pddl_domain_file import info_from_file

FILE_NAME = 'undefined'

def encodingHandler(file_name):
        global FILE_NAME
        FILE_NAME = file_name
        setFileName(FILE_NAME) #defines file_name in hebrand base

        atoms_to_numbers_dict, numbers_to_atoms_dict = createConversionDicts()
        hebrand_base = hebrandBase()
        action_schemas, init_state, goal_state = info_from_file(FILE_NAME)
        all_action_combinations = allVariationsOfActionNames(action_schemas)
        print('All action combinations: ', all_action_combinations)

        initial_state_CNF = createInitialStateCnfSentence(atoms_to_numbers_dict, init_state, all_action_combinations)
        goal_state_CNF = createGoalStateCnfSentence(atoms_to_numbers_dict, goal_state, '0')
        print('Initial state CNF is: ', initial_state_CNF)
        print('Goal states: ', goal_state_CNF)
        print('Length of initial CNF is: ', len(initial_state_CNF))

        at_most_one_axioms_CNF, at_least_one_axioms_CNF = extendOnlyOneActionAxioms(atoms_to_numbers_dict, all_action_combinations, '0')
        print('At-most-one axioms: ', at_most_one_axioms_CNF)
        print('At-least-one axioms: ', at_least_one_axioms_CNF)

        sat_sentence = []
        sat_sentence.extend(initial_state_CNF)
        sat_sentence.extend(goal_state_CNF)
        sat_sentence.extend(at_most_one_axioms_CNF)
        sat_sentence.extend(at_least_one_axioms_CNF)

        print('First sat-sentence is: ', sat_sentence)

        # horizon = 0
        # while no solution:
        #         goal_state_CNF = createGoalStateCnfSentence(goal_state, horizon)

        #functions under this line should eventually be part of while-loop in linear_encoder
       ## goal_state_CNF = createGoalStateCnfSentence(goal_state, 5)
        #print('Goal states: ', goal_state_CNF)
        #print('Atoms_to_numbers_dict: ', atoms_to_numbers_dict)

        #print('First element of all_action_combinations is: ', all_action_combinations[0])
        #print('Len of all_action_combinations is:', len(all_action_combinations))
        ##temp_extended_atoms_dict, temp_extended_numbers_dict = extendConversionDicts(1, atoms_to_numbers_dict, numbers_to_atoms_dict)
        #print('Extended dictionary: ', temp_extended_atoms_dict)
        #actions_CNF = extendActions(atoms_to_numbers_dict, all_action_combinations, 1)
        #print('Action CNF for ', all_action_combinations, ' with horizon=1 is: ', actions_CNF)

        ##frame_axioms_cnf = extendFrameAxioms(temp_extended_atoms_dict, hebrand_base, all_action_combinations, 1)
        #print('Frame axioms: ', frame_axioms_cnf)

# def linear_encoder(horizon): #lager final sat_sentence for hver horizon, og returner til encoding_handler som kaller opp dpll() og slikt
#         #rekkefølgen ting må gjøres i for å lage sat_sentence, bruker mange av hjelpefunksjonene under
#         #har ikke tenkt gjennom hvilken rekkefølge som er helt riktig, men tar utgangspunkt i oppgaveteksten
#         goal_states = createGoalStateCnfSentence(goal_states, horizon)
#         actions = extendActions(sat_set, horizon)
#         fame_axioms = extendFrameAxioms(sat_set, horizon)
#         at_least_one_axioms = extendAtLeastOneAxioms(sat_set, horizon)

#         return sat_sentence


def createConversionDicts():
        action_schemas, init_state, goal_state = info_from_file(FILE_NAME)
        actions = allVariationsOfActionNames(action_schemas)
        print('List of action schemas is: ', actions)
        action_names = []
        for action in range(len(actions)):
                action_names.append(actions[action].name + '0')

        hebrand_base_set = hebrandBase()
        hebrand_base_list = list(hebrand_base_set)
        for i in range (0, len(hebrand_base_list)):
                hebrand_base_list[i] = hebrand_base_list[i] + '0'
        hebrand_base_dict = dict.fromkeys(hebrand_base_list, 0)
        for i in range (0, len(action_names)):
                hebrand_base_dict[action_names[i]] = 0
        value = 1
        #print('This is Hebrand_Base_Dict: ', hebrand_base_dict)
        #print('This is the length of hebrand_base_dict:', len(hebrand_base_dict))
        atoms_to_numbers_dict = {}
        numbers_to_atoms_dict = {}
        for key, val in hebrand_base_dict.items():
                val1 = str(value)
                val2 = '-' + str(value)
                if key.startswith('-'):
                        key1 = key
                        key2 = key[1:]
                        if ((key1 not in atoms_to_numbers_dict) or (key2 not in atoms_to_numbers_dict)):
                                atoms_to_numbers_dict[key2] = val1
                                atoms_to_numbers_dict[key1] = val2
                                numbers_to_atoms_dict[val1] = key2
                                numbers_to_atoms_dict[val2] = key1
                                value += 1 
                else:
                        key1 = key
                        key2 = '-' + key
                        if ((key1 not in atoms_to_numbers_dict) or (key2 not in atoms_to_numbers_dict)):
                                atoms_to_numbers_dict[key1] = val1
                                atoms_to_numbers_dict[key2] = val2
                                numbers_to_atoms_dict[val1] = key1
                                numbers_to_atoms_dict[val2] = key2
                                value += 1 
        #print('SAT_DICTIONARY: ', atoms_to_numbers_dict)
        #print('LENGTH OF ATOMS_TO_NUMBERS_DICT: ', len(atoms_to_numbers_dict))
        #print('NUM_DiCTIONARY: ', numbers_to_atoms_dict)


        return atoms_to_numbers_dict, numbers_to_atoms_dict

def extendConversionDicts(horizon, old_atoms_to_num_dict, old_num_to_atoms_dict):
        #extend with one time-step
        #return atoms_to_numbers and numbers_to_atoms - dicts
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

def createInitialStateCnfSentence(sat_set_dict, init_states, all_action_combinations):
        
        action_names = []

        for action in range(len(all_action_combinations)):
                action_names.append('-' + all_action_combinations[action].name + '0')
        #print('Updated action_names: ', action_names)

        init_cnf = set()
        single_object_clause = ['init']
        copy_sat_set_dict = copy.deepcopy(sat_set_dict)
        copy_init_states = copy.deepcopy(init_states)
        #print('Copy of sat_set_dict: ', copy_sat_set_dict)
        #print('Init states: ', init_states)
        for atom in range(len(copy_init_states)):
                copy_init_states[atom] = copy_init_states[atom] + '0'
        for atom in range(len(copy_init_states)):
                for key, val in copy_sat_set_dict.items():
                        #print('Copy_init_states[atom]: ', copy_init_states[atom])
                        if key in copy_init_states:
                                #print('ATOM MATCH FOUND')
                                single_object_clause = key
                                #print('Single_object_clause match is: ', single_object_clause)
                                init_cnf.add(single_object_clause)
                                #print('Init_CNF after match append: ', init_cnf)
                        elif key[0] == '-':
                                stripped_key = key.strip('-')
                                #print('Key is: ', key)
                                #print('Stripped key is ', stripped_key)                                
                                if key not in action_names:
                                        if stripped_key not in copy_init_states:
                                                #print(stripped_key, ' is not in ', copy_init_states, '\n')
                                                single_object_clause = key
                                                init_cnf.add(single_object_clause)
        clauses = []
        init_cnf_list = []
        #print('Init cnf set: ', init_cnf)
        while init_cnf:
                clause = init_cnf.pop()
                init_cnf_list.append(clause)
        for atom in range(len(init_cnf_list)):
                clauses.append([atomToNumber(sat_set_dict, init_cnf_list[atom])])
                #print('Single clause: ', clauses)

        #print('Clauses: ', clauses)
        return clauses

def createGoalStateCnfSentence(atoms_to_numbers_dict, goal_states, horizon):
        current_goal_states = []
        clauses = []
        for state in range(len(goal_states)):
                clauses.clear()
                #print('Goal state: ', goal_states[state] + str(horizon))
                clauses.append([atomToNumber(atoms_to_numbers_dict, (goal_states[state] + str(horizon)))])
                #current_goal_states.append(goal_states[state] + str(horizon))
                current_goal_states.extend(clauses)
        #print('Clauses goals: ', clauses)
        return current_goal_states #DETTE ER EN ENKELTLISTE; MÅ VÆRE LISTE-I-LISTE???

# def extendActions(atoms_to_numbers_dict, all_action_combinations, horizon): #to be run when horizon is >= 1
#         previous_time_step = str(horizon-1)
#         current_time_step = str(horizon)

#         action_var_number = []
#         preconds_in_numbers = []
#         effects_in_numbers = []

#         propostional_logic_statement = []
#         actions_cnf = []

#         for action in range(len(all_action_combinations)):
#                 action_var_number.clear()
#                 preconds_in_numbers.clear()
#                 effects_in_numbers.clear()
#                 propostional_logic_statement.clear()

#                 current_action = all_action_combinations[action]
#                 #print('Current action: ', current_action)
#                 action_var_number.append(atomToNumber(atoms_to_numbers_dict, (current_action.name + previous_time_step)))
#                 for precond in range(len(current_action.preconds)):
#                         current_precond = current_action.preconds[precond] + previous_time_step
#                         preconds_in_numbers.append(atomToNumber(atoms_to_numbers_dict, current_precond))
#                 for effect in range(len(current_action.effects)):
#                         current_effect = current_action.effects[effect] + current_time_step
#                         effects_in_numbers.append(atomToNumber(atoms_to_numbers_dict, current_effect))

#                 propostional_logic_statement.append(action_var_number)
#                 propostional_logic_statement.append(preconds_in_numbers)
#                 propostional_logic_statement.append(effects_in_numbers)

#                 actions_cnf.append(actionStatementToCnf(propostional_logic_statement))
#                 #print('Current actions_cnf: ', actions_cnf)
#         return actions_cnf #Liste-i-liste

def extendFrameAxioms(atoms_to_numbers_dict, hebrand_base_set, all_action_combinations, horizon): #to be run when horizon is >= 1
        previous_time_step = str(horizon-1)
        current_time_step = str(horizon)

        propostional_logic_statement = []
        frame_axioms_cnf = []

        for action in range(len(all_action_combinations)):
                ground_action = all_action_combinations[action].name + previous_time_step
                for atom in hebrand_base_set:
                        propostional_logic_statement.clear()
                        if atom not in all_action_combinations[action].effects:
                                print(atom, ' not in ', all_action_combinations[action].effects)
                                current_atom = atom + current_time_step
                                previous_atom = atom + previous_time_step
                                propostional_logic_statement.append(atomToNumber(atoms_to_numbers_dict, previous_atom)) 
                                propostional_logic_statement.append(atomToNumber(atoms_to_numbers_dict, ground_action))
                                propostional_logic_statement.append(atomToNumber(atoms_to_numbers_dict, current_atom))
                                frame_axioms_cnf.append(frameAxiomStatementToCnf(propostional_logic_statement))

        return frame_axioms_cnf #DATASTRUKTUR PÅ DENNE?
        #return 0

def extendOnlyOneActionAxioms(atoms_to_numbers_dict, all_action_combinations, horizon):
        #needs to make clauses of -(actionY AND actionX). Number of clauses = all_action_combinations * all_action_combinations
        #also clauses of (x OR y OR... OR last_action_combo)
        timestep = str(horizon)
        at_least_one_axioms_cnf = [] #list containing one clause on CNF-form

        at_most_one_axiom = []
        at_most_one_axioms_cnf = []


        for actionX in range(len(all_action_combinations)):
                actionX_name = all_action_combinations[actionX].name
                at_least_one_axioms_cnf.append([atomToNumber(atoms_to_numbers_dict, (actionX_name + timestep))])
                for actionY in range(len(all_action_combinations)):
                        actionY_name = all_action_combinations[actionY].name
                        at_most_one_axiom.clear()
                        if actionY_name != actionX_name:
                                #-(x and y) clause
                                at_most_one_axiom.append(atomToNumber(atoms_to_numbers_dict, (actionX_name + timestep)))
                                at_most_one_axiom.append(atomToNumber(atoms_to_numbers_dict, (actionY_name + timestep)))
                                at_most_one_axioms_cnf.append(onlyOneActionAxiomToCnf(at_most_one_axiom))

        return at_most_one_axioms_cnf, at_least_one_axioms_cnf #liste-i-liste

def onlyOneActionAxiomToCnf(prop_logic_sentence):
        #kommer på formen [2,3]
        #betyr -(2 AND 3)
        not_first_argument = '-' + prop_logic_sentence[0]
        not_second_argument = '-' + prop_logic_sentence[1]
        cnf_clause = [not_first_argument, not_second_argument]
        return cnf_clause #single liste

        #return CNF uttrykk (liste-i-liste)


#def satToCnf(sat_sentence): sat_sentence = [[action], [preconds], [effects]] der [action] er et tall, [preconds] og [effects] er på formen [1,2,8,..] (der komma tilsvarer "and")
#def actionSatToCnf():
def actionStatementToCnf(prop_logic_sentence):
        #prop_logic_sentence = [['23'], ['2','15', '36'], ['-3', '2', '-36']]
        action = prop_logic_sentence[0]
        negated_action = '-' + action[0]
        preconds = prop_logic_sentence[1]
        effects = prop_logic_sentence[2]
        cnf_expression = []
        for i in range(0, len(preconds)):
                disjunction = [negated_action, preconds[i]]
                cnf_expression.append(disjunction)
        for i in range(0, len(effects)):
                disjunction = [negated_action, effects[i]]
                cnf_expression.append(disjunction)
        #print('CNF-expression: ',cnf_expression)
        return cnf_expression
#         return cnf_expression #cnf-expression er en liste i liste  [[1,2,8],[-3,-4,-6]] der komma tilsvarer "or"

def frameAxiomStatementToCnf(prop_logic_sentence):
        # ##prop_logic_sentence = [['23'], ['30']] (der 23 er et atom fra hebrand base og 30 er en action)
        # atom = prop_logic_sentence[0]
        # atom_negated = '-' + atom[0]
        # action = prop_logic_sentence[1]
        # action_negated = '-' + action[0]
        # name_of_atom = current_num_dict[atom[0]]
        # new_end_of_name = str(int(name_of_atom[-1]) + 1) 
        # name_of_atom_updated_timestep = name_of_atom[:-1] + new_end_of_name
        # ##!! ERROR: kan vi anta at atomet med oppdatert timestep ligger i current atom dict?? 
        # value_of_atom_updated_timestep = current_atom_dict[name_of_atom_updated_timestep]
        # cnf_expression = [atom_negated, action_negated, value_of_atom_updated_timestep] #Komma betyr "or" her
        # ##print('CNF-expression: ', cnf_expression)
        # return cnf_expression
        atom = prop_logic_sentence[0]
        atom_negated = '-' + atom[0]

        action = prop_logic_sentence[1]
        action_negated = '-' + action[0]

        #BLIR DENNE RETURNEN RIKTIG MTP HVORDAN CNF'N SKAL VÆRE??
        cnf_clause = [atom_negated, action_negated, prop_logic_sentence[2]] #Komma betyr "or" her
        print('Frame Axiom CNF-expression: ', cnf_clause)
        return cnf_clause


def atomToNumber(atom_to_number_dict, atom_name):
        number = atom_to_number_dict[atom_name]
        return number


#statene endres i DPLL?

#def createSATsentence():


# def ConvertToDIMACSsyntax():
#               #SAT_sentence = createSATsentence()
#               #list_SAT = SAT_sentence on list form [clause1, clause2, clause3] (der clause1 = a, b, c (der komma er OR))
#               number_of_clauses = 4 # telle hvor mange '^' det er og plusse på 1?
#               number_of_variables = 3 # 
#               f = open('cnf.txt', 'w')
#               f.write('p cnf' + ' '+ str(number_of_variables) + ' ' + str(number_of_clauses))
#               values = #splitLine? mellom hver '^' også splitte den igjen ved V ? 
#               f.write(value


#ConvertToDIMACSsyntax()

# sat_sentence = [['23'], ['30']]
# atom_to_num, num_to_atom = createConversionDicts()
# dict_atom, dict_num = extendConversionDicts(1, atom_to_num, num_to_atom)
# frameAxiomSatToCnf(sat_sentence, dict_atom, dict_num)

#extendConversionDicts(2, atom_to_num, num_to_atom)



#createConversionDicts()
#actionSatToCnf()
#encodingHandler()