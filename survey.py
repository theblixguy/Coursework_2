# Customer survey results program written in Python
# Compiled and tested using Python 3.5.0
# Author: Suyash Srijan, student ID: 14076594, Coursework 2 U08008 Modern Computing Technology

# Some imports that we need

import csv
import string
import os
import copy
import collections

# Global variables we need

survey_data = dict()
weights_list = ['3', '2', '1']

# Function to clear the console output

def clear_screen():
        os.system('cls' if os.name == 'nt' else 'clear')

# Function to read survey data from text file
#
# This function reads the text file using the CSV reader and stores them in a dictionary
# The dictionary contains the department name as the key and the votes as the value stored in a list, together known as an "item"
# The dictionary has as many items as there are departments

def readData():
    with open('survey_data.txt', 'r') as surveyFile:
        readerObj = csv.reader(surveyFile, delimiter = ' ')
        for row in readerObj:
                survey_data[row[0]]=row[1:]

# Function to print survey data
# 
# This function simply loops through all the items in the dictionary and prints the data with readable format

def displayData():
    for k,v in survey_data.items():
        print(str(k) + ":\nGood votes => " + str(v[0]) + "\nFair votes => " + str(v[1]) + "\nPoor votes => " + str(v[2]) + "\n")

# Function to calculate total number of users/votes in a department
#
# This function takes the department name as input and then uses a helper function called checkDepartmentExists() to check if
# the department exists or not, and returns the total users/votes if the department exists, or 0 if the department does not exist
#

def calculateTotalByDepartment(key):
    total_users = 0
    if checkDepartmentExists(key) == True:
        total_users = sum(int(i) for i in survey_data[key])
    return total_users

# Function to calculate weighted average of votes in a department
#
# This function takes the department name as input and then uses a helper function called checkDepartmentExists() to check if
# the department exists or not, and returns the weighted average if the department exists, or 0 if the department does not exist

def calculateAverageByDepartment(key):
    avg = 0
    if checkDepartmentExists(key) == True:
        avg = ((int(survey_data[key][0]) * int(weights_list[0]) + int(survey_data[key][1]) * int(weights_list[1]) + int(survey_data[key][2]) * int(weights_list[2])) / sum(int(i) for i in survey_data[key]))
    return avg

# Function to print data specific to a department
#
# This function takes the department name as input and prints the Total users/votes in the department and the weighted average value 
# using the helper function calculateTotalByDepartment() and calculateAverageByDepartment()
        
def getDataByDepartment(key):
    print("Total users: " + str(calculateTotalByDepartment(key)) + "\nAverage: " + str(calculateAverageByDepartment(key)))
        
# Function to check if a department exists in our dictionary, returns True if it does, otherwise False

def checkDepartmentExists(key):
    does_exist = False
    if key in survey_data:
        does_exist = True
    return does_exist
        
# Function to ask the user which department's data he/she would like to see and then print the data using the function getDataByDepartment()
# If the department the user entered does not exists then an error message is shown and the user is asked to type the name of the department again
# The user can also type 'menu' to go back to the main menu of the program

def displayDataByDepartment():
    selection = True
    while selection:
        print ("""
        Type the name of the department to see its information, or type 'menu' to go back
        """)
        break
        
    ans = input("")
    if ans == "menu":
         clear_screen()
         menu()
    elif checkDepartmentExists(ans) == False:
         print("The department you entered does not exist")
         displayDataByDepartment()
    else:
         getDataByDepartment(ans)

# Function to calculate total number of users/votes
#
# To calculate the total number of users/votes, we get all the values for each department from our dictionary (stored as a list) and 
# then store it in a list of lists. Then we use a for loop to extract each list and then using another for loop we extract each item 
# in the list and sum it and store the total summed value and then display it to the user

def calculateTotal():
    total_sum = 0
    list_values = list(survey_data.values())
    for x in list_values: total_sum = total_sum + sum(int(i) for i in x)
    print("Total users: " + str(total_sum))

# Function to calculate total weighted average
#
# To calculate weighted average, we create a new list of lists containing values of each department as a list. We use a for loop to
# loop through the lists and for each list, we create three new dictionaries items, with the vote as the key and the corresponding weight as the 
# value. We use the zip method to create the dictionary containing the three items using the two lists, and then we merge the dictionary with 
# an empty (base) dictionary using the helper function merge_two_dicts() we keep doing it until we've gone through all the lists of votes. Now, 
# it's just a matter of looping through the items of the dictionary and simply taking a sum of the multiplication of the key (votes) and 
# value (weight) and then dividing it by the sum of the keys (votes) to get the weighted average
#
# Once we have calculated the weight, we then display it to the user
#
# Weighted average formula: (x1 * w1 + ... xn * wn) / (x1 + ... xn), where x1 .. xn are votes and w1 ... wn are the weights

def calculateAverage():
    value_weight_dict = dict()
    list_values = list(survey_data.values())
    for x in list_values:
        tmp_dict = zip(x, weights_list)
        value_weight_dict = merge_two_dicts(value_weight_dict,tmp_dict)
        print(tmp_dict.items())

    numerator = sum(int(k) * int(v) for k,v in value_weight_dict.items())
    denominator = sum(int(k) for k,v in value_weight_dict.items())

    weighted_average = numerator / denominator

    print("Total average: " + str(weighted_average))

