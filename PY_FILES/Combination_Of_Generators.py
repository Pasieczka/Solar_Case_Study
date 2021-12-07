#OPTIMIZATION COST FOR ONLY GENERATORs
#Code adapted from: https://www.geeksforgeeks.org/combinations-with-repetitions/
#This function shows the fuel consumption rate of "n" generators.
#The output will show the total fuel rate for n generators, follwed by each individual generator fuel rate

#Combination code for generator
import numpy
import matplotlib.pyplot as plt
import openpyxl


#Cost of fuel
fuel_cost = 3.380

#Fuel consumption rate (US gph)
#100_rate = 10.81
# 75_rate = 8.77
# 50_rate = 6.32
# 25_rate = 3.88


#Driver code
arr = [ 135, 101.25, 67.5, 33.75 ]
generator = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12] #possible generator trials
n = len(arr) - 1
trial = {}
#trial2 = {}

#setting up spreadsheet to work on
wb = openpyxl.Workbook()
sheet = wb.active
excel_row = 0


def CombinationRepetitionUtil(chosen, arr, index, r, start, end, cost_model, excel_row, trial2):
    
    
    running_sum = 0
    
    
    if index == r:
        trial_cost = 1
        for j in range(r):
           
            running_sum = running_sum + chosen[j]
            chosen_sum = (sum(chosen))
          
           
                
            if chosen[j] == 135:
                trial_cost = trial_cost + (10.81)
            if chosen[j] == 101.25:
                trial_cost = trial_cost + (8.77)
            if chosen[j] == 67.5:
                trial_cost = trial_cost + (6.32)
            if chosen[j] == 33.75:
                trial_cost = trial_cost + (3.88)    
            if chosen_sum >= 376.1: 
                trial[chosen_sum] = str(chosen)# if chosen_sum >= 376.1:
            #     cost_model = cost_model[j].append()
                trial2.update({trial_cost : chosen[j:]})
      
   
        chosen_sum = 0
        return 

    # When there are no more elements for chosen[]
    if start > n:
        return 
         
   
    chosen[index] = arr[start]
     
    # Current value is excluded, we replace it with the next one
    CombinationRepetitionUtil(chosen, arr, index + 1, r, start, end, cost_model, excel_row, trial2)
    CombinationRepetitionUtil(chosen, arr, index, r, start + 1, end, cost_model, excel_row, trial2)
 
# The main function that prints all combinations of the generators
def CombinationRepetition(arr, n, r):
    
    cost_model = []
    plt = 0
    excel_row = 1
    trial2 ={}
    
    chosen = [0] * r
 
    
    CombinationRepetitionUtil(chosen, arr, 0, r, 0, n, cost_model, excel_row, trial2)
    
    spreadsheet = wb.save('Generator_Cost.csv')
   
    print(min(trial2.items()))



for gen in generator:
    CombinationRepetition(arr, n, gen, )