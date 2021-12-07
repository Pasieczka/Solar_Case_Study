#This function analyzes the cost of implement just a solar array with battery for the entire load


#COST OF SOLAR

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

        
    lowest_value = 1000 #arbitary high starting point
    for j in range(200, 5, -1): #iterating to make solar data closer to load data
        solar_data_multiplied = [element * j for element in solar_data]
        #print(solar_data_multiplied)
        
        #This is where it gets real
        if sum(solar_data_multiplied) >= sum(load_data):
            #print("Equal")
            #print(j)
            lowest_value = j
            lowest_solar_value = (solar_data_multiplied)
            
            #print("Difference between matrix")
            #print(difference)
    
    #print(lowest_solar_value)
    print("Total load to accomiate for is: " + str('{0:.6g}'.format(sum(load_data))) + (" kW"))
    print("The multiplying factor of the solar data is " + str(lowest_value))
    print()
    
    #finding how much battery storage will be required
    solar_data_lowest_value = [element * lowest_value for element in solar_data]
    load_data_matrix = np.array(load_data)
    solar_data_matrix = np.array(solar_data_lowest_value)
    difference = load_data_matrix - solar_data_lowest_value

    
    #Finding battery storage
    battery_storage = 0
    for entry in difference:
        if entry < 0:
            battery_storage += entry
    battery_storage = abs(battery_storage)
    print("Battery storage required: " + str('{0:.6g}'.format(battery_storage)) + ("kW"))
        
    
    #Number of batteries
    battery_count = ((battery_storage / battery_capacity))
    battery_count = whole_number(battery_count)
    print("Number of batteries required: " + str('{0:.5g}'.format(battery_count)))

        
    #Number of Solar Panels
    pv_array = ((lowest_solar_value[10])) #Maximum kW required to be output at a given hour
    panel_count = pv_array / panel_wattage
    panel_count = whole_number(panel_count)
    print("Number of solar panels required: " + str('{0:.5g}'.format(panel_count)))
    
    #Number of Inverters
    #print("size inverter based off average hourly production : " + str((sum(load_data))/24))
    inverter_count = 0
    print("Number of inverters required: " + str('{0:.5g}'.format(inverter_count)))
    
    #Number of controllers
    controller_size = ((panel_count * (panel_wattage * 1000)) / battery_dc_voltage) #amp
    controller_count = controller_size / (controller_amperage)
    controller_count = whole_number(controller_count)
    print("Number of controllers required: " + str('{0:.5g}'.format(controller_count)))


    #INITAL COSTS
    initial_cost_solar = cost_of_item(panel_count, panel_cost)
    initial_cost_battery = cost_of_item(battery_count, battery_cost)
    initial_cost_inverter = cost_of_item(inverter_count, inverter_cost)
    initial_cost_controller = cost_of_item(controller_count, controller_cost)
    initial_cost_labour = ((initial_cost_solar + initial_cost_battery + initial_cost_inverter + initial_cost_controller ) * 0.1) #10%
    
  
    #Printing findings
    print()
    print("COST")
    print("Cost of panels : $" +str(initial_cost_solar))
    print("Cost of battery: $" + str(initial_cost_battery))
    print("Cost of inverter: $" + str(initial_cost_inverter))
    print("Cost of charge controllers: $" + str(initial_cost_controller))
    print("Cost of labour (10%) " + str(initial_cost_labour))
    
    #Inital upfront cost
    initial_cost = (initial_cost_solar + initial_cost_battery + initial_cost_inverter + initial_cost_controller + initial_cost_labour )
    print("Initial cost for system: $" + str(initial_cost))
    
    #OPERATION COSTS
    maintenance_solar = panel_maintenance * panel_count
    maintenance_battery = battery_maintenance * battery_count
    maintenance_inverter = inverter_maintenance * inverter_count
    maintenance_controller = controller_maintenance * controller_count
    
    maintenance_per_year = (maintenance_solar + maintenance_battery + maintenance_inverter + maintenance_controller)
    print("Yearly Maintenance: $" + str(maintenance_per_year))
    print()
    print("Total cost: $" + str((maintenance_per_year*25) + initial_cost))


def main():
    
    
    avaliable_solar()
    
    return

if __name__ == "__main__":
    main()