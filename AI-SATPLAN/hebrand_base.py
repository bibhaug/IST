from read_pddl_domain_file import info_from_file
import itertools


def constantsInDomain():
        all_actions, init_atoms, goal_atoms = info_from_file()
        constants_in_domain = []
        length_init = len(init_atoms)
        for i in range(0, length_init):
                atom = init_atoms[i]
                if "," not in atom:
                        for j in range(atom.index('(')+1, atom.index(')')):
                                letter = atom[j]
                                if letter not in constants_in_domain and letter.isupper():
                                        constants_in_domain.append(letter)
                else:
                        letter_before_comma = ""
                        for j in range(atom.index('(')+1, atom.index(',')):
                                startswith= atom[(atom.index('(')+1)]
                                letter_before_comma += atom[j]
                        if letter_before_comma not in constants_in_domain and startswith.isupper():
                                constants_in_domain.append(letter_before_comma)
                        letter_after_comma = ""
                        for j in range(atom.index(',')+1, atom.index(')')):
                                startswith = atom[(atom.index(',') +1)]
                                letter_after_comma += atom[j]
                        if letter_after_comma not in constants_in_domain and startswith.isupper():
                                constants_in_domain.append(letter_after_comma)
        print('Constants_in_domain' , constants_in_domain)
        return constants_in_domain

def all_combinations(how_many_characters):
        n = how_many_characters
        constants_in_domain = constantsInDomain() #list of all constants
        combination_list = []
        for i in itertools.product(constants_in_domain, repeat = n):
                combination_list.append(list(i))
        print('Combination_list ', combination_list)
        return combination_list # [['A', 'A', 'A'], ...]

def groundActions():
        #Skal navnet på Action's være med i grounded_actions-lista? (tror ikke det)
        all_actions, init_atoms, goal_atoms = info_from_file()
        grounded_actions = {} 
        list_of_atoms = []
        name_of_preconds_and_effects = []
        num_of_actions = len(all_actions)
        for i in range (0, num_of_actions):
                list_of_atoms += (init_atoms + goal_atoms)
        grounded_actions = set(list_of_atoms) #All excisting actions (without duplicates)
        print('grounded_actions to start with ', grounded_actions)
        
        for n in range (0, num_of_actions): #Go through each action
                preconds = all_actions[n].preconds
                print('PRECONDS ', preconds)
                one_precondition = []
                for i in range(0, len(preconds)): #go through each precondition
                        one_precondition += preconds[i]
                        name = [] # list for creating name for new precondtion
                        for j in range(0, one_precondition.index('(')):
                                name += one_precondition[j]
                        if name not in name_of_preconds_and_effects: # Excluding already excisting names (hoping its not possible to get on(a,b) AND on(a,b,c))
                                name_of_preconds_and_effects.append(name) #Add name to list (eks. on, clear,..)
                                variable_list = []
                                for j in range(one_precondition.index('(')+1, one_precondition.index(')')): #go through elements between parentheses
                                        if one_precondition[j].isalpha():
                                                variable_list.append(one_precondition[j]) #Add all letters between the parantheses to a list
                                howManyCharacters = len(variable_list) #how many letters do we have
                                list_of_combinations = all_combinations(howManyCharacters) #get all the combinations of the constants in the domain
                                howManyCombinations = len(list_of_combinations) #How many combinations do we get
                                for j in range(0, howManyCombinations): #go through each combination
                                        for k in range(0, len(name_of_preconds_and_effects)): #go through all the different names we have
                                                create_new_precond = []
                                                for l in range (0, len(name_of_preconds_and_effects[k])):
                                                        create_new_precond.append(name_of_preconds_and_effects[k][l]) #add the name to a new precond
                                                if '(' not in create_new_precond:
                                                        create_new_precond.append('(')  #add the start parenthese to a new precond
                                                for m in range(0, len(list_of_combinations[j])):
                                                        create_new_precond.append(list_of_combinations[j][m]) #add the different combinations with a comma between
                                                        if m != (len(list_of_combinations[j])-1):
                                                                create_new_precond.append(',')
                                                create_new_precond.append(')') #Add the end paranthese to the new precond
                                                joined_create_new_precond = "".join(create_new_precond)
                                                if joined_create_new_precond not in grounded_actions:
                                                        grounded_actions.add(joined_create_new_precond)
                        one_precondition = []
                effects = all_actions[n].effects
                print ('EFFECTS ', effects)
                one_effect = []
                for i in range(0, len(effects)):
                		one_effect += effects[i]
                		name = []
                		for j in range(0, one_effect.index('(')):
                				name += one_effect[j]
                		if name not in name_of_preconds_and_effects:
                				name_of_preconds_and_effects.append(name)
                				variable_list = []
                				for j in range(one_effect.index('(')+1, one_effect.index(')')):
                						if one_effect[j].isalpha():
                								variable_list.append(one_effect[j])
                				howManyCharacters = len(variable_list)
                				list_of_combinations = all_combinations(howManyCharacters)
                				howManyCombinations = len(list_of_combinations)
                				for j in range(0, howManyCombinations):
                						for k in range(0, len(name_of_preconds_and_effects)):
                								create_new_effect = []
                								for l in range(0,len(name_of_preconds_and_effects[k])):
                										create_new_effect.append(name_of_preconds_and_effects[k][l])
                								if '(' not in create_new_effect:
                										create_new_effect.append('(')
                								for m in range(0, len(list_of_combinations[j])):
                										create_new_effect.append(list_of_combinations[j][m])
                										if m != (len(list_of_combinations[j])-1):
                												create_new_effect.append(',')
                								create_new_effect.append(')')
                								joined_create_new_effect = "".join(create_new_effect)
                								if joined_create_new_effect not in grounded_actions:
                										grounded_actions.add(joined_create_new_effect)
                		one_effect = []
        print('grounded_actions with new elements', grounded_actions)

        

#constantsInDomain()
groundActions()

	
