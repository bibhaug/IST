from hebrand_base import hebrandBase

def encoding_handler():
        initial_sat_set = hebrandBase()
        all_actions, initil_state, goal_state = info_from_file()
        initial_state_CNF = createInitialStateCnfSentence(sat_set)

        her kommer en while løkke som kaller dpll og slikt

def linear_encoder(horizon): #lager final sat_sentence for hver horizon, og returner til encoding_handler som kaller opp dpll() og slikt
        #rekkefølgen ting må gjøres i for å lage sat_sentence, bruker mange av hjelpefunksjonene under
        #har ikke tenkt gjennom hvilken rekkefølge som er helt riktig, men tar utgangspunkt i oppgaveteksten
        goal_states = createGoalStateCnfSentence(goal_states, horizon)
        actions = extendActions(sat_set, horizon)
        fame_axioms = extendFrameAxioms(sat_set, horizon)
        at_least_one_axioms = extendAtLeastOneAxioms(sat_set, horizon)

        return sat_sentence

def createSatSet(): #renamed from give_values_to_hebrandBase()
        #her må keysene endres til å inneholde timesteps
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

def extendSatSet(horizon):
        #utvid med ett timestep
        return sat_set_dict


def createInitialStateCnfSentence(sat_set): #denne kjøres bare en gang 
        Gå gjennom hebrand base, sjekk for negated initial_state (de som er omvent av init_atoms)
        slett de fra hebrand.
        da har vi slettet negated av init, og får bare negated av alt annet.
        slette alle som ikke er init og som er positive.
        return initial_states_list #list med strings

def createGoalStateCnfSentence(goal_states, horizon):
        Vil ha det på liste-form
        return goal_states_list

def extendActions(sat_set, horizon):

        actions_cnf = satToCnf(actions_sat_sentence)
        return actions_cnf

def extendFrameAxioms(sat_set, horizon):

        frame_axioms_cnf = satToCnf(frame_axioms_sat_sentence)
        return frame_axioms_cnf

def extendAtLeastOneAxioms(sat_set, horizon):

        at_least_one_axioms_cnf = satToCnf(at_least_one_axioms_sat_sentence)
        return at_least_one_axioms_cnf


def satToCnf(sat_sentence):
        return cnf_expression #cnf-expression er en liste i liste

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
createSatSet()