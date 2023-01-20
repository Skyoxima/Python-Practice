from os import system
import numpy as np
import pandas as pd

def take_input():
    data = []
    no_of_process = int(input("Enter the number of processes: "))
    if no_of_process <= 0:
        print("Exiting...")
        exit()

    for i in range(1, no_of_process + 1):
        arr_time = int(input("Enter the Arrival Time for Process {}: ".format(i)))
        burst_time = int(input("Enter the Burst Time for Process {}: ".format(i)))
        priority = int(input("Enter the Priority for Process {}: ".format(i)))
        temp_dict = {'Process No.': i, 'Arrival Time': arr_time, 'Burst Time': burst_time, 'Priority': priority}
        data.append(temp_dict)
    
    schd_type = int(input("Enter the type of Scheduling Algorithm:\n1. FCFS\n2. SJF\nChoice: "))

    return data, schd_type

def sort_df(data_frame, by_parameter):
    sorted_df = data_frame.sort_values(by = by_parameter)
    sorted_df.reset_index(inplace = True, drop = True) #! necessary, otherwise process list function would give unsorted list since for-in loop goes by index
    return sorted_df

def sorted_process_list(sorted_df):
    process_list = []

    for i in range(0, len(sorted_df)):
        process_list.append([sorted_df['Process No.'][i], sorted_df['Arrival Time'][i], sorted_df['Burst Time'][i], sorted_df['Priority'][i]])
    
    return process_list

def redone_gantt_chart(sorted_schd_list, passed_time = 0):
    end_times = []
    gantt_list = []
    passed_time = 0

    def redone_match_ATPT(curr_passed_time, next_arr_time):
        if curr_passed_time < next_arr_time:
            if curr_passed_time == 0:
                gantt_list.extend([curr_passed_time, "idle", next_arr_time])
            else:
                gantt_list.extend(['idle', next_arr_time])
            return next_arr_time
        elif curr_passed_time == 0:
            gantt_list.append(curr_passed_time)
        return curr_passed_time

    for i in sorted_schd_list:
        passed_time = redone_match_ATPT(passed_time, i[1])
        passed_time += i[2]
        gantt_list.extend(['P' + str(i[0]), passed_time])
        end_times.append(passed_time)

    def print_gantt(gantt_list):
        for i in gantt_list:
            if i != gantt_list[-1]:
                print(i, "-> ", end = "")
            else:
                print(i)
    print_gantt(gantt_list)

    return end_times

def turnaround_time(sorted_df):
    indv_TAT = []

    for i in range(0, len(sorted_df)):
        pFT = sorted_df["Finish Time"][i]
        aT = sorted_df["Arrival Time"][i]
        indv_TAT.append(pFT - aT)
    
    avg_TAT = np.average(indv_TAT)
    sorted_df["Turnaround Time"] = indv_TAT
    return avg_TAT, sorted_df

def waiting_time(sorted_df):
    indv_WT = []       #in FCFS, the waiting time of the first process will be always 0
    
    #! using formula WT = TAT - BT 
    for i in range(0, len(sorted_df)):
        TAT = sorted_df["Turnaround Time"][i]
        BT = sorted_df["Burst Time"][i]
        indv_WT.append(TAT - BT)
    
    avg_WT = np.average(indv_WT)
    sorted_df["Waiting Time"] = indv_WT
    return avg_WT, sorted_df

def fcfs(raw_df):
    sorted_df = sort_df(raw_df, 'Arrival Time')
    sorted_schd_list = sorted_process_list(sorted_df)
    
    print("\nGantt Chart:")
    per_process_end_time = redone_gantt_chart(sorted_schd_list)
    sorted_df["Finish Time"] = per_process_end_time

    avg_turnaround_time, sorted_df = turnaround_time(sorted_df)
    avg_wait_time, sorted_df = waiting_time(sorted_df)
    pd.set_option('display.expand_frame_repr', False)
    print("\nSchedule Table:\n",sorted_df)
    print("\nAverage Waiting Time: {}\nAverage Turnaround Time: {}\n".format(avg_wait_time, avg_turnaround_time))

