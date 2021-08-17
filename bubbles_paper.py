###NUCLEOS###

### Authors: Luis Manuel Muñoz Nava and Marcos Nahmad

### Save the bubbles_function file in the same folder

from bubbles_functions import *

########### Variables in the model #################


### Define the possible states for the individuals (nodes)
S_state = "S" # Susceptible state
I_state = ["I1","I2","I3","I4","I5"] # Infected state in a presymptomatic stage
A_state = ["A1","A2","A3","A4","A5","A6","A7","A8","A9"] # Infected and asymptomatic
C_state = ["C1","C2","C3","C4","C5","C6","C7","C8","C9"] # Infected and symptomatic 
R_state = "R" # Recovered state

### A list with all the states in an asymptomatic individual
all_infected_states_together_asymptomatic = ["I1","I2","I3","I4","I5","A1","A2","A3","A4","A5","A6","A7","A8","A9"]

### A list with all the states in a symptomatic individual
all_infected_states_together_symptomatic = ["I1","I2","I3","I4","I5","C1","C2","C3","C4","C5","C6","C7","C8","C9"]

### Day during infection to detect symptoms (only symptomatic) 
symptoms_detection_day_list = ["C1", "C2", "C3"]

### Set the symptoms detection day (defalut in C1)
symptoms_detection_day = symptoms_detection_day_list[0]
symptoms_detection_day_index = C_state.index(symptoms_detection_day) # Obtain the index of the symptoms detection day in the C state list 

### Define the number of families (default 10)
num_fam = 10

### How many members are in the families (deafult 5)
fam_memb_num = 5

### Define the possible members number per NÚCLEO

possible_memb_in_NUCLEO_k_value_list = [1,4,6,8,20]
## To run the simulation without NUCLEOs, set the value to 1
# To run just one possible k, uncomment the next line and put the k you want (default 4)
# possible_memb_in_NUCLEO_k_value_list = [4] 

### Set the probability for an adult to get infected from the society in every step of the model (default "high")
probability_from_society_list = {"very high":0.005, "high":0.001, "moderate/high":0.0005}
probability_from_society = probability_from_society_list["high"]

### Define the total steps (days) in the model (default 90)
steps_in_the_model = 90

### Define the number of iterations (default 1), we used 500 for the analysis
num_iteration = 1

### Import a data frame with the values of the proabilities to get infected from the people in the household or in a NUCLEO, depending on the viral shedding.  
## You need to read a csv file with the probabilities as shown in the supplementary material
#prob_to_get_infected_df = pd.read_csv("the_path_to_the_file/the_file.csv")

### To say the model if the NUCLEOs are going to be fragmented or not (False = to not get fragmented, default = True)
intervention = True

### To set if there will be teachers in the bubbles (defalut False), 
# If you set this to True, you need to put 1 or more teachers in the num_teachers to avoid errors
# If you set this to False, you need to put 0 in the num_teachers to avoid errors
teacher = False

### To set the number of teachers in the bubbles (default 0)
num_teachers = 0

############## TO RUN THE MODEL #################

### Create a list with all the families in the school
total_population_type, child_in_NUC_list = population_type(num_fam,fam_memb_num)

# If you want to use the same settings for the network for different simulations you can save the data  
# #dict_to_save = {"total_population_type":total_population_type, "fam_num_list":fam_num_list, "child_in_NUC_list":child_in_NUC_list, "nodes_num":nodes_num, "adult_nodes":adult_nodes, "children_in_NUCLEOs_program":children_in_NUCLEOs_program, "color_family_edge":color_family_edge, "color_adult_society":color_adult_society, "family_number_list":family_number_list}
# dict_to_save = {"total_population_type":total_population_type, "fam_num_list":fam_num_list, "child_in_NUC_list":child_in_NUC_list}
# to_save_file = open("path_to_save_file/file.pkl","wb")
# pickle.dump(dict_to_save, to_save_file)
# to_save_file.close()

### Open the file and avoid using the population_type fucntion to have the same setting for multiple simulations

# to_open_file = open("path_of_saved_file/file_saved.pkl","rb")
# the_file = pickle.load(to_open_file)
# total_population_type, fam_num_list, child_in_NUC_list = the_file["total_population_type"], the_file["fam_num_list"], the_file["child_in_NUC_list"]

### Create the network for all the population
N, nodes_num, adult_nodes, children_in_NUCLEOs_program, color_family_edge, color_adult_society, family_number_list = create_the_family_network(num_fam, fam_memb_num, total_population_type, child_in_NUC_list)

### Define if the children in the NUCLEO use mask False = not using, True = using (default both)
using_mask = [False,True]



