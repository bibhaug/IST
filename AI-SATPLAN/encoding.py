from hebrand_base import hebrandBase

def give_values_to_hebrandBase():
        hebrand_base_set = hebrandBase() 
        hebrand_base_dict = dict.fromkeys(hebrand_base_set, 0)
        print('Hebrand_base_dict ', hebrand_base_dict)
        value = 1
        hebrand_base_dict_copy = {}
        for key, val in hebrand_base_dict.items():
                hebrand_base_dict_copy[key] = value
                value += 1
        print('Dictionary ', hebrand_base_dict_copy)
        return hebrand_base_dict_copy


def encoding_handler():
        hebrand_base = hebrandBase()
        all_actions, initil_state, goal_state = info_from_file()
        initial_state_CNF = initil_state_SAT(hebrand_base)



#def initial_state_SAT(henbrand_base): 
Gå gjennom hebrand base, sjekk for negated initil_state (de som er omvent av init_atoms)
slett de fra hebrand.
da har vi slettet negated av init, og får bare negated av alt annet.
slette alle som ikke er init og som er positive.
return clauses (list med strings)

def goal_state_CNF(goal_states):
        Vil ha det på liste-form
        return goal_states_list


def SAT_to_CNF(): #kanskje to forskjellige funksjoner for punkt 3 og 4

#deale med tids-stg
#for løkke der i er tidssteget
#dpll inni forløkken og sjekke for cnf setningen du har der og da.



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
give_values_to_hebrandBase()
