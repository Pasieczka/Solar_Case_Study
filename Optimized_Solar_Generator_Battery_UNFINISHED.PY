#This script is not complete. It was the beginning stages of optimizing batteries, solar panels, and generators. 
#It would account for the fluctuating costs of the variables as well as different rates of fuel consumption.

#HYBRID APPROACH
import numpy as np
from numpy import matrix
from scipy.optimize import minimize
import math



#CONSTNATS

#Battery Specs
battery_capacity = 13.5     #kWh
battery_cost = 8500         #$
battery_maintenance = 50    #$/year
battery_dc_voltage = 50     #V



#Solar Panel Specs
panel_cost = 220            #$
panel_maintenance = 10      #$/year
panel_wattage = 0.425         #kW
efficiency = 0.90

#Inverter Specs
inverter_cost = 0           #$ #set to zero because battery: Tesla Powerwall 2 has inverter combined. 
inverter_maintenance = 0    #$/year

#Charge Controller Specs
controller_cost =15         #$
controller_maintenance = 5    #$/year #accounts for having to replace controllers
controller_amperage = 30 



#BUFFER
buffer = 1.2255 #Use this buffer to play around with what level of factor you want for the array
#peak load is 376.1 kW (from Nov 20th @ 19:00) / 306.875 (daily average from peak day) = 1.2255

#DATA
#Load data from January 30th 1990 (kW)
load_data = [278.4 ,276.2, 274.1, 271, 269.3, 279.7, 311.8, 299.3, 302.3, 313.2, 321.3, 322.5, 345, 336.7, 329.1, 325.5, 315.9, 318.3, 328.1, 364.6, 339.9, 315.6, 308.1, 288.1]
load_data = [element * buffer for element in load_data]

#Solar Data from June 9th 2014 (hourly average)
solar_data = [0, 0, 0, 0, 0 , 0.675, 2.883333333, 5.2, 6.966666667, 9.35, 10.775, 10.50833333, 9.366666667, 7.1, 3.95, 1.108333333, 0, 0, 0, 0, 0, 0, 0, 0] #June 9th

    
    
def cost_of_item(num_of_item, price_per_item):
    cost = num_of_item * price_per_item 
    return cost
    
       

def whole_number(battery_count):
    battery_count_int = battery_count.is_integer()
    if (battery_count_int) == False:
        battery_count += 1
        battery_count = math.trunc(battery_count)
    return battery_count


def avaliable_solar(): 

    #ARBITRARY COSTS 
    gen_power_cost = 0.22 #$/kWh
    solar_power_cost = 0.15 #$/kWh
    battery_power_cost = 0.31 #$/kWh
    lowest_method = {}
    lowest_cost = 1000000000 #arbitary high starting point to compare if cost is lower than this
    
    
    #The idea is that we will hold one variable constant and compare the other two. 
    #We know the maximum number of solar panels for supplying the entire load from "Solar_Cost.py" script earlier.
    #This way we can set our max bounds and iterate as we get close and closer to zero. 
    #We are then able to store the lowest cost from each iteration and compare that in a list, array, or dictionary.
    
    for i in range(3425,0,-25): #3425 is maximum number of solar panels to power grid
    
        for j in range(400,0,-5):   #400 = maximum batteries required to supply power

            #j panels produces m watts. 
            solar_trial =  ((j * panel_wattage) / solar_data[10])
            solar_data_multiplied = [element * solar_trial for element in solar_data]
            solar_data_trial_sum = sum(solar_data_multiplied) #this is how much energy the array will produce on that day with the number of panels we have
            
            #print("THIS ONE")
            #print(solar_data_trial_sum)
            #print(sum(load_data))
            #m watts/ solar_data[11] = multiplier 
            #This means how large our arry is 

            # if solar_data_trial_sum < sum(load_data): 
            #     gen_power = ((sum(load_data)) - sum(solar_data_multiplied) ) #This is the energy required by the generator to meet the current needs
            
            #Setting counter values
            battery_level = 0
            gen_power_day = 0
            solar_power_day = 0
            battery_power_day = 0
            
            
            
            
            #run through each entry and compare the hour in the list. This is how we can determine cost 
            for h in range(1,24): #step through each hour of the day
                hour_energy = load_data[h]
               
                
                if solar_data[h] > hour_energy: #determine the battery level if there is excess energy being produced
                    battery_level += (solar_data[h] - hour_energy[h])
                    battery_power_day += battery_level
                    
                #if not enough solar is being produced, try take energy from battery first
                if solar_data[h] <= hour_energy and battery_level > 0: 
                        energy_remaining = (max((hour_energy - battery_level), 0)) #gets the remaining energy in the battery but stops at zero
                        
                #if not enough sun is being produced and there is no more energy in the battery, turn on the generator  
                elif solar_data[h] <= hour_energy and battery_level <= 0: 
                    gen_power = (max((hour_energy - battery_level), 0))
                    
                    #remaining power gets supplied by generator
                    gen_power = (load_data[h] - solar_data_multiplied[h])
                    gen_power_day += gen_power
                    
                else:
                    battery_level += solar_data[h]

                power_day_cost = (gen_power_day * gen_power_cost) + (solar_power_day * solar_power_cost) + (battery_power_day * battery_power_cost)
                if power_day_cost < lowest_cost: 
                    #lowest_method[gen_power_day_cost] = {gen_power, battery_level, j}
                    #lowest_method.update({power_day_cost : (gen_power, battery_level, j)})
                    lowest_method.update({(gen_power, battery_level, j) : power_day_cost})
                
                    
    print("lowest day production")
    print((lowest_method))
    print(lowest_cost)
    
    print("best key = lowest cost production per hour")
    best_key = min(lowest_method, key = lowest_method.get)
    print(best_key)
    #print(best_key[])
     #print(min(lowest_method[0]))
    # a_dictionary.update({"a": 0, "c": 3})

                        
                   
                        
               # gen_power_amount = gen_power * 
                #Could calculate the cost for one hour of production. Then add that up to make the cost for a day. 
                #cost to produce generator power
                
                #get cost of each generator, solar panels, battery
                #add up cost
                #check if cost is less than existing lowest cost. 
                #if it is lower, add 
            
       


#make an equation that if battery is greater than 13.5, add another battery, reset +=battery_num
def main():
    
    
    avaliable_solar()
    #load = avaliable_solar(x) * array_size(y) * battery_num(z)
    
    return

if __name__ == "__main__":
    main()