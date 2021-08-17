###Bubbles FUNCTIONS###

### Authors: Luis Manuel Muñoz Nava and Marcos Nahmad

## Import some python packages
import numpy as np
import networkx as nx 
import matplotlib.pyplot as plt 
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
import pandas as pd
import random
import pickle

############# Functions #############

def probability_choice(probability_):
	"""This function returns a true or false depending on a probability"""
	probability_choice_ = False
	random_number = random.uniform(0,1)
	if random_number <= probability_:
		probability_choice_ = True

	return probability_choice_


def population_type(num_fam,fam_memb_num):
	"""This function makes a list of all the indiviudals type (Adult, Child and Child in the Bubbles program)"""
	total_population_type = [] # Empty list to append all the individuals type (Adult, Other, Child in the Bubbles program)
	child_in_NUC_list = [] # Empty list to append the children in the Bubbles program

	### A loop to look for every family
	for i in range(num_fam):
		### To define the number of children that will go to a bubble per family ###
		### There is always a child in the Bubbles program, we set a probability to have a second (50%) or third (25%) child in the Bubbles program per family
		prob_second_child_in_NUCLEO = probability_choice(0.5) # Using the probability_choice function (defined before), we determined if the second child goes to a bubble
		prob_third_child_in_NUCLEO = probability_choice(0.25) # Using the probability_choice function (defined before), we determined if the third child goes to a bubble
		child_in_NUC = 1 + prob_second_child_in_NUCLEO + prob_third_child_in_NUCLEO # To know the total number of children that will go to a bubble
		child_in_NUC_list.append(child_in_NUC) # To append the total number of children that will go to a bubble per family

		### To fill the list of all the population within the network school ###
		family_members = ["Adult","Adult"] # A list for every family with two adults and the rest are children
		for child in range(fam_memb_num-2): # A loop for the two children in every family
			family_members.append("Child") # Complete the family members list with children
		total_population_type.extend(family_members) # Append all the members of the family to the list of all the population

	return (total_population_type, child_in_NUC_list) # Returns the three lists described above


def create_the_family_network(num_fam, fam_memb_num, total_population_type, child_in_NUC_list):
	"""This function generates the network with all the families"""
	N = nx.Graph() # Generates the graph
	N.add_node(0, Type = "Society", State = "C", NUCLEO = False, Family = False, Infect_through_NUCLEO = 0, NUCLEO_number = 0, Days_after_symptoms_onset = 0, Symptomatic = "False") # It adds the Society node
	
	### To show when plotting the Graph ###
	color_family_edge = [] # Emtpy list to append all the edges inside the families to show in the Graph
	color_adult_society = [] # Empty list to append all the edges from the adults to the society to show in the Graph
	adult_nodes = [] # Empty list to append all the nodes numbers corresponding to adults to show in the Graph	
	
	### Lists to append information about the nodes and the families ###
	nodes_num = [0] # List to append the number of all the nodes (number 0 corresponds to the society node)
	children_in_NUC_program = [] # Empty list to append all the nodes numbers corresponding to children in the Bubbles porgram
	family_number_list = [] # Empty list to append the number of all the families
	
	m = 0 # To iterate from 0 for every individual
	l = 1 # To iterate from 1
	p = 0 # To iterate from 0 for family and not individual
	for i in range(num_fam): # Iterate over all the families
		family_number_list.append(p+1) # To append the number of the current family
		child_in_NUC = child_in_NUC_list[p] # The number of children that will go to the Bubbles program in the current family
	
		### To create the nodes, nodes atributes and edges in the network ###
		for mem in range(fam_memb_num): # Iterate in all the members of a family
			N.add_node(l) # Add the current node to the network
			N.nodes[l]["Type"] = total_population_type[m] # Assign the corresponding type attribute ("Adult" or "Child") to the current node from the type list
			N.nodes[l]["State"] = "S" # Assign a susceptible to infection state for all the nodes 
			N.nodes[l]["Family"] = p + 1 # Assign a unique and consecutive number for every family
			N.nodes[l]["NUCLEO"] = False # Not to be in a bubble yet (NUCLEO is a possible name in spanish)
			N.nodes[l]["NUCLEO_number"] = 0 # Not bubble (NUCLEO) assigned yet
			N.nodes[l]["Days_after_symptoms_onset"] = 0 # To count the days after a symptoms onset
			N.nodes[l]["Symptomatic"] = False # To decide if the node is going to be symptomatic or asymptomatic in case of infection
			
			# If the node is an Adult
			if total_population_type[m] == "Adult":	# Make an edge from all Adult nodes in the population to the Society node				
				N.add_edge(l,0, type = "To society") # Add the edge adult-society in the network
				color_adult_society.append((l,0)) # Append the corresponding adult-society values to the list to give color to all the adult-society nodes
				adult_nodes.append(l) # Append the current node to a list of 

			# If the node is a Child that will go to a bubble
			elif total_population_type[m] == "Child" and child_in_NUC > 0: # Looks if the current node is a Child and if it will go to a bubble depending on the number of children that family is having in the Bubbles program
				N.nodes[l]["NUCLEO"] = True # Establish the children to be in the Bubbles program
				children_in_NUC_program.append(l) # Append the children to a list of all the children in the Bubbles program
				child_in_NUC -= 1 # One children less to go to the Bubbles program for the current family

			# Create the edges within the current family
			memb_tup_list = [] # Empty list to append tuples to make edges within family members
			for h in range(mem): # Iterates in the family members to make edges between them
				memb_tup = (l-(h+1),l) # Tuple within two members of the current family
				memb_tup_list.append(memb_tup) # Append the tuple to the list within the family
				color_family_edge.append(memb_tup) # Append the corresponding edge within the family to give a color when plotting the Graph
			N.add_edges_from(memb_tup_list, type = "In family") # Generates the edges between all the members in the corresponding family

			nodes_num.append(l) # Append the nodes number to the list of all the nodes
			m += 1
			l += 1
		p += 1

	return (N, nodes_num, adult_nodes, children_in_NUC_program, color_family_edge, color_adult_society, family_number_list) # Returns the network with all the nodes and edges between society and families 


