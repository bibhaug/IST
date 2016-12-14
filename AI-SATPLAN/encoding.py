import copy

from hebrand_base import hebrandBase
from hebrand_base import actionNames
from hebrand_base import allVariationsOfActionNames
from hebrand_base import setFileName
from read_pddl_domain_file import info_from_file
from dpll_solver import dpllHandler
from dpll_solver import dpllHandlerWithoutReadingDimacs

FILE_NAME = 'undefined'

def encodingHandler(file_name):
        global FILE_NAME
        FILE_NAME = file_name
        setFileName(FILE_NAME) #defines file_name in hebrand base

        atoms_to_numbers_dict, numbers_to_atoms_dict = createConversionDicts() #conversion dicts storing the relationship between atom and the assigned number (and vice-versa)
        hebrand_base = hebrandBase()
        action_schemas, init_state, goal_state = info_from_file(FILE_NAME)
        all_action_combinations = allVariationsOfActionNames(action_schemas)
        print('All action combinations: ', all_action_combinations)

        #The following code creates the SAT-sentence for horizon = 0 ---------------------------------------------------------------------------
        initial_state_CNF = createInitialStateCnfSentence(atoms_to_numbers_dict, init_state, all_action_combinations)
        goal_state_CNF = createGoalStateCnfSentence(atoms_to_numbers_dict, goal_state, '0')
        print('Initial state CNF is: ', initial_state_CNF)
        print('Goal states: ', goal_state_CNF)
        print('Length of initial CNF is: ', len(initial_state_CNF))

        at_most_one_axioms_CNF, at_least_one_axioms_CNF = extendOnlyOneActionAxioms(atoms_to_numbers_dict, all_action_combinations, '0')
        #print('At-most-one axioms: ', at_most_one_axioms_CNF)
        #print('At-least-one axioms: ', at_least_one_axioms_CNF)

        sat_sentence = []
        sat_sentence.extend(initial_state_CNF)
        sat_sentence.extend(goal_state_CNF)
        sat_sentence.extend(at_most_one_axioms_CNF)
        sat_sentence.extend(at_least_one_axioms_CNF)

        print('First sat-sentence is: ', sat_sentence)
        nbvar = (len(atoms_to_numbers_dict))/2
        nbclauses = len(sat_sentence)

        
        satisfiability, polarity_of_literals = dpllHandlerWithoutReadingDimacs(sat_sentence, nbvar, nbclauses)

        #this is where the SATPLAN idea comes into play by expanding the horizon with 1 until a solution is found
        horizon = 1
        while not satisfiability:
                temp_extended_atoms_dict, temp_extended_numbers_dict = extendConversionDicts(horizon, atoms_to_numbers_dict, numbers_to_atoms_dict)
                goal_state_CNF = createGoalStateCnfSentence(temp_extended_atoms_dict, goal_state, horizon)
                actions_CNF = extendActions(temp_extended_atoms_dict, all_action_combinations, horizon)
                at_most_one_axioms_CNF, at_least_one_axioms_CNF = extendOnlyOneActionAxioms(temp_extended_atoms_dict, all_action_combinations, horizon)

                sat_sentence.extend(goal_state_CNF) #this is wrong, we need to remove the old goal_states first
                sat_sentence.extend(at_most_one_axioms_CNF)
                sat_sentence.extend(at_least_one_axioms_CNF)
                sat_sentence.extend(actions_CNF)
               
                nbvar = (len(temp_extended_atoms_dict)/2)
                nbclauses = len(sat_sentence)
                
                satisfiability, polarity_of_literals = dpllHandlerWithoutReadingDimacs(sat_sentence, nbvar, nbclauses)

                horizon += 1

        print('A solution was found after ', horizon-1, ' steps!!')

# def linear_encoder(horizon): #lager final sat_sentence for hver horizon, og returner til encoding_handler som kaller opp dpll() og slikt
#         #rekkefølgen ting må gjøres i for å lage sat_sentence, bruker mange av hjelpefunksjonene under
#         #har ikke tenkt gjennom hvilken rekkefølge som er helt riktig, men tar utgangspunkt i oppgaveteksten
#         goal_states = createGoalStateCnfSentence(goal_states, horizon)
#         actions = extendActions(sat_set, horizon)
#         fame_axioms = extendFrameAxioms(sat_set, horizon)
#         at_least_one_axioms = extendAtLeastOneAxioms(sat_set, horizon)

#         return sat_sentence


def createConversionDicts(): ##conversion dicts storing the relationship between atom and the assigned number (and vice-versa)
        action_schemas, init_state, goal_state = info_from_file(FILE_NAME)
        actions = allVariationsOfActionNames(action_schemas)
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

