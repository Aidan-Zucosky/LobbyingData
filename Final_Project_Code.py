#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
Created on Fri Mar 15 11:34:04 2024

@author: aidanzucosky


Aidan Zucosky 
Dr. Laney Strange
DS 2500 Final Project
04/12/2024

"""


import csv
import seaborn as sns
import os 
import statistics
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from collections import Counter


DIR = "final_project"



def normalize(lst):
    ''' given a list of numbers, scale each one in
        min/max normalization, and return a new list of
        scaled values
    '''
    mn = min(lst)
    mx = max(lst)
    scaled = []
    for num in lst:
        new_num = (num - mn) / (mx - mn)
        scaled.append(new_num)
    return scaled      


def get_files(dirname, ext = ".csv"):
    """
    Parameters
    ----------
    dirname : The name of the directory 
    ext : we are looking for files in the directory that end with the 
    extension in this case .csv

    Returns
    -------
    A list of all the files that meet the criteria we were looking for 

    """
    
    filenames= []
    files = os.listdir(dirname)
    for file in files: 
        if not os.path.isdir(file):
            filenames.append(dirname +"/" +file)
    
    return filenames



def get_file_types(name, filenames):
    """
    

    Parameters
    ----------
    name : The name of the type of files I need to get 
    filenames : A list of all the filenames from get_files

    Returns
    -------
    good_files : A list of the files wanted 

    """
    good_files = []
    for file in filenames:
        if name in file:
            good_files.append(file)
    return good_files



def read_csv(cont_files, yes):
    """
    Parameters
    ----------
    cont_files : The content of files I want to read from

    Returns
    -------
    lst : Returns the information from each file and what file it came from in a list 

    """
    
    lst = []
    for file in cont_files: 
        with open(file, 'r') as data:
            reader = csv.reader(data)
            next(reader)
            lines = list(reader)
            lst.append(file)
            lst.append(lines)
    
    return lst




def make_dct(large_lst):
    """

    Parameters
    ----------
    large_lst : The twod recieved from read_csv

    Returns
    -------
    dct : The dictionary in which the file name is the key and the information 
    in it is the value 

    """
    dct = {}

    for i  in range(len(large_lst)): 
        key = large_lst[int(2*(i-1))]
        value = large_lst[int(2*(i-1)+1)]
        dct[key] = value
        
        if i == (len(large_lst))/2: 
            break
        
    return dct





def top_recievers(cont_files, dct):
    """

    Parameters
    ----------
    cont_files : The files the dictionary has as keys
    dct : The dictionary recieved from reading the files

    Returns
    -------
    dct_TP : A dictionary describing the top recievers from all the files

    """
    
    top_people = []
    for i in range(len(cont_files)):
        
        two_d = dct[cont_files[i]]

        sorted(two_d, key =lambda person: person[2])
     
        top_people.append(cont_files[i])
        top_people.append(two_d[:10])
 
    dct_TP = {}

    for i  in range(len(top_people)): 
        key = top_people[int(2*(i-1))]
        value = top_people[int(2*(i-1)+1)]
        dct_TP[key] = value
        
        if i == (len(top_people))/2: 
            break
        
    return dct_TP
    


def most_common_top_earners(cont_files, dct_TP):
    """
    

    Parameters
    ----------
    cont_files : The content of files I want 
    dct_TP : A dictionary describing the top recievers from all the files

    Returns
    -------
    LST : A list of the most common top earners 

    """
    
    all_people= []
    for i in range(len(cont_files)):
        year_info = dct_TP[cont_files[i]]
        for person in year_info:
            all_people.append(person[0])
    loop_count = 0 
    LST = []
    
    while loop_count < 5:
        rich = statistics.mode(all_people)
        all_people = [item for item in all_people if item != rich]
        LST.append(rich)
        loop_count += 1
        
    return LST 



def top_pol_incomes(pol, reciever_info):
    """
    Returns
    -------
    pol_salary : Using the previous information find out how much our top earners make

    """
    
    #Create a dictionary of earners and how much they made recieved each year they were on the list

    keys = list(reciever_info.keys())
    earners_dct={}
    for i in range(len(keys)):
        earners_lst=[]
        earners = reciever_info[keys[i]]
        for person in earners:
            if person[0] in pol:
                earners_lst.append(person)
        earners_dct[keys[i]] = earners_lst
    
   
   #Get the list of important people we need  
   
    people = []
    for i in range(len(keys)):
        twod = earners_dct[keys[i]]
        
        for person in twod:
            if person[0] in pol:
                people.append(person)
   
    
    #Create a dictionary of their total salary not just the money they recieved 
    
    pol_salary = {}

    for item in people:
        name = item[0]
        
        lobbying = int(item[2].replace('$', ''))
        
        
    #Politicians have recieved a constant gross yearly salary of $174000 since 2018 so I am adding that here
        if name not in pol_salary:
            pol_salary[name] = [lobbying+174000]
        else:
            pol_salary[name].append(lobbying+174000)

    return pol_salary
    
                    
def compare_pol_to_people():
    
    #Get the files desrcribing each states avergae salary since 1984
    files = get_file_types("MEHOINUS", get_files(DIR))
    
    #Read the information in each files
    read = read_csv(files, get_files(DIR))
    
    #Make a dictionary of the information we want 
    dct = make_dct(read)
    
    #split the dictionary between how much the avergae salary was and what year that was in 
    all_money = []
    all_dates = []
    for i in range(len(files)):
        twod = dct[files[i]]
        money_state= []
        date_state= []
    
    #turn the salary into an integer to do computations with it 
        for entry in twod:
            money = int(entry[1])
            date = entry[0]
            money_state.append(money)
            date_state.append(date)
        all_money.append(money_state)
    all_dates.append(date_state)
    
    #Each state has it's own position in the list
    pensylvania = all_money[0]
    washington = all_money[4]
    south_ca = all_money[3]
    california = all_money[2]
    montana = all_money[1]
    
    #return the information for each state 
    return pensylvania, washington, south_ca, california, montana




def plot_top_earners(TPI):
    
    """
    Plot a bargraph demonstarting how much each politican has 
    earned in total in their apperaneces in the data
    """
    
    people = list(TPI.keys())
    all_earnings = []
    for i in range(len(people)):
        
        total_earnining = sum(TPI[people[i]])
        
        all_earnings.append(total_earnining)
        
    plt.figure(figsize = (13,5))
    plt.bar(x = list(range(len(all_earnings))), height = all_earnings, color = "darkorchid")
    
    for i in range(len(people)):
        plt.text(x = i, y= all_earnings[i], s = all_earnings[i])
    plt.xticks(list(range(len(people))), people)
    
    plt.xlabel("Politicians")
    plt.ylabel("Money recieved in the last 6 years")
    plt.title("Top earners since 2018")
    
    plt.show()
    

def plot_difference_penn(penn):
    #Demonstrate the differences in earning growth between Bob Casey and his constituents 
    
    dct_1 = top_pol_incomes()
        
    y_pol = dct_1["Bob Casey (D-Pa)"]
    
    #This list is based on the order of the files 2018,2022,2024,2020
    x_pol = [34,38,40,36]
    
    label=[2018,2019,2020,2021,2022,2023,2024]
    x_1=[34,35,36,37,38,39,40]
        
    
    #Use Linear Regression to predict the average salary for constituents up to 2024 which is not given
    slope, inter = statistics.linear_regression(list(range(len(penn))), penn)
    
    predict = [(38*slope)+inter,(39*slope)+inter, (40*slope)+inter]
    for val in predict:
        penn.append(val)
        
        
    #Plot the Normalized data to obtain proper visualizations on growth rates
    sns.lineplot(x=x_1, y=normalize(penn[35:]), label = "Average salary of constituients", color = "red")
    sns.lineplot(x=x_pol, y=normalize(y_pol), label = "Salary of Bob Casey", color = "skyblue")

    plt.xticks(x_1, label)
    salaries_2018 = penn[34], y_pol[0]
    salaries_2020 = penn[36], y_pol[3]
    salaries_2022 = penn[38], y_pol[1]
    salaries_2024 = (40*slope)+inter, y_pol[2]
    
    plt.title("Politican's Salary vs Constituent's")
    plt.ylabel("Normilization Vlaues")
    plt.xlabel("Years")
    plt.legend()
    
    salaries = []
    salaries.append(salaries_2018)
    salaries.append(salaries_2020)
    salaries.append(salaries_2022)
    salaries.append(salaries_2024)
    
 
    #Return the 2d list of slaries of the politican and constiuents to compare them later
    return salaries
    
    
    
    
    
    
def plot_difference_washington(wash):
    
        #Demonstrate the differences in earning growth between Maria Cantwell and her constituents 
        
        dct_1 = top_pol_incomes()
            
        y_pol = dct_1['Maria Cantwell (D-Wash)']
        #This list is based on the order of the files 2018,2022,2024,2020
        x_pol = [34,40]
        
        label=[2018,2019,2020,2021,2022,2023,2024]
        x_1=[34,35,36,37,38,39,40]
            
        
        #Use Linear Regression to predict the average salary for constituents up to 2024 which is not given
        slope, inter = statistics.linear_regression(list(range(len(wash))), wash)
        
        slope_1, inter_1  = statistics.linear_regression([38,40], y_pol)
        
        regression_y_pol = [(slope_1*34)+inter, (slope_1*36)+inter ]
        
        
        wash.append((38*slope)+inter)
        wash.append((39*slope)+inter)
        wash.append((40*slope)+inter)
        
        
        for pos in y_pol:
            regression_y_pol.append(pos)
        
        #Plot the Normalized data to obtain proper visualizations on growth rates
        sns.lineplot(x=x_1, y=normalize(wash[35:]), label = "Average salary of constituients", color= "red")
        sns.lineplot(x=x_pol, y=normalize(y_pol), label = "Salary of Maria Cantwell", color = "skyblue")
       
        
        plt.xticks(x_1, label)
        salaries_2018 = wash[34], y_pol[0]
        salaries_2024 = wash[40], y_pol[1]
        
        plt.title("Politican's Salary vs Constituent's")
        plt.ylabel("Normilization Vlaues")
        plt.xlabel("Years")
        plt.legend()
        
        
        salaries = []
        salaries.append(salaries_2018)
        salaries.append(salaries_2024)
        

        #Return the 2d list of slaries of the politican and constiuents to compare them later
        return salaries
       
        
def plot_difference_cal(cal):
    #Demonstrate the differences in earning growth between Kevin McCarthy and his constituents 
    
    dct_1 = top_pol_incomes()
        
    y_pol = dct_1["Kevin McCarthy (R-Calif)"]
    
    #This list is based on the order of the files 2018,2022,2024,2020
    x_pol = [34,38,40,36]
    
    label=[2018,2019,2020,2021,2022,2023,2024]
    x_1=[34,35,36,37,38,39,40]
        
    #Use Linear Regression to predict the average salary for constituents up to 2024 which is not given
    slope, inter = statistics.linear_regression(list(range(len(cal))), cal)
    
    predict = [(38*slope)+inter,(39*slope)+inter, (40*slope)+inter]
    for val in predict:
        cal.append(val)
        
        
    #Plot the Normalized data to obtain proper visualizations on growth rates
    sns.lineplot(x=x_1, y=normalize(cal[35:]), label = "Average salary of constituients", color = "skyblue")
    sns.lineplot(x=x_pol, y=normalize(y_pol), label = "Salary of Kevin McCarthy", color = "red")

    plt.xticks(x_1, label)
    salaries_2018 = cal[34], y_pol[0]
    salaries_2020 = cal[36], y_pol[3]
    salaries_2022 = cal[38], y_pol[1]
    salaries_2024 = (40*slope)+inter, y_pol[2]
    
    plt.title("Politican's Salary vs Constituent's")
    plt.ylabel("Normilization Vlaues")
    plt.xlabel("Years")
    plt.legend()
    
    salaries = []
    salaries.append(salaries_2018)
    salaries.append(salaries_2020)
    salaries.append(salaries_2022)
    salaries.append(salaries_2024)
    
 
    #Return the 2d list of slaries of the politican and constiuents to compare them later
    return salaries
    

def plot_difference_southcar(socar):
    #Demonstrate the differences in earning growth between Tim Scott and his constituents 
        
        dct_1 = top_pol_incomes()
            
        y_pol = dct_1['Tim Scott (R-SC)']
        
        #This list is based on the order of the files 2018,2022,2024,2020
        x_pol = [34,40]
        
        label=[2018,2019,2020,2021,2022,2023,2024]
        x_1=[34,35,36,37,38,39,40]
            
        #Use Linear Regression to predict the average salary for constituents up to  2024 which is not given
        slope, inter = statistics.linear_regression(list(range(len(socar))), socar)
        
        slope_1, inter_1  = statistics.linear_regression([38,40], y_pol)
        
        regression_y_pol = [(slope_1*34)+inter, (slope_1*36)+inter ]
        
        
        socar.append((38*slope)+inter)
        socar.append((39*slope)+inter)
        socar.append((40*slope)+inter)
        
        
        for pos in y_pol:
            regression_y_pol.append(pos)
        
        #Plot the Normalized data to obtain proper visualizations on growth rates
        sns.lineplot(x=x_1, y=normalize(socar[35:]), label = "Average salary of constituients", color= "skyblue")
        sns.lineplot(x=x_pol, y=normalize(y_pol), label = "Salary of Tim Scott", color = "red")
       
        
        plt.xticks(x_1, label)
        salaries_2018 = socar[34], y_pol[0]
        salaries_2024 = socar[40], y_pol[1]
        
        plt.title("Politican's Salary vs Constituent's")
        plt.ylabel("Normilization Vlaues")
        plt.xlabel("Years")
        plt.legend()
        
        
        salaries = []
        salaries.append(salaries_2018)
        salaries.append(salaries_2024)
        
        #Return the 2d list of slaries of the politican and constiuents to compare them later
        return salaries
    
    
    
def plot_difference_mont(mont):
    #Demonstrate the differences in earning growth between Jon Tester and his constituents 
        
        dct_1 = top_pol_incomes()
            
        y_pol = dct_1['Jon Tester (D-Mont)']
        #This list is based on the order of the files 2018,2022,2024,2020
        x_pol = [34,38,40]
        
        label=[2018,2019,2020,2021,2022,2023,2024]
        x_1=[34,35,36,37,38,39,40]
            
        
        #Use Linear Regression to predict the average salary for constituents up to 2024 which is not given
        slope, inter = statistics.linear_regression(list(range(len(mont))), mont)
        
        
        slope_1, inter_1  = statistics.linear_regression([34,38,40], y_pol)
        
        regression_y_pol = [(slope_1*34)+inter]
        
        
        mont.append((38*slope)+inter)
        mont.append((39*slope)+inter)
        mont.append((40*slope)+inter)
        
        
        for pos in y_pol:
            regression_y_pol.append(pos)
        
        
        #Plot the Normalized data to obtain proper visualizations on growth rates
        sns.lineplot(x=x_1, y=normalize(mont[35:]), label = "Average salary of constituients", color= "red")
        sns.lineplot(x=x_pol, y=normalize(y_pol), label = "Salary of Jon Tester", color = "skyblue")
       
        
        plt.xticks(x_1, label)
        salaries_2018 = mont[34], y_pol[0]
        salaries_2022 = mont[38], y_pol[1]
        salaries_2024 = mont[40], y_pol[2]
        
        plt.title("Politican's Salary vs Constituent's")
        plt.ylabel("Normilization Vlaues")
        plt.xlabel("Years")
        plt.legend()
        
        
        salaries = []
        salaries.append(salaries_2018)
        salaries.append(salaries_2022)
        salaries.append(salaries_2024)
        
        #Return the 2d list of slaries of the politican and constiuents to compare them later
        return salaries
    
def plot_difference_in_sal(sals, years):
    """
    

    Parameters
    ----------
    sals : The list of slaries we are looking at returned in the normilzation graph
    years : The list of years being looked at 

    Returns
    -------
    Plots a bar graph comoparing salaries 

    """
    
    #Clear the graph of the normilization 
    plt.clf()
    
    
    #seperate the list from the politicians slaries and the consitunets 
    X = years
    
    people_s =[]
    politician_s = []
    for entry in sals: 
        people = entry[0]
        politician = entry[1]
        people_s.append(people)
        politician_s.append(politician)
    
    X_axis = np.arange(len(X)) 
    
    
    #Plot two bargraphs next to each other to show the differences in slaries 
    plt.bar(X_axis - 0.2, politician_s, 0.4, label = 'Politician Salary', color = "red") 
    plt.bar(X_axis + 0.2, people_s, 0.4, label = 'Constituent Average Salary', color = "skyblue") 
  
    plt.xticks(X_axis, X) 
    
    plt.xlabel("Groups") 
    plt.ylabel("Money") 
    plt.title("Poltician Salary Compared to Consituent's") 
    plt.legend() 
    
    plt.show() 
    
    
    return

def who_is_funding(politician):
    
    #Based on the politician the file we use is different 
    Files = get_file_types("top-contributors", get_files(DIR))
    
    for pos in Files :
        if "-"+politician in pos:
            file = pos
    
    file_2 = "final_project/Top 20 Spenders,  2015-2023.csv"
      
    
    df_poli = pd.read_csv(file)
    df_overall = pd.read_csv(file_2)
    
    features = ["ultorg", "total"]
    
    df_poli = df_poli[features]
    
    df_overall["Combined Total"] = df_overall["Combined Total"].str.replace("$" , "")
    
    df_overall["Combined Total"] = df_overall["Combined Total"].astype(int)
    
    
    dct = {}
   
    for i in range(len(df_poli["ultorg"].tolist())): 
        if df_poli["ultorg"].iloc[i] in df_overall["Lobbying Client"].tolist():
            dct[df_poli["ultorg"].iloc[i]] = [df_poli["total"].iloc[i], 
                                              df_overall["Combined Total"].iloc[i], 
                                              df_poli["total"].iloc[i]/df_overall["Combined Total"].iloc[i] *100
                                              , i+1]

    return dct



def similiar_lobby():
    
    #Find out what lobbyists are most commonly shared across top politicians 
    
    files = get_file_types("top-contributors", get_files(DIR))
    
    jon = pd.read_csv(files[0])
    tim = pd.read_csv(files[1])
    maria = pd.read_csv(files[2])
    bob = pd.read_csv(files[3])
    kevin = pd.read_csv(files[4])
    
    #get the top contributors of each politician
    frame = [jon["ultorg"], tim["ultorg"], maria["ultorg"], bob["ultorg"], kevin["ultorg"]]
    
    
    counter_l = []

    #Count the occurance of each lobbyist 
    for df in frame:
        dfl = df.tolist()
        for item in dfl:
            counter_l.append(item)
    
    counts = Counter(counter_l)
    
    return counts







def main():
    
    
    all_files = get_files(DIR)
    
    contribution_files = get_file_types("Top Recipients of Contributions from Lobbyists,", all_files)
    
    contribution_information = read_csv(contribution_files, all_files)
    
    contribution_dct = make_dct(contribution_information)
    
    contribution_dct
    
    top_recieving_politicians = top_recievers(contribution_files, contribution_dct)
    
    earners = most_common_top_earners(contribution_files, top_recieving_politicians)
    
    print("These are the top earning politicians we will be looking at", earners)
    
    income_info = top_pol_incomes(earners, contribution_dct)
    
    print("This is the reported income of the politicians we are examining", income_info)
    
    #These are the average salaries of people in the states we are looking at using linear regresion
    Penn, Wash, SouthCar, Cali, Mon = compare_pol_to_people()
    
    
    
    plot_top_earners(income_info)
    
    #These are the bargraphs demonstarting each state's politican vs constituent salaries 
    W_sal = plot_difference_washington(Wash)
    P_sal = plot_difference_penn(Penn)
    C_sal = plot_difference_cal(Cali)
    SC_sal = plot_difference_southcar(SouthCar)
    M_sal = plot_difference_mont(Mon)
    
    state = input("What state would you like to compare growth rates of?")
    
    if "Mon" in state:
        growth_ex = M_sal
    if "Cal" in state:
        growth_ex = C_sal
    if "South" in state:
        growth_ex = SC_sal
    if "Penn" in state:
        growth_ex = P_sal
    if "Wash" in state:
        growth_ex = W_sal
    
    plot_difference_in_sal(growth_ex, [2018,2020,2022,2024])
    
    poli = input("What politician would you like to examine?")
    
    funded_by = who_is_funding(poli)
    
    print("These are the companies funding this politician", funded_by)
    
    similiarities = similiar_lobby()
    
    print("These are the companies that our politicians share", similiarities)
    
    
    
if __name__ == "__main__":
    main()