def assign_NUCLEOS(N, nodes_num, adult_nodes, children_in_NUCLEOs_program, possible_memb_NUCLEO, color_family_edge, color_adult_society, teacher, family_number_list, num_teachers):
	"""This function assigns all the children in the Bubbles program to a bubble"""
	N_NUC = nx.Graph(N) # Create a new network that is equivalent to the network N (to iterate on) not changing the original
	families_in_NUCLEOs_program = list(family_number_list) # Create a list that is equivalent to the list of the family list, to avoid changing the original
	color_NUCLEO_edge_list = [] # Empty list to append all the edges inside every bubble to give a color when plotting the Graph


	### To create the bubbles ###
	NUCLEOs_list_all_list = [] # Empty list to append all the 10 possible bubbles arrangment
	NUCLEOS_list_all_len_list = [] # Empty list to save the length of the 10 possible bubbles arrangment 
	children_in_NUC_program_left_list = [] # Empty list to append the children without an assigned bubble

	# To make the bubbles arrangment 10 different times (to decide the best arrangment)
	for i in range(10):
		children_in_NUC_program = list(children_in_NUCLEOs_program) # List with the children in the Bubbles program (as children are assigned to a bubble, they are going to be removed from the list)
		children_in_NUC_program_len = len(children_in_NUC_program) # Length of the list with the children in the Bubbles program (as children are assigned to a bubble, they are going to be removed from the list)
		NUCLEOS_list_all = [] # Empty list to append all the NÚCLEOS
		n = 0

		# While there are children without a bubble assignated
		# Try with up to 5 times to assign all the members in the Bubbles program to a bubble
		while children_in_NUC_program_len > 0: 

			NUCLEO_list = [] # Empty list to append all the members in a bubble
			neighbors_all = [] # Empty list to append all the neighbors (especially the brothers) for the members in a bubble (to avoid icluding brothers in the same bubble)

			### If the bubble size is 0 or 1, there are not bubbles created
			if possible_memb_NUCLEO == 0 or possible_memb_NUCLEO == 1: 
				for child_ in children_in_NUC_program: # Loop over all the children in the Bubbles program
					N_NUC.nodes[child_]["NUCLEO"] = 0 # Take out all the children from the bubbles, so everyone are in home
				break 

			### If the size of the bubble is > than 1
			# To make bubbles of a corresponding defined value
			if len(children_in_NUC_program) >= possible_memb_NUCLEO: # If there are enough children left without a bubble to fill all the size of the bubble
				l = 0
				# Try with up to 10 times to assign all the members in the bubble
				while len(NUCLEO_list) < possible_memb_NUCLEO: # While the bubble has less members than desired

					for memb_NUC in NUCLEO_list: # For every member that is already in the current forming bubble
						neighbors = list(N_NUC.neighbors(memb_NUC)) # Collect the node number of all it neighbors
						neighbors_all.extend(neighbors) # Extend a list with all the neighbors (to look for the brothers) of the members in the bubble

					# To assign the members of the bubble
					NUCLEO_member_try = 0 
					# It will try to create the bubble up to 10 times to avoid assigning brothers in the same bubble
					while NUCLEO_member_try < 10: # While the the try is less than 10
						for i in range(len(children_in_NUC_program)): # A loop of length equivalent to every child without an assigned bubble
							child_random = random.choice(children_in_NUC_program) # Select randomly from the list of the children without an assigned bubble
							if child_random not in neighbors_all and child_random not in NUCLEO_list: # If the child is not in the forming bubble and is not a brother of a member of the forming bubble
								NUCLEO_list.append(child_random) # The child is assigned to the current bubble
								NUCLEO_member_try = 12000 # An extrem number to break the while loop
								break
							else: 
								NUCLEO_member_try += 1 # To try again (up to 10 times) to assign a child to the bubble
					# If the try to create the bubble is the number 10, break the while loop and stop trying to form the corresponding bubble
					if l == 10:
						break
					# If a member of the bubble has been assigned, continue to assign the rest to complete the bubble size
					if NUCLEO_member_try == 12000:
						continue
					# If the member is not assigned, try again up to 10 times
					else:
						l += 1

			# Append the new bubble to a list with all the bubbles
			if len(NUCLEO_list) == possible_memb_NUCLEO: # If the new bubble has the correct size
				NUCLEOS_list_all.append(NUCLEO_list) # Append the new bubble to the list of all the bubble
			else: # If is not of the correct size
				NUCLEO_list = [] # The bubble needs to be created again

			# Remove all the members in the bubble from the list of children without an assigned bubble
			for n in NUCLEO_list: # For every member in the bubble
				children_in_NUC_program.remove(n) # Remove them from the list of children without an assigned bubble

			children_in_NUC_program_len -= possible_memb_NUCLEO # Substract the length of the total length of the children without an assigned bubble

			# Decide to remove the children not assigned to a bubble from the Bubbles promgram
			# If after trying 5 times there are children without a bubble assigned, stop trying (This children are going to be out of the bubbles program)
			if n == 5:
				break
			n += 1

		# Append to a list the bubbles data for every possible arrangment to decide which was the best arrangment (10 possibles arrangmets)
		children_in_NUC_program_left_list.append(children_in_NUC_program) # To append the children that were not assigned to a bubble for every possible arrangment of the bubbles

		NUCLEOS_list_all_len_list.append(len(NUCLEOS_list_all)) # To append the total number of bubbles created for every possible arrangment of the bubbles

		NUCLEOs_list_all_list.append(NUCLEOS_list_all) # To append the bubbles created to the list for every possible arrangment of the bubbles

	### Set the final arrangment of the bubbles, with the best arrangment of the 10 possible
	# The best arrangment is the one with more bubbles
	index_max_len_NUCLEOs = NUCLEOS_list_all_len_list.index(np.max(NUCLEOS_list_all_len_list)) # Look for the index of the arrangment with more bubbles created

	NUCLEOS_list_all = NUCLEOs_list_all_list[index_max_len_NUCLEOs] # Set the final arrangment of the bubbles

	children_in_NUC_program = children_in_NUC_program_left_list[index_max_len_NUCLEOs] # Set the children that weren't assigned to a bubble in the final arrangment

	### Take out of the Bubbles program the children not assigned to a bubble 
	for children_left in children_in_NUC_program: # For every child in the list of children without a bubble
		N_NUC.nodes[children_left]["NUCLEO"] = 0 # Take out the child from the Bubbles program changing the NUCLEO (bubble) argument from True to False

	### To create the edges of the bubbles in the school network ### 
	NUC = 1 # To count form 1
	list_of_NUCLEOs = [] # To append a list of all the bubbles
	list_of_fams_for_each_NUCLEO_list = [] # To append the families that correspond to every bubble
	teachers_fams_list = [] # To append the fams of the teachers
	teachers_list = [] # To append the teachers in the bubbles
	list_of_teachers_for_each_NUCLEO_list = [] # To append the teachers for each bubble
	for NUCLEO in NUCLEOS_list_all: # Iterate over all the bubbles
		list_of_fams_for_each_NUCLEO = [] # To append all the fams for the current bubble
		list_of_teachers_for_each_NUCLEO = [] # To append the teachers for each bubble
		### To assign a teacher if it is specified
		if teacher == True: # If the bubble includes a teacher 
			for i in range(num_teachers): # If there are more than 1 teacher, then make a loop for all teachers
				N_NUC.add_node("teacher"+str(i)+"_"+str(NUC)) # Add a node for the teacher
				N_NUC.nodes["teacher"+str(i)+"_"+str(NUC)]["Type"] = "Adult" # Make it Type teacher
				N_NUC.nodes["teacher"+str(i)+"_"+str(NUC)]["State"] = "S" # Susceptible state
				N_NUC.nodes["teacher"+str(i)+"_"+str(NUC)]["Family"] = "T"+str(i)+"_"+str(NUC) # Teacher family is defined with a T and the bubble number (is the only member in the family)
				N_NUC.nodes["teacher"+str(i)+"_"+str(NUC)]["NUCLEO"] = True # To be in the Bubbles program
				N_NUC.nodes["teacher"+str(i)+"_"+str(NUC)]["Days_after_symptoms_onset"] = 0 # To count the days after a possible infection
				N_NUC.nodes["teacher"+str(i)+"_"+str(NUC)]["Symptomatic"] = False # To decide if the node is going to be symptomatic or asymptomatic in case of infection
				N_NUC.add_edge("teacher"+str(i)+"_"+str(NUC),0, type = "To society") # Join it to the society node
				NUCLEO.append("teacher"+str(i)+"_"+str(NUC)) # Append the teacher to the bubble list
				teachers_list.append("teacher"+str(i)+"_"+str(NUC)) # Append the teacher number to the list
				teachers_fams_list.append("T"+str(i)+"_"+str(NUC)) # Append the teacher's fam number to the list
				list_of_teachers_for_each_NUCLEO.append("teacher"+str(i)+"_"+str(NUC)) # Append the teacher to a list of teachers within the bubble
				adult_nodes.append("teacher"+str(i)+"_"+str(NUC)) # Append the teacher to the adults nodes list
				color_adult_society.append(("teacher"+str(i)+"_"+str(NUC),0)) # Apend the teacher to the list to give the color from society to adult when plotting the network
			list_of_teachers_for_each_NUCLEO_list.append(list_of_teachers_for_each_NUCLEO) # Apend to the total teachers within the current bubble to a list of all the bubbles
	
		# To create the edges within the bubble	
		for memb_in_NUC in NUCLEO: # For every member in a bubble
			if N_NUC.nodes[memb_in_NUC]["Type"] == "Child": # If the member is a child
				list_of_fams_for_each_NUCLEO.append(N_NUC.nodes[memb_in_NUC]["Family"]) # Append the family to the list of the corresponding bubble
				if N_NUC.nodes[memb_in_NUC]["Family"] in families_in_NUCLEOs_program:
					families_in_NUCLEOs_program.remove(N_NUC.nodes[memb_in_NUC]["Family"]) # Remove the family from the list of families to be assigned to a bubble (all the families here are of the children not assigned to a bubble)
			N_NUC.nodes[memb_in_NUC]["NUCLEO_number"] = NUC # Assign a bubble number
			list_of_tuples = [] # Empty list to append the tuples of one member of the bubble with every other members to create all the edges inside the bubble in the network
			for i in range(len(NUCLEO)): # Iterate over the range of the bubble length
				if memb_in_NUC in list_of_teachers_for_each_NUCLEO and NUCLEO[i] in list_of_teachers_for_each_NUCLEO: # If there are more than one teachers, to avoid joining them directly through an edge
					continue
				elif memb_in_NUC != NUCLEO[i]: # If the current member and the iteration member are not the same
					tup_memb = (NUCLEO[i],memb_in_NUC) # Create a tuple for the member of the bubble with te rest of the members
					list_of_tuples.append(tup_memb) # Append the tuples to a list
					### To show when plotting the Graph
					if (NUCLEO[i],memb_in_NUC) in color_NUCLEO_edge_list or (memb_in_NUC,NUCLEO[i]) in color_NUCLEO_edge_list: # If the tuple is in the list of edges between a bubble do nothing
						continue
					else:
						color_NUCLEO_edge_list.append(tup_memb) # Append the tuples to a list to generate a color in the network that correspond to the edges inside the bubbles
			N_NUC.add_edges_from(list_of_tuples, type = "NUCLEO") # Create the edges inside the bubbles in the network
		list_of_fams_for_each_NUCLEO = list(set(list_of_fams_for_each_NUCLEO)) # Remove repeated families from the list of families for each bubble
		list_of_fams_for_each_NUCLEO_list.append(list_of_fams_for_each_NUCLEO) # Append the list of families for each bubble to a general list for all bubbles
		list_of_NUCLEOs.append(NUC) # Append the number of bubble to a list of bubbles numbers
		NUC += 1

	### Extend the list of the families that were not assigned to a bubble
	fams_not_in_NUCLEOs = [0] # Number 0 correspond to the society (this list is to take out this families from the iteration of the model)
	fams_not_in_NUCLEOs.extend(families_in_NUCLEOs_program) # The families that were not assigned to be part of a bubble

	### To take out the families that will not participate in the program from the list to plot later in the Graph
	adults_to_remove = [adult for adult in adult_nodes if N_NUC.nodes[adult]["Family"] in families_in_NUCLEOs_program] # If the adult is member of a family taken out from the Bubbles program
	adult_nodes_copy = list(adult_nodes) # Make a copy of the adult_nodes list to remove an adult from the copy when the family of an adult is not in the Bubbles program
	color_family_edge_copy = list(color_family_edge) # Make a copy of the color_family_edge
	color_adult_society_copy = list(color_adult_society) # Make a copy of the color_adult_society
	for adult in adults_to_remove: # For all adults in the adult_nodes list
		if adult in adult_nodes_copy: # It will look for just the first adult for every family, because when it finds it, it will remove also the spouse
			adult_nodes_copy.remove(adult) # Remove the adult from the copy list
			adult_nodes_copy.remove(adult+1) # Remove the spouse of the first adult
			for i in color_family_edge: # For every tuple in the list of tuples for coloring the family edges
				if adult in i or adult+1 in i or adult+2 in i or adult+3 in i or adult+4 in i: # Look if one member or the entire family (5 members) is in the tuple
					if i in color_family_edge_copy: # If the tuple is still in the color_family_edge_copy list
						color_family_edge_copy.remove(i) # Remove it
			for i in color_adult_society: # For every tuple in the list of tuples for coloring the adult to society edges
				if adult in i or adult+1 in i: # If one of the adults of the family is in the tuple
					if i in color_adult_society_copy: # If the tuple is still in the color_adult_society_copy list
						color_adult_society_copy.remove(i) # Remove it


	return (N_NUC, adult_nodes_copy, color_adult_society_copy, color_family_edge_copy, NUCLEOS_list_all, color_NUCLEO_edge_list, list_of_NUCLEOs, list_of_fams_for_each_NUCLEO_list, fams_not_in_NUCLEOs, teachers_list, list_of_teachers_for_each_NUCLEO_list, teachers_fams_list) # Returns the network, a list with al the edges corresponding to the NÚCLEOS and a list with the NUCLEOs number