def extendConversionDicts(horizon, old_atoms_to_num_dict, old_num_to_atoms_dict): #extends the conversion dicts with the new atoms/numbers for the added time-step
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
        for atom in range(len(copy_init_states)):
                copy_init_states[atom] = copy_init_states[atom] + '0'
        for atom in range(len(copy_init_states)):
                for key, val in copy_sat_set_dict.items():
                        if key in copy_init_states:
                                #print('ATOM MATCH FOUND')
                                single_object_clause = key
                                init_cnf.add(single_object_clause)
                        elif key[0] == '-':
                                stripped_key = key.strip('-')                                
                                if key not in action_names:
                                        if stripped_key not in copy_init_states:
                                                single_object_clause = key
                                                init_cnf.add(single_object_clause)
        clauses = []
        init_cnf_list = []
        while init_cnf:
                clause = init_cnf.pop()
                init_cnf_list.append(clause)
        for atom in range(len(init_cnf_list)):
                clauses.append([atomToNumber(sat_set_dict, init_cnf_list[atom])])

        return clauses

def createGoalStateCnfSentence(atoms_to_numbers_dict, goal_states, horizon):
        current_goal_states = []
        clauses = []
        for state in range(len(goal_states)):
                clauses.clear()
                clauses.append([atomToNumber(atoms_to_numbers_dict, (goal_states[state] + str(horizon)))])
                current_goal_states.extend(clauses)
        return current_goal_states #simple list (not list-in-list)

def extendActions(atoms_to_numbers_dict, all_action_combinations, horizon): #to be run when horizon is >= 1. Extends all possible action schemas for the new time-step 
        previous_time_step = str(horizon-1)
        current_time_step = str(horizon)

        action_var_number = []
        preconds_in_numbers = []
        effects_in_numbers = []

        propostional_logic_statement = []
        actions_cnf = []

        for action in range(len(all_action_combinations)):
                action_var_number.clear()
                preconds_in_numbers.clear()
                effects_in_numbers.clear()
                propostional_logic_statement.clear()

                current_action = all_action_combinations[action]
                #print('Current action: ', current_action)
                action_var_number.append(atomToNumber(atoms_to_numbers_dict, (current_action.name + previous_time_step)))
                for precond in range(len(current_action.preconds)):
                        current_precond = current_action.preconds[precond] + previous_time_step
                        preconds_in_numbers.append(atomToNumber(atoms_to_numbers_dict, current_precond))
                for effect in range(len(current_action.effects)):
                        current_effect = current_action.effects[effect] + current_time_step
                        effects_in_numbers.append(atomToNumber(atoms_to_numbers_dict, current_effect))

                propostional_logic_statement.append(action_var_number)
                propostional_logic_statement.append(preconds_in_numbers)
                propostional_logic_statement.append(effects_in_numbers)

                actions_cnf.append(actionStatementToCnf(propostional_logic_statement))
                #print('Current actions_cnf: ', actions_cnf)
        return actions_cnf #List-in-list

def extendFrameAxioms(atoms_to_numbers_dict, hebrand_base_set, all_action_combinations, horizon): #to be run when horizon is >= 1. Extends all fram axioms for the new time-step
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

        return frame_axioms_cnf

def extendOnlyOneActionAxioms(atoms_to_numbers_dict, all_action_combinations, horizon): #at-least-one and at-most-one axioms for the new time-step
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

        return at_most_one_axioms_cnf, at_least_one_axioms_cnf

def onlyOneActionAxiomToCnf(prop_logic_sentence):
        #input on the form [2,3]
        #means -(2 AND 3)
        not_first_argument = '-' + prop_logic_sentence[0]
        not_second_argument = '-' + prop_logic_sentence[1]
        cnf_clause = [not_first_argument, not_second_argument]
        return cnf_clause

def actionStatementToCnf(prop_logic_sentence): #transforms a prop_logic_sentence from step 3 in the assignment
        #prop_logic_sentence on the form: [['23'], ['2','15', '36'], ['-3', '2', '-36']]
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
        return cnf_expression

def frameAxiomStatementToCnf(prop_logic_sentence):
        # ##prop_logic_sentence = [['23'], ['30'], ['-23']]
        atom = prop_logic_sentence[0]
        atom_negated = '-' + atom[0]

        action = prop_logic_sentence[1]
        action_negated = '-' + action[0]

        #Debug: Is the return-type correct?
        cnf_clause = [atom_negated, action_negated, prop_logic_sentence[2]]
        print('Frame Axiom CNF-expression: ', cnf_clause)
        return cnf_clause


def atomToNumber(atom_to_number_dict, atom_name):
        number = atom_to_number_dict[atom_name]
        return number

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

#encodingHandler()