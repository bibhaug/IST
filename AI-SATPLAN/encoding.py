from hebrand_base import hebrandBase

#tar hebrand base og gir alle uttrykkene en verdi (1,2,3..)

def give_values_to_hebrandBase():
        hebrand_base_set = hebrandBase() #hebrand_base is keys in the dictionary
        hebrand_base_dict = dict.fromkeys(hebrand_base_set, 0)
        #hebrand_base_dict = {e:0 for e in hebrand_base_set}
        print('Hebrand_base_dict ', hebrand_base_dict)
        value = 1
        hebrand_base_dict_copy = {}
        for key, val in hebrand_base_dict.items():
                hebrand_base_dict_copy[key] = value
                value += 1
        print('Dictionary ', hebrand_base_dict_copy)
        return hebrand_base_dict_copy

#def initial_state_SAT():
#	lag en liste med alle de som skal få den verdien fra funksjonen over, og resten får motsatt verdi.
        



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
