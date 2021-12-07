#This script will find the cost of only operating a generator
#This script can be imporved by putting all lowest year values into a dictionary and printing the lowest value.

#GENERATOR ONLY COST FUNCTION

import openpyxl 

#BURN RATES (Gallon/hr)
# g3_rate = 11.81
# g4_rate = 9.77
# g5_rate = 9.77
# g6_rate = 7.32
# g7_rate = 7.32
# g8_rate = 7.32
# g9_rate = 7.32
# g10_rate = 7.32
# g11_rate = 7.32
# g12_rate = 4.88

generator = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
generator_fuel_rate = [0, 0, 0, 11.81, 9.77, 9.77, 7.32, 7.32, 7.32, 7.32, 7.32, 7.32, 4.88]
gen_lifetime_cost = {}


wb = openpyxl.Workbook()
sheet = wb.active 



def inflation(present_value, rate, time):
    
    future_value = ((present_value) * ((1.0 + (rate))**(time)))
    
    return future_value

def gen_cost(diesel_cost, inflation_rate, gen_maintenance, year_hours):
    print('in gen_cost function')
    case_list = []
    for gen in generator:
        gen_total_cost = 0

        for i in range(1,26):
            #print(i)
            print("in range")
            diesel_cost = float(diesel_cost)
            inflation_rate = float(inflation_rate)
            i = float(i)
            fuel_price = inflation(diesel_cost, inflation_rate, i)
            fuel_cost_year = (fuel_price * generator_fuel_rate[gen] * year_hours)
            print(fuel_cost_year)
            maintenance = gen_maintenance * gen
           
            year_cost = fuel_cost_year + maintenance
            print("YEAR COST")
            print(year_cost)
        
            #Generator cost for this year
            gen_year_cost = (maintenance + fuel_cost_year)
            gen_column = gen+2
            sheet.cell(row = (i+1), column = gen_column ).value = gen_year_cost

            print("Operating " + str(gen) + " generators costs " + str('{0:.8g}'.format(year_cost)) + " in year " + str(i))
            print("Generator year cost: $" + str('{0:.8g}'.format(gen_year_cost)))
            gen_total_cost += gen_year_cost
        
        gen_lifetime_cost  = (gen, gen_total_cost)
        case_list.append(gen_lifetime_cost)
    spreadsheet = wb.save('Generator_Cost_With_Python2.xlsx')
    
    #Put all lowest year functions in a diction and print lowest value
        #best_key = min()
       # print(gen_lifetime_cost)
        #print(case_list, sep = "\n")
        #print(case_list[0][0])
        # for case in case_list:
        #     lowest_value = case_list[case]
        #     print("Int this function")
        #     print(lowest_value)
        
    return case_list

def main():
    
    #CONSTANTS
    diesel_cost = 3.38 #$/g
    inflation_rate = 0.0261
    year_hours = 8760
    gen_maintenance = 5000  #$/year
    
    gen_cost(diesel_cost, inflation_rate, gen_maintenance, year_hours)
    #print("back from function")
    
    return

if __name__ == "__main__":
    main()