def sjf_check_special_cases(raw_df):
    if(len(raw_df["Arrival Time"].unique()) == 1):
        return 0
    elif(len(raw_df["Burst Time"].unique()) == 1):
        return 1
    return -1

def slice_df(sorted_df, sort_factor, curr_passed_time):
    sliced_df = sorted_df.loc[sorted_df[sort_factor] <= curr_passed_time]
    
    if len(sliced_df) == 0:
        sliced_df = sorted_df.loc[sorted_df[sort_factor] > curr_passed_time]
        first_greater_AT = sliced_df["Arrival Time"].iloc[0]
        sliced_df = sorted_df.loc[sorted_df[sort_factor] == first_greater_AT]
    
    sliced_sorted_BT_df = sort_df(sliced_df, "Burst Time")
    to_schd = list(sliced_sorted_BT_df.iloc[0])
    sorted_df = sorted_df.drop(sorted_df[sorted_df["Process No."] == to_schd[0]].index)

    return to_schd, to_schd[2], sorted_df

def sjf(raw_df):
    case = sjf_check_special_cases(raw_df)
    fin_sorted_schd_list = []
    curr_passed_time = 0

    if case == 1:           #All burst times equal
        fcfs(raw_df)
    elif case == 0:         #All arrival times equal
        sorted_df = sort_df(raw_df, 'Burst Time')
        sorted_schd_list = sorted_process_list(sorted_df)

        print("\nGantt Chart:")
        per_process_end_time = redone_gantt_chart(sorted_schd_list)
        sorted_df["Finish Time"] = per_process_end_time

        avg_turnaround_time, sorted_df = turnaround_time(sorted_df)
        avg_wait_time, sorted_df = waiting_time(sorted_df)
        pd.set_option('display.expand_frame_repr', False)
        print("\nSchedule Table:\n",sorted_df)
        print("Average Waiting Time: {}\nAverage Turnaround Time: {}".format(avg_wait_time, avg_turnaround_time))
    else:
        initial_sorted_df = sort_df(raw_df, 'Arrival Time')
        mod_sorted_df = initial_sorted_df.copy()
        curr_passed_time = initial_sorted_df["Arrival Time"][0]

        for i in range(0, len(initial_sorted_df)):
            temp_catcher, prev_burst, mod_sorted_df = slice_df(mod_sorted_df, "Arrival Time", curr_passed_time)
            curr_passed_time += prev_burst
            fin_sorted_schd_list.append(temp_catcher)

        process_order = [j[0] for j in fin_sorted_schd_list] 
        new_sorted_df = pd.DataFrame()
        for i in range(0, len(process_order)):
            new_sorted_df = pd.concat([new_sorted_df, initial_sorted_df[initial_sorted_df["Process No."] == process_order[i]]], ignore_index = True)
        
        print("\nGantt Chart:")
        per_process_end_time = redone_gantt_chart(fin_sorted_schd_list)
        new_sorted_df["Finish Time"] = per_process_end_time

        avg_turnaround_time, new_sorted_df = turnaround_time(new_sorted_df)
        avg_wait_time, new_sorted_df = waiting_time(new_sorted_df)
        pd.set_option('display.expand_frame_repr', False)
        print("\nSchedule Table:\n",new_sorted_df)
        print("\nAverage Waiting Time: {}\nAverage Turnaround Time: {}\n".format(avg_wait_time, avg_turnaround_time))

def caller():
    system("cls")
    data, schd_type = take_input()
    data_frame = pd.DataFrame(data)
    print("\nRaw DataFrame:\n", data_frame)
    if schd_type == 1:
        fcfs(data_frame)
    elif schd_type == 2:
        sjf(data_frame)
    else:
        print("Invalid Choice!")

caller()