# Function to calculate the highest average, i.e department with the highest weighted average
#
# This is actually very simple to do, we create a new dictionary with a copy of all items from our survey data, and then we use a for loop
# to loop through all the lists of value for each department and take a weighted average of it and then replace the list of values with
# the weighted average value. Now, we have a dictionary with the key as the department name and the value as the weighted average of the votes. 
# We then sort the dictionary items into an OrderedDict, which contains our dictionary items in decending order (highest value first) and then 
# we simply take the first item from the dictionary and show it to the user
#
# # Weighted average formula: (x1 * w1 + ... xn * wn) / (x1 + ... xn), where x1 .. xn are votes and w1 ... wn are the weights

def displayHighest():
    survey_data_temp = dict(survey_data)
    for k,v in survey_data_temp.items():
            avg = ((int(v[0]) * int(weights_list[0]) + int(v[1]) * int(weights_list[1]) + int(v[2]) * int(weights_list[2])) / sum(int(i) for i in v))
            survey_data_temp[k] = avg
    sorted_survey_data_temp = collections.OrderedDict(sorted(survey_data_temp.items(), key=lambda t: t[1], reverse = True))
    print(list(sorted_survey_data_temp.keys())[0] + ": " + str((list(sorted_survey_data_temp.values())[0])))

# Function to calculate the lowest average, i.e department with the lowest weighted average
#
# This is actually very simple to do, we create a new dictionary with a copy of all items from our survey data, and then we use a for loop
# to loop through all the lists of value for each department and take a weighted average of it and then replace the list of values with
# the weighted average value. Now, we have a dictionary with the key as the department name and the value as the weighted average of the votes. 
# We then sort the dictionary items into an OrderedDict, which contains our dictionary items in ascending order (lowest value first) and then 
# we simply take the first item from the dictionary and show it to the user
#
# Weighted average formula: (x1 * w1 + ... xn * wn) / (x1 + ... xn), where x1 .. xn are votes and w1 ... wn are the weights

def displayLowest():
    survey_data_temp = dict(survey_data)
    for k,v in survey_data_temp.items():
            avg = ((int(v[0]) * int(weights_list[0]) + int(v[1]) * int(weights_list[1]) + int(v[2]) * int(weights_list[2])) / sum(int(i) for i in v))
            survey_data_temp[k] = avg
    sorted_survey_data_temp = collections.OrderedDict(sorted(survey_data_temp.items(), key=lambda t: t[1], reverse = False))
    print(list(sorted_survey_data_temp.keys())[0] + ": " + str((list(sorted_survey_data_temp.values())[0])))

# Function to calculate the number of departments with poor or fair performance and display it to the user
#
# To do this, we first create a copy of the survey data, then we loop through all the fair and poor votes and calculate the contribution factor
# of the votes i.e percentage of votes ((number of votes / sum of votes) * 100) and then we check if the percentage is equal to or more than 50,
# and if it is then we add the department name to a list. If there are no departments, then we simply tell the user that there are no departments 
# with equal to or more than 50% poor or fair votes

def displayPoorPerformance():
    survey_data_temp = dict(survey_data)
    list_dept = list()
    for k,v in survey_data_temp.items():
        perc_fair = (int(v[1]) / sum(int(i) for i in v) * 100)
        perc_poor = (int(v[2]) / sum(int(i) for i in v) * 100)
        if perc_fair >= 50 or perc_poor >= 50:
            list_dept.append(k)
    if not list_dept:
        print("No departments with 50% or more fair or poor votes")
    else:
        print(*list_dept, sep='\n')

# Function to calculate the number of departments with good performance and display it to the user
#
# To do this, we first create a copy of the survey data, then we loop through all the good votes and calculate the contribution factor
# of the votes i.e percentage of votes ((number of votes / sum of votes) * 100) and then we check if the percentage is equal to or more than 60,
# and if it is then we add the department name to a list. If there are no departments, then we simply tell the user that there are no departments 
# with equal to or more than 60% good votes

def displayExcellentPerformance():
    survey_data_temp = dict(survey_data)
    list_dept = list()
    for k,v in survey_data_temp.items():
        perc_excellent = (int(v[0]) / sum(int(i) for i in v) * 100)
        if perc_excellent >= 60:
            list_dept.append(k)
    if not list_dept:
        print("No departments with 60% or more good votes")
    else:
        print(*list_dept, sep='\n')

# Function to combine two dictionaries into one dictionrary, returns the final dictionary back

def merge_two_dicts(dict1, dict2):
    final_dict = dict1.copy()
    final_dict.update(dict2)
    return final_dict

# Function to display program menu to the user. The user can choose from a variety of options. If the user wants to exit, he can simply
# type 8 to select Quit. If an invalid choice is selected then the user is informed

def menu():
    selection = True
    while selection:
        print ("""
        1. Display all survey information
        2. Display survey information by department
        3. Display departments with highest average customer satisfaction
        4. Display departments with lowest average customer satisfaction
        5. Display the departments for which 50% or more of the customers voted fair or poor
        6. Display the departments for which 60% or more of the customers voted good
        7. Display the number of people that have used the customer satisfaction devices and the total average value of their responses
        8. Quit
        """)
    
        ans = input("What would you like to do?\n\n") 
        if ans == "1": 
            displayData()
        elif ans == "2":
            displayDataByDepartment()
        elif ans == "3":
            displayHighest()
        elif ans == "4":
            displayLowest()
        elif ans == "5":
            displayPoorPerformance()
        elif ans == "6":
            displayExcellentPerformance()
        elif ans == "7":
            calculateTotal()
            calculateAverage()
        elif ans == "8":
            print("Goodbye!")
            quit() 
        elif ans != "":
            print("\n Not a valid choice, please try again")

if __name__ == "__main__":
    readData()
    menu()