def iterate_the_network(N_NUC,steps_in_the_model,S_state,I_state,A_state,C_state,R_state, symptoms_detection_day_index, nodes_num, family_number_list, child_in_NUC_list, NUCLEOS_list_all, adult_nodes, color_family_edge, color_adult_society,color_NUCLEO_edge_list, probabilities, asympt_states, sympt_states, using_mask, list_of_NUCLEOs, probability_from_society, list_of_fams_for_each_NUCLEO_list, fams_not_in_NUCLEOs, intervention, teacher, teachers_list, list_of_teachers_for_each_NUCLEO_list, teachers_fams_list):
	"""This function iterate over all the network and update the nodes state"""
	
	N = nx.Graph(N_NUC) # Set the graph to be a new one to avoid modifing the initial network
	N_original = nx.Graph(N) # Create a new network that is equivalent to the network N (to know the the initial values of the network)

	### Zeros lists with length of the total number of bubbles to set some information about a particular bubble
	list_of_previous_infected_NUCLEOS_calculated = list(np.zeros(len(list_of_NUCLEOs))) # To set when a bubble has been previously fragmented because of symptoms onset
	list_of_previous_infected_NUCLEOS_real = list(np.zeros(len(list_of_NUCLEOs))) # To set really when a bubble has been previously infected (depending on the infection onset instead of symptoms onset)
	list_of_infected_NUCLEOS_calulated = list(np.zeros(len(list_of_NUCLEOs))) # To set when a bubble has a previous positive case (symptomatic cases)
	list_of_infected_NUCLEO_real_count = list(np.zeros(len(list_of_NUCLEOs))) # To set when a bubble has a previous positive case (infection onset)
	new_cases_through_NUCLEOS_list_calculated = list(np.zeros(len(list_of_NUCLEOs))) # To count the number of infected families through the bubble (detecting only symptomatic cases)
	new_cases_through_NUCLEOS_list_real_count = list(np.zeros(len(list_of_NUCLEOs))) # To count the number of infected families through the bubble (detecting the infection onset)
	days_of_infection_in_NUCLEO = list(np.zeros(len(list_of_NUCLEOs))) # To count the number of days after a positive detected case with symptoms
	days_of_infection_in_NUCLEO_real_count = list(np.zeros(len(list_of_NUCLEOs))) # To count the number of days after a positive case (infection onset)

	### To visualize in the plot
	color_for_NUCELO_edge = list(color_NUCLEO_edge_list) # To see in the plot when there is an infection through the bubble
	pos = nx.spring_layout(N) # Set a position for every node in the graph to plot (to have the same position for every step)
	
	### Other lists to store data from the simulation
	list_of_fams_in_infected_NUCLEOS_calculated = [] # List to append the families with positive cases to calculate infection through a bubble
	list_of_fams_in_infected_NUCLEOS_real_count = [] # List to append the families with positive cases to measure the real count of infection through a bubble
	families_counting_after_symptomatic_detection_day = list(np.zeros(len(family_number_list))) # To count the number of days after the symptoms detection for every family
	families_counting_days_in_home = list(np.zeros(len(family_number_list))) # To count the number of days a family is not assisting to the bubble and are in home
	families_with_a_member_in_symptomatic_detection_day = [] # A general list to append the families with symptoms onset
	families_in_fragmented_NUCLEOs = [] # To append the family number to a list of families in fragmented bubbles
	not_complete_NUCLEO_return = [] # To append the bubbles in which not all the families returned after 14 days of fragmentation
	not_complete_teachers_NUCLEO_return = [] # To append the bubbles in which not all the teachers returned after 14 days of fragmentation
	fams_not_returned_to_NUCLEO_list = [] # To append the families that didn't return to the bubbles after 14 days of fragmentation
	fams_in_home_at_day_list = [] # To know the number of families not attending to the bubbles every day
	new_cases_list = [] # List to append the new positive cases for every day
	families_infected_every_day_list = [] # To append the families that get infected daily
	total_fams_infected_real = [] # To append the total families that got infected	
	total_fams_infected_real_through_NUCLEO = [] # To append the total families that got infected through a bubble	
	teachers_to_return_later_to_NUCLEO_list = [] # 
	for NUCLEO_ in list_of_NUCLEOs: # To create a list for every individual bubble inside other lists
		list_of_fams_in_infected_NUCLEOS_calculated.append([]) # Empty list for every bubble to append families with symptoms
		list_of_fams_in_infected_NUCLEOS_real_count.append([]) # Empty list for every bubble to append families with an infected member
		teachers_to_return_later_to_NUCLEO_list.append([]) # Empty list to append the teachers that will return later to the bubbble

	### To count the number of infected or just symptomatic cases
	total_cases = 0 # To add every new real case
	total_detected_cases = 0 # To add every detected or symptomatic case

	
	### A loop to iterate over all the steps in the simulation
	b = 0 # To iterate from 0
	# For a specific day in the model
	for i in range(steps_in_the_model):
		N1 = nx.Graph(N) # Create a new network that is equivalent to the network N (to iterate on)
		
		### Create lists for coloring the ploted network depending on the state of the nodes
		s_nodes_color = [] # Empty list to append all the nodes in the S state
		i_nodes_color = [] # Empty list to append all the nodes in the I state list
		a_nodes_color = [] # Empty list to append all the nodes in the A state list
		c_nodes_color = [] # Empty list to append all the nodes in the C state list
		r_nodes_color = [] # Empty list to append all the nodes in the R state
		color_for_NUCELO_reintegration = [] # Empty list to append the edges to rejoin within the bubbles
		color_for_brothers_reintegration = [] # Empty list to append the edges to rejoin the brothers to their corresponding bubble
		infection_in_NUCLEO_edges = [] # Empty list to append and show in the plot the infections through the bubble
		
		### Lists to append values for every step in the model
		families_infected_every_day = [] # To append the families that are infected every day
		families_with_symptoms = [] # To append the families with a symptomatic member for every step in the model
		to_append_to_families_in_fragmented_NUCLEOs = [] # To append the families to the list of families in fragmented bubbles
		families_true_list_for_counting_after_symptomatic_detection_day = list(np.zeros(len(family_number_list))) # To avoid double counting (just detect the first member in a family to count one day in home for each step)
		families_true_list_for_counting_days_in_home = list(np.zeros(len(family_number_list))) # To avoid double counting in days in home for every family
		
		### To count the number of infected cases and the families not attending to a bubble
		new_cases = 0 # To know the total new cases for every step
		fams_in_home_at_day = 0 # know the number of families not attending to the bubble in the current day

		### A loop to iterate over all the nodes in the network
		for node in list(N.nodes):
			if N.nodes[node]["Family"] not in fams_not_in_NUCLEOs: # Not to iterate the society (fam 0) and the families not in the bubbles program
				### Create a list of the first neighbors for the node 
				neighbors = list(N.neighbors(node)) # Make a list of all it first neighbors
				neighbors_in_the_same_NUCLEO = [neighbor for neighbor in neighbors if N.edges[node,neighbor]["type"] == "NUCLEO" and N.nodes[neighbor]["Family"] != N.nodes[node]["Family"]] # List of the neighbors in the same bubble 
				family_node_infected = [True for neighbor in neighbors if N.nodes[neighbor]["Family"] == N.nodes[node]["Family"] and N.nodes[neighbor]["State"] == C_state[symptoms_detection_day_index]] # Create a list of True values for all the members in the family that are in the symptoms detection day

				### To check if there are symptopatic cases
				# If the node or someone in the family of the node is in the symptoms detection day
				if N.nodes[node]["NUCLEO"] == True and (N.nodes[node]["State"] == C_state[symptoms_detection_day_index] or len(family_node_infected) >= 1):
					### To calculate the Estimated R0, new symptomatic cases through a bubble 
					numb_of_NUCLEO = N.nodes[node]["NUCLEO_number"] # Find the bubble number of the node
					index_of_NUCLEO_number = list_of_NUCLEOs.index(numb_of_NUCLEO) # Find the index position of the bubble in the bubbles list

					### To detect a bubble with the first family with symptoms
					if list_of_infected_NUCLEOS_calulated[index_of_NUCLEO_number] == 0: # If there are no previous positive cases in the bubble
						if N.nodes[node]["Family"] not in families_in_fragmented_NUCLEOs: # If the family of the node is not in the list of families in fragmented bubbles (to avoid double counting)		
							list_of_infected_NUCLEOS_calulated[index_of_NUCLEO_number] = True # Set this value to True to say that this bubble has a positive case 
							list_of_fams_in_infected_NUCLEOS_calculated[index_of_NUCLEO_number].append(N.nodes[node]["Family"]) # Append the family number to a list of infected families in the bubble

					### To Estimate the R0 when the bubble has already a symptomatic case
					elif list_of_infected_NUCLEOS_calulated[index_of_NUCLEO_number] == True: # If there are previous positive cases in the bubble
						if N.nodes[node]["Family"] not in list_of_fams_in_infected_NUCLEOS_calculated[index_of_NUCLEO_number]: # If the family number of the node is not in the list of infected families in the bubble (to avoid double counting)
							### The Estimated R0 is going to be calculated just the first time the bubble has a symptomatic case
							if list_of_previous_infected_NUCLEOS_calculated[index_of_NUCLEO_number] == 0: # If there are no previous fragmentations of the bubble
								new_cases_through_NUCLEOS_list_calculated[index_of_NUCLEO_number] += 1 # Add 1 new case to the Estimated R0 (cases are for families and not for individuals)
							list_of_fams_in_infected_NUCLEOS_calculated[index_of_NUCLEO_number].append(N.nodes[node]["Family"]) # Append the family number to a list of infected families in the bubble

					### If intervention is set to True to fragment the bubbles
					if intervention == True:
						### To fragment the bubble
						neighbors_in_frag_NUC = [] # List to append the neighbor nodes to be fragmented
						for neighbor in neighbors:
							# If the node is in the same bubble as the neighbor and the node are not members of the same family
							if N.edges[node,neighbor]["type"] == "NUCLEO" and N.nodes[neighbor]["Family"] != N.nodes[node]["Family"]:
								neighbors_in_frag_NUC.append(neighbor) # Append the neighbor to the list to be fragmented 
								neighbors_N1 = list(N1.neighbors(node)) # Make a list of the neighbor nodes in the N1 network (the list for the next day or step) to know if the edge between the two nodes is still there (maybe it was deleted by another node in the same step)
								### To append the families to a list of families in fragmented bubbles
								if N.nodes[node]["Family"] not in families_in_fragmented_NUCLEOs: # If the family of the node is not in the list of families in fragmented bubbles
									to_append_to_families_in_fragmented_NUCLEOs.append(N.nodes[node]["Family"]) # Append de family to the list
								if N.nodes[neighbor]["Family"] not in families_in_fragmented_NUCLEOs: # If the family of the neighbor is not in the list of families in fragmented bubbles
									to_append_to_families_in_fragmented_NUCLEOs.append(N.nodes[neighbor]["Family"]) # Append de family to the list
								### If the neighbor still being a neighbor in the N1 network, then...
								if neighbor in neighbors_N1:
									N1.remove_edge(node,neighbor) # Remove the edge between the neighbor and the node
									if (node,neighbor) in color_for_NUCELO_edge:  # If the node and neighbor edge is in a list of bubbles edges
										color_for_NUCELO_edge.remove((node,neighbor)) # Remove the edge from the list
									elif(neighbor,node) in color_for_NUCELO_edge: # If the neighbor and node edge is in a list of bubbles edges
										color_for_NUCELO_edge.remove((neighbor,node)) # Remove the edge from the list

						### To separate the brothers (from their corresponding bubble) of children that are in a fragmented bubble (not including the actual node)
						for memb in neighbors_in_frag_NUC: # Iterate over the members (neighbors) in the fragmented bubble not intcluding the actual node
							neighbor_fam_NUC = [fam_memb for fam_memb in list(N.neighbors(memb)) if N.nodes[fam_memb]["NUCLEO"] == True] # Look for the brothers that also go to another bubble
							for n in neighbor_fam_NUC: # For all the brothers in another bubble
								NUCLEO_edges = [k for k in list(N.neighbors(n)) if N.edges[n,k]["type"] == "NUCLEO" and N.nodes[k]["Family"] != N.nodes[n]["Family"]] # Look for the members of the brother's bubble
								neighbors_N1_n = list(N1.neighbors(n)) # Make a list of the neighbor nodes in the N1 network (the list for the next day or step) to know if the edge between the two nodes is still there
								for k in NUCLEO_edges: # For every member in the brother's bubble
									if k in neighbors_N1_n: # If the member still being a neighbor in the N1 network, then...
										N1.remove_edge(k,n) # Remove the edge between the member and the brother
										if (k,n) in color_for_NUCELO_edge: # If the brother and bubble member edge is in a list of bubbles edges
											color_for_NUCELO_edge.remove((k,n)) # Remove the edge from the list
										elif(n,k) in color_for_NUCELO_edge: # If the NUCLEO member and brother edge is in a list of bubbles edges
											color_for_NUCELO_edge.remove((n,k)) # Remove the edge from the list

					### For start counting the days for every family after symptoms onset (in the detection day) 			
					index_of_fam_number = family_number_list.index(N.nodes[node]["Family"]) # Look for the index number of the family in the family number list

					if N.nodes[node]["Family"] not in families_with_a_member_in_symptomatic_detection_day: # If the family is not in a list of families with symptoms
						families_with_a_member_in_symptomatic_detection_day.append(N.nodes[node]["Family"]) # Append the family number to a general list of families with symptoms
						families_true_list_for_counting_after_symptomatic_detection_day[index_of_fam_number] = True # Set the value to True for the corresponding family to avoid doble counting

				### For continue counting the days for every family after symptoms onset (after the detection day)	
				index_of_fam_number = family_number_list.index(N.nodes[node]["Family"]) # Look for the index number of the family in the family number list
				# If the family is in the list of families with symptoms and the value for the family is equal to 0, then:
				if N.nodes[node]["Family"] in families_with_a_member_in_symptomatic_detection_day and families_true_list_for_counting_after_symptomatic_detection_day[index_of_fam_number] == 0:
					families_true_list_for_counting_after_symptomatic_detection_day[index_of_fam_number] = True # Change the value of the family to True to avoid double counting
					families_counting_after_symptomatic_detection_day[index_of_fam_number] += 1 # Add one day after symptoms onset (only one member in the family is contributing to this to avoid doble counting)

				# If the family is in te list of families in fragmented bubbles
				if N.nodes[node]["Family"] in families_in_fragmented_NUCLEOs and families_true_list_for_counting_days_in_home[index_of_fam_number] == 0:
					families_true_list_for_counting_days_in_home[index_of_fam_number] = True # Change the value of the family to True to avoid double counting
					families_counting_days_in_home[index_of_fam_number] += 1 # Add one day to be in home for the family
					fams_in_home_at_day += 1 # Add one family in home in a specific day 

				### To decide if the state for every node or person in the network is going to change
				### If the node is in the susceptible state
				if N.nodes[node]["State"] == S_state:
					prob_to_infect_list = [] # Empty list to append the probability to get infected from someone
					prob_to_infection_in_NUCLEO_list = [] # Empty list to append the probability to get infected from someone in the bubble
					for_edges_neighbors = [] # Empty list to append which of the neighbors infected the actual node
					### To know if the node is going to be infected from the neighbors
					for neighbor in neighbors: # For neighbor in the neighbors of the node list
						prob_to_infection_in_NUCLEO = False # The default value to get infected from the bubble is set to False
						prob_to_infect = 0 # The default value to get infected from the neighbor is set to 0
						actual_state = N.nodes[neighbor]["State"] # To find the actual state of the neighbor
						if N.nodes[node]["Type"] == "Adult": # If the current node is an adult
							if N.nodes[neighbor]["Symptomatic"] == False and N.nodes[neighbor]["State"] != S_state and N.nodes[neighbor]["State"] != R_state: # If the neighbor is (is going to be) asymptomatic
								index_in_list_states = asympt_states.index(actual_state) # Find the index of the actual state of the neighbor in the asymptomatic state list
								if N.nodes[neighbor]["Type"] == "Adult": # If the neighbor is an adult
									prob_to_infect = probabilities["Asynt Adult-Spouse"][index_in_list_states] # Set the probability for an adult to get infected from an asymptomatic adult
								elif N.nodes[neighbor]["Type"] == "Child": # If the neighbor is a child
									prob_to_infect = probabilities["Asynt Child-Adult"][index_in_list_states] # Set the probability for an adult to get infected from an asymptomatic child
							elif N.nodes[neighbor]["Symptomatic"] == True and N.nodes[neighbor]["State"] != R_state: # If the neighbor is (is going to be) symptomatic
								index_in_list_states = sympt_states.index(actual_state) # Find the index of the actual state of the neighbor in the symptomatic state list
								if N.nodes[neighbor]["Type"] == "Adult": # If the neighbor is an adult
									prob_to_infect = probabilities["Synt Adult-Spouse"][index_in_list_states] # Set the probability for an adult to get infected from a symptomatic adult
								elif N.nodes[neighbor]["Type"] == "Child": # If the neighbor is a child
									prob_to_infect = probabilities["Synt Child-Adult"][index_in_list_states] # Set the probability for an adult to get infected from a symptomatic child

						elif N.nodes[node]["Type"] == "Child": # If the node is a child
							if N.nodes[neighbor]["Symptomatic"] == False and N.nodes[neighbor]["State"] != S_state and N.nodes[neighbor]["State"] != R_state: # If the neighbor is (is going to be) asymptomatic
								index_in_list_states = asympt_states.index(actual_state) # Find the index of the actual state of the neighbor in the asymptomatic state list
								if N.nodes[neighbor]["Type"] == "Adult": # If the neighbor is an adult
									prob_to_infect = probabilities["Asynt Adult-Child"][index_in_list_states] # Set the probability for a child to get infected from an asymptomatic adult
								elif N.nodes[neighbor]["Type"] == "Child": # If the neighbor is a child
									prob_to_infect = probabilities["Asynt Child-Child"][index_in_list_states] # Set the probability for a child to get infected from an asymptomatic child
							elif N.nodes[neighbor]["Symptomatic"] == True and N.nodes[neighbor]["State"] != R_state: # If the neighbor is (is going to be) symptomatic
								index_in_list_states = sympt_states.index(actual_state) # Find the index of the actual state of the neighbor in the symptomatic state list
								if N.nodes[neighbor]["Type"] == "Adult": # If the neighbor is an adult
									prob_to_infect = probabilities["Synt Adult-Child"][index_in_list_states] # Set the probability for a child to get infected from a symptomatic adult
								elif N.nodes[neighbor]["Type"] == "Child": # If the neighbor is a child
									prob_to_infect = probabilities["Synt Child-Child"][index_in_list_states] # Set the probability for a child to get infected from a symptomatic child

						### To know the probability to get infected from someone in the bubble
						# If the neighbor is in the bubble of the node and is not a brother and is infected
						if N.edges[node,neighbor]["type"] == "NUCLEO" and N.nodes[neighbor]["Family"] != N.nodes[node]["Family"] and prob_to_infect > 0:
							prob_to_infection_in_NUCLEO = True # It is possible that the node can be infected through the bubble				
							if using_mask == True and N.nodes[neighbor]["Type"] == "Child": # If the bubble members are set to use mask and the neighbor is a child
								prob_to_infect = prob_to_infect*0.21 # The probability of infection is less (aprox. 79% less)
							if N.nodes[neighbor]["Family"] in teachers_fams_list: # If the neighbor is the teacher
								prob_to_infect = prob_to_infect*0.21 # The probability of infection is less (aprox. 79% less)

						prob_to_infect_list.append(prob_to_infect) # Append the probability to get infected from the neighbor to a list for all neighbors
						prob_to_infection_in_NUCLEO_list.append(prob_to_infection_in_NUCLEO) # Append True or 0 if it is possible or not to get infected through the bubble to a list for all neighbors
						for_edges_neighbors.append(neighbor) # To know which of the neighbors infected the actual node

					### Start counting for the Real R0 if there is an index case in the node's bubble
					if  N.nodes[node]["NUCLEO"] == True: # If the node is going to a bubble
						p = 0 # To iterate from 0
						for i in prob_to_infection_in_NUCLEO_list: # For every member in the probability to be infected through bubble list
							if prob_to_infection_in_NUCLEO_list[p] == True: # If there is an index case in the bubble
								numb_of_NUCLEO = N.nodes[node]["NUCLEO_number"] # Get the bubble number of the node 
								index_of_NUCLEO_number = list_of_NUCLEOs.index(numb_of_NUCLEO) # Find the index number of the bubble of the node
								list_of_infected_NUCLEO_real_count[index_of_NUCLEO_number] = True # To say that this bubble has an index case so it starts to count the R0
							p += 1

					### To calculate the real probability for the node to get infected from all the neighbors
					prob_to_be_infected_from_neighbors = 1 
					# The probability is defined by 1 less the product of the neighbors probabilities
					for j in prob_to_infect_list: # For all the neighbors
						prob_to_be_infected_from_neighbors = prob_to_be_infected_from_neighbors*(1-(j/100)) # Multiply all the neighbors probabilities
					prob_to_be_infected_from_neighbors = 1 - prob_to_be_infected_from_neighbors # 1 less the product of the neighbors probabilites

					### To know if the node is going to get infected
					bet_0_and_1 = random.uniform(0,1) # Look for a random number between 0 and 1 to calculate if the node is going to get infected
					if bet_0_and_1 < prob_to_be_infected_from_neighbors: # If the random number is shorter than the probability to get infected from the neighbors
						N1.nodes[node]["State"] = I_state[0] # The corresponding node in the N1 network updates to be the first element in the I_state list
						i_nodes_color.append(node) # Append to the list of I_state nodes
					
						### To decide if the node is going to be symptomatic or asymptomatic depending on a probabilty
						porb_to_be_symptomatic = random.uniform(0,1) # Random number between 0 and 1 to decide if the node is going to be symptomatic or asymtomatic
						if N.nodes[node]["Type"] == "Adult" and porb_to_be_symptomatic > 0.17: # Probability to be asymptomatic for adult
							N1.nodes[node]["Symptomatic"] = True # The corresponding node in the N1 network is going to be symptomatic
						elif N.nodes[node]["Type"] == "Child" and porb_to_be_symptomatic > 0.35: # Probability to be asymptomatic for child
							N1.nodes[node]["Symptomatic"] = True # The corresponding node in the N1 network is going to be symptomatic

						### To update the number of new and total positive cases in the network
						new_cases += 1 # Add 1 to the number of new cases for every day
						total_cases += 1 # Add 1 to the number of total infected cases

						### To know the total families that got infected
						if N.nodes[node]["Family"] not in total_fams_infected_real: # If the family is not in a list of infected families
							total_fams_infected_real.append(N.nodes[node]["Family"]) # Append the family to the list of total families infected
							families_infected_every_day.append(N.nodes[node]["Family"]) # Append the family to the list of daily families infected

						### To know if the node is infected through the bubble
						p = 0 # To count from 0
						for prob in prob_to_infect_list: # For every probability to be infected from the neighbors
							# If the probabilty is greather than the random number and the probabilty to be infected through the bubble is True
							if bet_0_and_1 < (prob/100) and prob_to_infection_in_NUCLEO_list[p] == True:  
								if N.nodes[node]["NUCLEO"] == True: # If the node is in the bubble
									### To know the total families that got infected through a bubble
									if N.nodes[node]["Family"] not in total_fams_infected_real_through_NUCLEO: # If the family is not in a list of infected families through a bubble
										total_fams_infected_real_through_NUCLEO.append(N.nodes[node]["Family"]) # Append the family to the list of total families infected through a bubble

									numb_of_NUCLEO = N.nodes[node]["NUCLEO_number"] # Get the bubble number of the node
									index_of_NUCLEO_number = list_of_NUCLEOs.index(numb_of_NUCLEO) # Find the index number of the bubble of the node
									if list_of_previous_infected_NUCLEOS_real[index_of_NUCLEO_number] == 0: # If the bubble has not been previously infected
										### To get the Real R0
										# If the family of the node is not in the list of families infected in the current bubble
										if N.nodes[node]["Family"] not in list_of_fams_in_infected_NUCLEOS_real_count[index_of_NUCLEO_number]:
											infection_in_NUCLEO_edges.append((node,for_edges_neighbors[p])) # To show the edge of the infection in the plot
											# If the bubble is infected
											if list_of_infected_NUCLEO_real_count[index_of_NUCLEO_number] == True:
												# Append the family number to the list of families infected in the actual bubble
												list_of_fams_in_infected_NUCLEOS_real_count[index_of_NUCLEO_number].append(N.nodes[node]["Family"]) # Append the family to the list of families infected in the current bubble
												new_cases_through_NUCLEOS_list_real_count[index_of_NUCLEO_number] += 1 # Add 1 to the Real R0
							p += 1 

					else: # If the node don't get infected
						s_nodes_color.append(node) # Append the node to a list to visualize the susceptible nodes 	

				### To know if the node is infected by the society
				# If the node is still in a susceptible state and is an Adult
				if N1.nodes[node]["State"] == S_state and N.nodes[node]["Type"] == "Adult": 
					prob_to_change = random.uniform(0,1) # The probability to change from susceptible to infected
					s_nodes_color.append(node)		
					if prob_to_change < probability_from_society: # Probability to get infected from the society
						N1.nodes[node]["State"] = I_state[0] # The corresponding node in the N1 network updates to be the first element in the I_state list
						i_nodes_color.append(node) # Append to the list of I_state nodes
						porb_to_be_symptomatic = random.uniform(0,1) # Random number between 0 and 1 to decide if the node is going to be symptomatic or asymtomatic
						if porb_to_be_symptomatic > 0.17: # Probability to be asymptomatic for adult
							N1.nodes[node]["Symptomatic"] = True # The corresponding node in the N1 network is going to be symptomatic
						### To update the number of new and total positive cases in the network
						new_cases += 1	# Add 1 to the number of new cases for every day
						total_cases += 1 # Add 1 to the number of total infected cases					
						### To know the total families that got infected
						if N.nodes[node]["Family"] not in total_fams_infected_real: # If the family is not in a list of infected families
							total_fams_infected_real.append(N.nodes[node]["Family"]) # Append the family to the list of total families infected		
							families_infected_every_day.append(N.nodes[node]["Family"]) # Append the family to the list of daily families infected

				# If the node is a element from the I_state, then...
				elif N.nodes[node]["State"] in I_state: 
					# If the node is the last element from th I_state, then...	
					if N.nodes[node]["State"] == I_state[-1]:	
						if N.nodes[node]["Symptomatic"] == True: # If the node is going to be symptomatic
							N1.nodes[node]["State"] = C_state[0] # The corresponding node in the N1 network updates to be the first element in the C_state (symptomatic) list
							c_nodes_color.append(node) # Append to the list of C_state nodes
						elif N.nodes[node]["Symptomatic"] == False: # If the node is going to be asymptomatic
							N1.nodes[node]["State"] = A_state[0] # The corresponding node in the N1 network updates to be the first element in the A_state (asymptomatic) list
							a_nodes_color.append(node) # Append to the list of A_state nodes

					# If the node is not the last element from th I_state, then...
					else:
						get_index = I_state.index(N.nodes[node]["State"]) # Get the index of the node in the network
						N1.nodes[node]["State"] = I_state[get_index+1] # The corresponding node in the N1 network updates to be the next element in the I_state list
						i_nodes_color.append(node) # Append to the list of I_state nodes


				# If the node is a element from the A_state, then...
				elif N.nodes[node]["State"] in A_state:
					# If the node is the last element from th A_state, then...
					if N.nodes[node]["State"] == A_state[-1]:
						N1.nodes[node]["State"] = R_state # The corresponding node in the N1 network updates to be the R_state 
						r_nodes_color.append(node) # Append to the list of R_state nodes
					# If not, then...
					else:
						get_index = A_state.index(N.nodes[node]["State"]) # Get the index of the node in the network
						N1.nodes[node]["State"] = A_state[get_index+1] # The corresponding node in the N1 network updates to be the next element in the A_state list	
						a_nodes_color.append(node) # Append to the list of A_state nodes

				# If the node is a element from the C_state, then...
				elif N.nodes[node]["State"] in C_state:
					# If the node is state is the corresponding for the detection day...
					if N.nodes[node]["State"] == C_state[symptoms_detection_day_index]: 
						total_detected_cases += 1 # Add one case to the total detected cases
					### To detect all the families with a symptomatic member every step in the model
					if N.nodes[node]["Family"] not in families_with_symptoms: # If the family of the node is not in the list of families with symptoms
						families_with_symptoms.append(N.nodes[node]["Family"]) # Append the family 
					# If the node is the last element from th C_state, then...
					if N.nodes[node]["State"] == C_state[-1]:
						N1.nodes[node]["State"] = R_state # The corresponding node in the N1 network updates to be the R_state 
						r_nodes_color.append(node) # Append to the list of R_state nodes
					# If not, then...
					else:
						get_index = C_state.index(N.nodes[node]["State"]) # Get the index of the node in the network
						N1.nodes[node]["State"] = C_state[get_index+1] # The corresponding node in the N1 network updates to be the next element in the C_state list	
						c_nodes_color.append(node) # Append to the list of C_state nodes
				# If the node is the R_state, then...
				elif N.nodes[node]["State"] == R_state:
					r_nodes_color.append(node)
		print("Step in the model number " + str(b))
		b += 1
		### The end of the iteration for all the nodes in one step of the model

		### To know all the families in home in a specific day
		fams_in_home_at_day_list.append(fams_in_home_at_day)

		### To update if a bubble is now infected for the Real R0
		new_list_of_infected_NUCLEO_real_count = list(list_of_infected_NUCLEO_real_count) # Make a new list equal to the list of real count of infection in bubbles
		t = 0 # To iterate from 0
		for NUCLEO_ in list_of_infected_NUCLEO_real_count: # For every bubble in the list of real bubbles infected
			### To update the days of infection of every bubble
			if NUCLEO_ == True or new_list_of_infected_NUCLEO_real_count[t] == True: # If the bubble is infected
				if days_of_infection_in_NUCLEO_real_count[t] < 14: # If the number of days of infection is less than 14 then,
					days_of_infection_in_NUCLEO_real_count[t] += 1 # Add a day of infection
				elif days_of_infection_in_NUCLEO_real_count[t] == 14: # If the number of days is equal to 14 then,
					days_of_infection_in_NUCLEO_real_count[t] = 0 # Reset the number of days to 0
					list_of_previous_infected_NUCLEOS_real[t] = True # Set to True to know that the bubble has been infected now
			t += 1
		list_of_infected_NUCLEO_real_count = list(new_list_of_infected_NUCLEO_real_count) # Update the list of real infected bubble

		### To reintegrate the bubbles
		t = 0 # To iterate from 0
		new_list_of_infected_NUCLEOs = list(list_of_infected_NUCLEOS_calulated) # Create a new list of the infected bubbles to make changes during iteration
		brothers_to_return_to_NUCLEO_list = [] # Empty list to append the brothers of members of an infected bubble that can return to their corresponding bubble
		for NUCLEO_ in list_of_infected_NUCLEOS_calulated: # For every bubble in the list of infected bubbles
			if NUCLEO_ == True: # If the bubble is infected (True)
				if days_of_infection_in_NUCLEO[t] < 14: # If the day after symptoms detection is less to 14
					days_of_infection_in_NUCLEO[t] += 1 # Add a new day to the counting
					### To set the families that are in an infected and fragmented bubble
					for family in to_append_to_families_in_fragmented_NUCLEOs: # For every family in a list of families to append to another list of families in fragmented bubbles
						if family in list_of_fams_for_each_NUCLEO_list[t]: # If the family is in the list of families of the actual infected bubble
							if family not in families_in_fragmented_NUCLEOs: # If the family is not already in the list of families in fragmented bubble
								families_in_fragmented_NUCLEOs.append(family) # Append the family to the list of families in fragmented bubble
				elif days_of_infection_in_NUCLEO[t] == 14: # If the day after symptoms detection is equal to 14
					days_of_infection_in_NUCLEO[t] = 0 # Reset to 0 the number of days after the symptoms detection of a bubble
					new_list_of_infected_NUCLEOs[t] = 0 # Change from True to 0 (False) the value that correspond to the bubble to say that is no more infected
					list_of_previous_infected_NUCLEOS_calculated[t] = 1 # Set to 1 to know that this bubble has been previously fragmented
					### For the bubble reintegration
					to_return_to_NUCLEO = [] # Empty list to append the families that can return to the bubble
					fams_not_returned_to_NUCLEO = [] # Empty list to append the families that cannot return tu the bubble
					if teacher == True: # If there are teachers assigned to the bubbles
						teacher_return = False # Default value to False for a teacher to return the bubble
						teachers_to_return = [] # Empty list to append the teachers that can return to the bubble
						for teacher in list_of_teachers_for_each_NUCLEO_list[t]: # For teacher in a teachers list for every bubble (if there are more than 1 teacher)
							if N.nodes[teacher]["State"] not in C_state: # If the teacher is not in the symptomatic state (no need to look for the rest of the teachers family as the teacher is the only member of the family)
								teacher_return = True # The teacher can return to the bubble  
								teachers_to_return.append(teacher) # Append the teacher to the list of teachers to return to the bubble
							else:
								teachers_to_return_later_to_NUCLEO_list[t].append(teacher) # Append the teacher to a list of teachers that will return later to the bubble
								not_complete_teachers_NUCLEO_return.append(list_of_NUCLEOs[t]) # Append to a list of bubbles that the teachers couldn't return

					for fam in list_of_fams_for_each_NUCLEO_list[t]: # For every family in the corresponding bubble
						if fam in families_with_a_member_in_symptomatic_detection_day: # If the family has a memeber with symptoms detected
							index_of_fam_number = family_number_list.index(fam) # Find the index position of the family in the families list
							# If the family has 14 or more days after symptoms onset and don't have any members with symptoms
							if families_counting_after_symptomatic_detection_day[index_of_fam_number] >= 14 and fam not in families_with_symptoms:
								families_counting_after_symptomatic_detection_day[index_of_fam_number] = 0 # Reset te counting after symptoms onset to 0 for that family
								families_with_a_member_in_symptomatic_detection_day.remove(fam) # Remove the family from the list of families with a member that presented symptoms
								if fam in families_in_fragmented_NUCLEOs:
									families_in_fragmented_NUCLEOs.remove(fam) # Remove the family from the list of families in fragmented bubbles
								to_return_to_NUCLEO.append(fam) # Append the family to the list to return to the bubble
							else: # If the family has a symptomatic member or the 14 days has not been completed
								fams_not_returned_to_NUCLEO.append(fam) # Append the family to the list to not return to the bubble
						else: # If the family doesn't have a member that was symptomatic in any moment during the bubble fragmentation
							to_return_to_NUCLEO.append(fam) # Append the family to the list to return to the bubble
							if fam in families_in_fragmented_NUCLEOs: 
								families_in_fragmented_NUCLEOs.remove(fam) # Remove the family from the list of families in fragmented bubbles

					# If the length of the list to return to bubble is not equal to the length of total families for the corresponding bubble
					if len(to_return_to_NUCLEO) != len(list_of_fams_for_each_NUCLEO_list[t]): 
						not_complete_NUCLEO_return.append(list_of_NUCLEOs[t]) # Append the bubble to a list of bubbles that not all the families returned
					# Append the list of not returned families of the corresponding bubble to a list of all the bubbles not completely returned
					fams_not_returned_to_NUCLEO_list.append(fams_not_returned_to_NUCLEO) 
					# Create a list of all the individuals that can return to the corresponding bubble and they need to be part of the families that can return to the bubble
					individuals_to_return_to_NUCLEO = [memb for memb in NUCLEOS_list_all[t] if N.nodes[memb]["Family"] in to_return_to_NUCLEO]
					if teacher == True: # If there are teachers assigned to the bubbles
						if teacher_return == True: # If there are teachers that can return to the bubble
							individuals_to_return_to_NUCLEO.extend(teachers_to_return) # Append the teachers to the list of members to return to the bubble
					set_edges = [] # Empty list to append the formed edges
					for individual in individuals_to_return_to_NUCLEO: # For every individual in the individuals list
						if individual in teachers_list: # To avoid joining the teachers together (if there are more than 1 teachers in the current bubble)
							others = [memb for memb in individuals_to_return_to_NUCLEO if memb != individual and memb not in teachers_list]
						else:
							others = [memb for memb in individuals_to_return_to_NUCLEO if memb != individual] # Look for the rest of the members of the list to make the edges
						for other in others: # For member in the rest of the members of the list
							if (individual,other) in set_edges or (other,individual) in set_edges: # If the edge individual with the other member is not in the edge list
								continue
							else:
								N1.add_edge(individual,other,type = "NUCLEO") # Set the edge between the individual and the other member
								set_edges.append((individual,other)) # Append the edge to the edge list
								color_for_NUCELO_reintegration.append((individual,other)) # Append the edge to a list to color the edges of the returning bubble
								if (individual,other) in color_for_NUCELO_edge or (other,individual) in color_for_NUCELO_edge: # If the individual and the other member are in the list of returning to the bubble
									continue
								else:
									color_for_NUCELO_edge.append((individual,other)) # If there are not in the list, append the edge to a list to color the edges of the returning bubble
						# For every individual in the bubble, make a list of all the brothers that also need to go back to their corresponding bubble
						brothers_of_individual = [memb for memb in list(N.neighbors(individual)) if N.nodes[memb]["Family"] == N.nodes[individual]["Family"] and N.nodes[memb]["NUCLEO"] == True and N.nodes[memb]["NUCLEO_number"] != N.nodes[individual]["NUCLEO_number"] and memb not in individuals_to_return_to_NUCLEO]
						brothers_to_return_to_NUCLEO_list.append(brothers_of_individual) # Append the brothers list to a general list of brothers to return to their bubble
			t += 1

		list_of_infected_NUCLEOS_calulated = list(new_list_of_infected_NUCLEOs) # Update the list of infected bubbles with the new list

		### To reintegrate the brothers in the general brothers list to their corresponding bubble
		for brothers in brothers_to_return_to_NUCLEO_list: # For the list of brothers of one child
			for brother in brothers: # For brother in the list of brothers
				brother_NUCLEO = N.nodes[brother]["NUCLEO_number"] # Find the bubble number of the corresponding brother
				if brother_NUCLEO not in list_of_infected_NUCLEOS_calulated: # If the bubble of the brother is not in the list of infected bubbles
					index_of_NUCLEO_number = list_of_NUCLEOs.index(brother_NUCLEO) # Find the index position of the bubble in the bubbles list
					rest_of_memb_in_NUCLEO = [memb for memb in NUCLEOS_list_all[index_of_NUCLEO_number] if memb != brother and N.nodes[memb]["Family"] not in families_with_symptoms] # Look for the rest of the members in the bubble to make the edges
					set_edges = [] # Empty list to append the formed edges
					for memb in rest_of_memb_in_NUCLEO: # For member in the rest of the members of the list
						if (brother,memb) in set_edges or (memb,brother) in set_edges: # If the edge individual with the other member is not in the edge list
							continue
						else:
							N1.add_edge(brother,memb,type = "NUCLEO") # Set the edge between the brother and the other member
							set_edges.append((brother,memb)) # Append the edge to the edge list
							color_for_brothers_reintegration.append((brother,memb)) # Append the edge to a list to color the edges of the returning bubble
							if (brother,memb) in color_for_NUCELO_edge or (memb,brother) in color_for_NUCELO_edge: # If the individual and the other member are in the list of returning to the bubble
								continue
							else:
								color_for_NUCELO_edge.append((brother,memb)) # If there are not in the list, append the edge to a list to color the edges of the returning bubble


		### To reintegrate the families that didn't return to the bubble in the first time
		new_list_not_complete_NUCLEO_return = list(not_complete_NUCLEO_return) # To generate a copy of the list of bubbles were families didn't return (to avoid modifying the original)
		new_list_fams_not_returned_to_NUCLEO_list = list(fams_not_returned_to_NUCLEO_list) # To generate a copy of the list of families not returned to the bubbles (to avoid modifying the original)
		t = 0
		### For every bubble in the list of not completely returned bubbles
		for NUCLEO_ in not_complete_NUCLEO_return:
			to_return_to_NUCLEO = [] # To append te families to return to the bubble
			for fam in fams_not_returned_to_NUCLEO_list[t]: # For family in the list of families not returned for the current bubble
				index_of_fam_number = family_number_list.index(fam) # Find the index position of the family in the families list
				# If the family has 14 or more days after symptoms onset and don't have any members with symptoms
				if families_counting_after_symptomatic_detection_day[index_of_fam_number] >= 14 and fam not in families_with_symptoms:
					families_counting_after_symptomatic_detection_day[index_of_fam_number] = 0 # Reset te counting after symptoms onset to 0 for that family
					families_with_a_member_in_symptomatic_detection_day.remove(fam) # Remove the family from the list of families with a member that presented symptoms
					if fam in families_in_fragmented_NUCLEOs:
						families_in_fragmented_NUCLEOs.remove(fam) # Remove the family from the list of families in fragmented bubbles
					to_return_to_NUCLEO.append(fam) # Append the family to the list to return to the bubble
					new_list_fams_not_returned_to_NUCLEO_list[t].remove(fam) # Remove from the list of families that haven't returned to the bubble

			index_of_NUCLEO_number = list_of_NUCLEOs.index(NUCLEO_) # Find the index position of the bubble in the bubbles list
			# Create a list of all the individuals that can return to the corresponding bubble and they need to be part of the families that can return to the bubble
			individuals_to_return_to_NUCLEO = [memb for memb in NUCLEOS_list_all[index_of_NUCLEO_number] if N.nodes[memb]["Family"] in to_return_to_NUCLEO]
			# Create a list of the rest of the members of the bubble
			rest_of_memb_in_NUCLEO = [memb for memb in NUCLEOS_list_all[index_of_NUCLEO_number] if N.nodes[memb]["Family"] not in to_return_to_NUCLEO and N.nodes[memb]["Family"] not in families_with_symptoms]
			set_edges = [] # Empty list to append the formed edges
			for individual in individuals_to_return_to_NUCLEO: # For every individual in the individuals list
				others = [memb for memb in individuals_to_return_to_NUCLEO if memb != individual and memb not in teachers_list] # Look for the rest of the members of the list to return to make the edges
				others.extend(rest_of_memb_in_NUCLEO) # Extend the list to all the current members in the bubble
				for other in others: # For member in the rest of the members of the list
					if (individual,other) in set_edges or (other,individual) in set_edges: # If the edge individual with the other member is not in the edge list
						continue
					else:
						N1.add_edge(individual,other,type = "NUCLEO") # Set the edge between the individual and the other member
						set_edges.append((individual,other)) # Append the edge to the edge list
						color_for_NUCELO_reintegration.append((individual,other)) # Append the edge to a list to color the edges of the returning bubble
						if (individual,other) in color_for_NUCELO_edge or (other,individual) in color_for_NUCELO_edge: # If the individual and the other member are in the list of returning to the bubble
							continue
						else:
							color_for_NUCELO_edge.append((individual,other)) # If there are not in the list, append the edge to a list to color the edges of the returning bubble

				### To reintegrate the brothers in the general brothers list to their corresponding bubble
				# To find the brothers of the child just returned to the bubble
				brothers_of_individual = [memb for memb in list(N.neighbors(individual)) if N.nodes[memb]["Family"] == N.nodes[individual]["Family"] and N.nodes[memb]["NUCLEO"] == True and N.nodes[memb]["NUCLEO_number"] != N.nodes[individual]["NUCLEO_number"]]
				for brother in brothers_of_individual: # For the list of brothers of one child
					brother_NUCLEO = N.nodes[brother]["NUCLEO_number"] # Find the bubble number of the corresponding brother
					if brother_NUCLEO not in list_of_infected_NUCLEOS_calulated: # If the bubble of the brother is not in the list of infected bubbles
						index_of_NUCLEO_number_brother = list_of_NUCLEOs.index(brother_NUCLEO) # Find the index position of the bubble in the bubbles list
						# Look for the rest of the members in the bubble to make the edges
						rest_of_memb_in_NUCLEO = [memb for memb in NUCLEOS_list_all[index_of_NUCLEO_number_brother] if memb != brother and N.nodes[memb]["Family"] not in families_with_symptoms]
						set_edges_brother = [] # Empty list to append the formed edges
						for memb in rest_of_memb_in_NUCLEO: # For member in the rest of the members of the list
							if (brother,memb) in set_edges_brother or (memb,brother) in set_edges_brother: # If the edge individual with the other member is not in the edge list
								continue
							else:
								N1.add_edge(brother,memb,type = "NUCLEO") # Set the edge between the brother and the other member
								set_edges_brother.append((brother,memb)) # Append the edge to the edge list
								color_for_NUCELO_reintegration.append((brother,memb)) # Append the edge to a list to color the edges of the returning bubble
							if (brother,memb) in color_for_NUCELO_edge or (memb,brother) in color_for_NUCELO_edge: # If the individual and the other member are in the list of returning to the bubble
								continue
							else:
								color_for_NUCELO_edge.append((brother,memb)) # If there are not in the list, append the edge to a list to color the edges of the returning bubble
			# If there are no families left to return to the bubble, remove all the families in the list to return for the current bubble
			if len(new_list_fams_not_returned_to_NUCLEO_list[t]) == 0:
				new_list_not_complete_NUCLEO_return.remove(NUCLEO_) 

			t += 1

		# Update the list of bubbles to return
		not_complete_NUCLEO_return = list(new_list_not_complete_NUCLEO_return)
		# Update the list of families in the bubbles to return
		fams_not_returned_to_NUCLEO_list = [memb for memb in new_list_fams_not_returned_to_NUCLEO_list if len(memb)!= 0]

		# For all the bubbles in the list of bubbles with not all the teachers returned
		if teacher == True: # If there are teachers assigned to the bubbles
			for NUCLEO_ in not_complete_teachers_NUCLEO_return:
				index_of_NUCLEO_number = list_of_NUCLEOs.index(NUCLEO_) # Find the index position of the teacher in the teachers list
				teacher_return = False # Default value to False for a teacher to return the bubble
				teachers_to_return = [] # Empty list to append the teachers that can return to the bubble
				for teacher in teachers_to_return_later_to_NUCLEO_list[index_of_NUCLEO_number]: # For teacher in a teachers list to return later for every bubble
					if N.nodes[teacher]["State"] not in C_state: # If the teacher is not in the symptomatic state (no need to look for the rest of the teachers family as the teacher is the only member of the family)
						teacher_return = True # The teacher can return to the bubble 
						teachers_to_return.append(teacher) # Append the teacher to the list of teachers to return to the bubble
						teachers_to_return_later_to_NUCLEO_list[index_of_NUCLEO_number].remove(teacher) # Remove the teacher from the list to return later

				if teacher_return == True: # If there are teachers that can return to the bubble
					individuals_to_return_to_NUCLEO = teachers_to_return # all the individuals to return are the selected teachers
					# Create a list of the rest of the members of the bubble avoiding adding other teachers
					rest_of_memb_in_NUCLEO = [memb for memb in NUCLEOS_list_all[index_of_NUCLEO_number] if N.nodes[memb]["Family"] not in to_return_to_NUCLEO and N.nodes[memb]["Family"] not in families_with_symptoms and memb not in teachers_list]
					set_edges = [] # Empty list to append the formed edges
					for individual in individuals_to_return_to_NUCLEO: # For every individual in the individuals list
						others = [memb for memb in individuals_to_return_to_NUCLEO if memb != individual] # Look for the rest of the members of the list to make the edges
						others.extend(rest_of_memb_in_NUCLEO) # Extend the list to all the members in the current bubble
						for other in others: # For member in the rest of the members of the list
							if (individual,other) in set_edges or (other,individual) in set_edges: # If the edge individual with the other member is not in the edge list
								continue
							else:
								N1.add_edge(individual,other,type = "NUCLEO") # Set the edge between the individual and the other member
								set_edges.append((individual,other)) # Append the edge to the edge list
								color_for_NUCELO_reintegration.append((individual,other)) # Append the edge to a list to color the edges of the returning bubble
								if (individual,other) in color_for_NUCELO_edge or (other,individual) in color_for_NUCELO_edge: # If the individual and the other member are in the list of returning to the bubble
									continue
								else:
									color_for_NUCELO_edge.append((individual,other)) # If there are not in the list, append the edge to a list to color the edges of the returning bubble

		### Update the network to the next step
		N = nx.Graph(N1)

		### Append the new cases to a list of new cases every day (corresponding to the current day)
		new_cases_list.append(new_cases)

		### Append the new families infected to a list of families infected every day (corresponding to the current day)
		families_infected_every_day_list.append(families_infected_every_day)

		### For plotting the Graph
		# To defin the adult and the children nodes
		adult_s_node_color = [node for node in s_nodes_color if node in adult_nodes] # Adults in the S state
		s_nodes_color = [node for node in s_nodes_color if node not in adult_nodes] # Children in the S state
		adult_i_node_color = [node for node in i_nodes_color if node in adult_nodes] # Adults in the I state
		i_nodes_color = [node for node in i_nodes_color if node not in adult_nodes] # Children in the I state
		adult_a_node_color = [node for node in a_nodes_color if node in adult_nodes] # Adults in the A state
		a_nodes_color = [node for node in a_nodes_color if node not in adult_nodes] # Children in the A state
		adult_c_node_color = [node for node in c_nodes_color if node in adult_nodes] # Adults in the C state
		c_nodes_color = [node for node in c_nodes_color if node not in adult_nodes] # Children in the C state
		adult_r_node_color = [node for node in r_nodes_color if node in adult_nodes] # Adults in the R state
		r_nodes_color = [node for node in r_nodes_color if node not in adult_nodes] # Children in the R state

		### To plot the nodes and the edges in the Graph
		nx.draw_networkx_nodes(N,pos,nodelist=s_nodes_color, node_color="#87CEFA",node_size=400, node_shape="o") # Children in the S state
		nx.draw_networkx_nodes(N,pos,nodelist=adult_s_node_color, node_color="#87CEFA",node_size=500, node_shape="v") # Adults in the S state
		nx.draw_networkx_nodes(N,pos,nodelist=i_nodes_color, node_color="#CDAD00",node_size=400, node_shape="o") # Children in the I state
		nx.draw_networkx_nodes(N,pos,nodelist=adult_i_node_color, node_color="#CDAD00",node_size=500, node_shape="v") # Adults in the I state
		nx.draw_networkx_nodes(N,pos,nodelist=a_nodes_color, node_color="#EE7600",node_size=400, node_shape="o") # Children in the A state
		nx.draw_networkx_nodes(N,pos,nodelist=adult_a_node_color, node_color="#EE7600",node_size=500, node_shape="v") # Adults in the A state	
		nx.draw_networkx_nodes(N,pos,nodelist=c_nodes_color, node_color="#B22222",node_size=400, node_shape="o") # Children in the C state
		nx.draw_networkx_nodes(N,pos,nodelist=adult_c_node_color, node_color="#B22222",node_size=500, node_shape="v") # Adults in the C state
		nx.draw_networkx_nodes(N,pos,nodelist=r_nodes_color, node_color="#228B22",node_size=400, node_shape="o") # Children in the R state
		nx.draw_networkx_nodes(N,pos,nodelist=adult_r_node_color, node_color="#228B22",node_size=500, node_shape="v") # Adults in the R state
		nx.draw_networkx_nodes(N,pos,nodelist=[0],node_color="darkgray",node_size=1000, node_shape="*") # Society node
		nx.draw_networkx_edges(N,pos,edgelist=color_adult_society, edge_color="dodgerblue", width=2) # Edges from society to adults
		nx.draw_networkx_edges(N,pos,edgelist=color_family_edge,edge_color="#545454", width=2) # Edges within families
		nx.draw_networkx_edges(N,pos,edgelist=color_for_NUCELO_edge,edge_color="black", width=5) # Edges within the bubbles
		nx.draw_networkx_edges(N,pos,edgelist=infection_in_NUCLEO_edges,edge_color="red", width=2) # Edge of infection through a bubble
		plt.axis('off') # Don't show axes
		plt.show() # Plot the Graph

	# List to append the Estimated and the Real bubble_R0 of all the bubbles with symptomatic or infected cases respectively
	r_through_NUCLEO_calculated = [] # To append the number of cases from a single index case in every bubble (detected with symptoms)
	r_through_NUCLEO_real_count = [] # To append the number of cases from a single index case in every bubble (detecting the infection onset or total real cases including asymptomatic)
	
	# To append the Estimated and the Real R0
	t = 0
	for i in list_of_previous_infected_NUCLEOS_real:
		if i == True: # If the bubbles completed 14 days after the first infected case
			r_through_NUCLEO_real_count.append(new_cases_through_NUCLEOS_list_real_count[t]) # Append the Real_R0 of the corresponding bubble

		if list_of_previous_infected_NUCLEOS_calculated[t] == True: # If the bubbles completed 14 days after the first symptomatic case
			r_through_NUCLEO_calculated.append(new_cases_through_NUCLEOS_list_calculated[t]) # Append the Estimated_R0 of the corresponding bubble
		t += 1
	# Return data for storing and furter analysis
	return r_through_NUCLEO_calculated, r_through_NUCLEO_real_count, new_cases_list, total_detected_cases, total_cases, families_infected_every_day_list, total_fams_infected_real, total_fams_infected_real_through_NUCLEO, new_cases_through_NUCLEOS_list_calculated, new_cases_through_NUCLEOS_list_real_count, families_counting_days_in_home, fams_in_home_at_day_list