### To run the simulation for every k
for k in possible_memb_in_NUCLEO_k_value_list:
	### To run the simultaion whether the children are using mask or not in the bubble
	for mask in using_mask:

		### Some lists to store information from the simulations
		r_0_list_calculated = [] # Estimated_R0 
		r_0_list_real = [] # Real_R0
		new_cases_list_list = [] # New cases for every day in the simulations
		new_cases_through_NUCLEOS_list_calculated_list = [] # Estimated new cases through the bubbles
		new_cases_through_NUCLEOS_list_real_count_list = [] # Real new cases through the bubbles
		children_not_in_NUCLEO_day_list_list = [] # Children not attending to a bubble for every day
		total_children_in_NUCLEO_list = [] # Total children in the Bubbles program
		total_cases_list = [] # Total cases in the simulations
		families_counting_days_in_home_list = [] # Days of isolation for the families (not attending to a bubble)
		families_infected_every_day_list_list = [] # Families infected for every day
		total_fams_infected_list = [] # Total families infected 
		total_fams_infected_list_through_NUCLEO = [] # Total families infected through the bubbbles
		total_detected_cases_list = [] # Total detected or symptomatic cases
		fams_in_home_at_day_list_list = [] # Families not attending to a bubble for every day

		### Iterate over a set number of times to know the dynamics of the virus within the population
		p = 1
		for i in range(num_iteration):
			### Create the bubbles for all the families in the school
			N_1, adult_nodes_copy, color_adult_society_copy, color_family_edge_copy, NUCLEOS_list_all, color_NUCLEO_edge_list, list_of_NUCLEOs,list_of_fams_for_each_NUCLEO_list,fams_not_in_NUCLEOs, teachers_list, list_of_teachers_for_each_NUCLEO_list, teachers_fams_list = assign_NUCLEOS(N, nodes_num, adult_nodes, children_in_NUCLEOs_program, k, color_family_edge, color_adult_society, teacher, family_number_list, num_teachers)
			### Iterate the defined number of steps over the network to obtain the data
			r_through_NUCLEO_calculated, r_through_NUCLEO_real_count, new_cases_list, total_detected_cases, total_cases, families_infected_every_day_list, total_fams_infected_real, total_fams_infected_real_through_NUCLEO, new_cases_through_NUCLEOS_list_calculated, new_cases_through_NUCLEOS_list_real_count, families_counting_days_in_home, fams_in_home_at_day_list = iterate_the_network(N_1,steps_in_the_model,S_state,I_state,A_state,C_state,R_state, symptoms_detection_day_index, nodes_num, family_number_list, child_in_NUC_list, NUCLEOS_list_all, adult_nodes_copy, color_family_edge_copy, color_adult_society_copy, color_NUCLEO_edge_list, prob_to_get_infected_df, all_infected_states_together_asymptomatic, all_infected_states_together_symptomatic, mask, list_of_NUCLEOs, probability_from_society, list_of_fams_for_each_NUCLEO_list, fams_not_in_NUCLEOs, intervention, teacher,teachers_list, list_of_teachers_for_each_NUCLEO_list, teachers_fams_list)
			# Append the obteined values to the list for every simulation
			r_0_list_calculated.append(r_through_NUCLEO_calculated)
			r_0_list_real.append(r_through_NUCLEO_real_count)
			new_cases_list_list.append(new_cases_list)
			total_detected_cases_list.append(total_detected_cases)
			total_cases_list.append(total_cases)
			families_infected_every_day_list_list.append(families_infected_every_day_list)
			total_fams_infected_list.append(len(total_fams_infected_real))
			total_fams_infected_list_through_NUCLEO.append(len(total_fams_infected_real_through_NUCLEO))
			families_counting_days_in_home_list.append(families_counting_days_in_home)
			new_cases_through_NUCLEOS_list_calculated_list.append(new_cases_through_NUCLEOS_list_calculated)
			new_cases_through_NUCLEOS_list_real_count_list.append(new_cases_through_NUCLEOS_list_real_count)
			fams_in_home_at_day_list_list.append(fams_in_home_at_day_list)

			print("Simulation number " + str(p))
			p += 1

		### Store the generated data in files (uncomment the next lines)
		# dict_results = {"Estimated R0":r_0_list_calculated, "Measured R0":r_0_list_real, "New cases through NUCLEO":new_cases_through_NUCLEOS_list_calculated_list, "New cases through NUCLEO real":new_cases_through_NUCLEOS_list_real_count_list,"New cases":new_cases_list_list, "Total detected cases":total_detected_cases_list, "Total cases":total_cases_list, "New infected families":families_infected_every_day_list_list, "Total families infected":total_fams_infected_list, "Total families infected through NUCLEO":total_fams_infected_list_through_NUCLEO, "Days in home per fam":families_counting_days_in_home_list, "Number of fams in home every day":fams_in_home_at_day_list_list}
		# df_results = pd.DataFrame(dict_results)
		# pd.DataFrame.to_csv(df_results,"path_of_the_folder_to_save"+"df_results_NUCLEOS_prob_from_society_"+str(probability_from_society)+"_symptoms_detection_day_"+symptoms_detection_day+"_using_mask_"+str(mask)+"_k_of_"+str(k)+".csv")

		# dict_info_NUCLEOs = {"List of NUCLEOs":[list_of_NUCLEOs], "Children in NUCLEOS per family":[child_in_NUC_list], "List of members of NUCLEOs":[NUCLEOS_list_all], "Families not in NUCLEOs":[fams_not_in_NUCLEOs]}
		# df_info_NUCLEOs = pd.DataFrame(dict_info_NUCLEOs)
		# pd.DataFrame.to_csv(df_info_NUCLEOs,"path_of_the_folder_to_save"+"df_info_NUCLEOS_prob_from_society_"+str(probability_from_society)+"_symptoms_detection_day_"+symptoms_detection_day+"_using_mask_"+str(mask)+"_k_of_"+str(k)+".csv")
