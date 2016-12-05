class Action:
        def __init__(self, name):
                self.name = name
                self.preconds = []
                self.effects = []

        def add_preconds(self, precond):
                self.preconds.append(precond)

        def add_effects(self, effect):
                self.effects.append(effect)

        def __repr__(self):
                return "%s; %s, %s" % (self.name, self.preconds, self.effects)
		 
def info_from_file():
	f = open('blocks.dat', 'r')
	line = f.readline()
	init_atoms = []
	goal_atoms = []
	all_actions = [] #List of Action Objects
	while line:
		if line != '\n':
			splitLine = line.split()
			#print('splitLine: ', splitLine[0])
			length_of_line = len(splitLine)
			if line.startswith('I'):
				for i in range(1,length_of_line):
					init_atoms.append(splitLine[i])
			elif line.startswith('A'):
				a = Action(splitLine[1])
				until_arrow = splitLine.index('->')
				for i in range(3,until_arrow):
					a.add_preconds(splitLine[i])
				for j in range((until_arrow+1), length_of_line):
					a.add_effects(splitLine[j])
				all_actions.append(a)
			elif line.startswith('G'):
				for i in range(1,length_of_line):
					goal_atoms.append(splitLine[i])
		line = f.readline()
	#print('init_atoms ', init_atoms)
	#print('goal_atoms ', goal_atoms)
	#print('all_actions ', all_actions)
	#print('Preconds1 ',all_actions[0].preconds)
	#print('Preconds2 ', all_actions[1].preconds)
	#print('Effects1 ', all_actions[0].effects)
	#print('Effects2 ', all_actions[1].effects)
	return all_actions, init_atoms, goal_atoms
    		#Har ikke delt opp navn og variabler i listene enda 		
    		#Sjekke stor, liten bokstav, lese pil, -tegn, egen lesing for I, A og G (Siden A er rar)

info_from_file()



##def addActions(file_name):
##	f = open('file_name, 'r')
##	all_actions = []
##	line = f.readline()
##	while line:
##		 if line != '\n':
##			 splitLine = line.split()
##			 length_of_line = len(splitLine)
##			 if line.startswith('A'):
##				a = Action(splitLine[1])
##				until_arrow = splitLine.index('->')
##				for i in range(3,until_arrow):
##					a.add_preconds(splitLine[i])
##				for j in range((until_arrow+1), length_of_line):
##					a.add_effects(splitLine[j])
##				 all_actions.append(a)
##	return all_actions
##
##def 
				 

