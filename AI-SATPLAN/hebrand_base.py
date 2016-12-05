from read_pddl_domain_file import info_from_file


def constantsInDomain():
        all_actions, init_atoms, goal_atoms = info_from_file()
        constants_in_domain = [] ##Alle bokstavene i init_atoms (store bokstaver)
        length_init = len(init_atoms)
        for i in range(0, length_init):
                atom = init_atoms[i]
                length_atom = len(atom)
                for j in range(0,length_atom):
                        letter = atom[j]
                        if letter not in constants_in_domain and letter.isupper():
                                constants_in_domain.append(letter)
        print('Constants_in_domain' , constants_in_domain)
        return constants_in_domain

def groundActions():
        #Skal navnet på Action's være med i grounded_actions-lista?
        all_actions, init_atoms, goal_atoms = info_from_file()
        grounded_actions = {} ## Alle mulige kombinasjoner
        list_of_atoms = [] #Temporary list used to initialize the grounded_action list
        new_preconds = [] #List of all preconds with all the letter-combinations
        num_of_actions = len(all_actions)
        for i in range (0, num_of_actions):
                list_of_atoms += all_actions[i].preconds + all_actions[i].effects #eventuelt plusse på navnet her.
                list_of_atoms += (init_atoms + goal_atoms)
        grounded_actions = set(list_of_atoms) #All excisting actions (without duplicates)
        print('grounded_actions to start with ', grounded_actions)
        character_list = []
        for i in range (0, num_of_actions):
                preconds1 = all_actions[i].preconds #Precondsene til en og en action
                for j in range(0, len(preconds1)):
                        list_of_letters = preconds1[j] #bokstavene i første del av preconds-arrayet
                        for k in range(0, len(list_of_letters)): #går gjennom alle bokstavene
                                for l in range(0, list_of_letters.index('(')):
                                        new_preconds[0] += (list_of_letters[i]-1) #Legger til navnet til precondition (eks. on, clear,..)
                                                for m in range(list_of_letters.index('(')+1, list_of_letters.index(')')): #ser på elementene mellom parantesene
                                                        if list_of_letters[m].isaplha():
                                                                character_list.append(list_of_letters[m])
                                                                 


                        




        #All combinations:
        #Add all already excisting atoms to a list.
        #In preconds list: for each precond, from paranthese start to paranthese slutt, add letters to a list with the name as the first value?

        #generate_new_precond():::
                #find name
                #find how many letters are in the parantheses
                #create list with the letters in the parantheses
                #exchange each letter with new letters from the Constants_in_domain (start med kun verdi nr 1 fra listen (feks. kun A'er))
                #then for each new combination (google) add the atom to the list.
        #in effects list: Do the same



constantsInDomain()
groundActions()

	
