import numpy as np
import pandas as pd
from os import system
import copy

def take_input():
    data = []
    no_of_process = int(input("Enter the number of processes: "))

    for i in range(1, no_of_process + 1):
        arr_time = int(input("Enter the Arrival Time for Process {}: ".format(i)))
        burst_time = int(input("Enter the Burst Time for Process {}: ".format(i)))
        temp_dict = {'Process No.': i, 'Arrival Time': arr_time, 'Initial Burst Time': burst_time, 'Remaining Time': burst_time}
        data.append(temp_dict)

    schd_type = int(input("Enter the Preemptive scheduler: \n1. SRTF\n2. Round-Robin: "))
    if(schd_type == 2):
        time_quantum = int(input("Enter the Time Quantum: "))
        return data, schd_type, time_quantum

    return data, schd_type, 1

def sort_df(data_frame, by_parameter):
    sorted_df = data_frame.sort_values(by = by_parameter)
    sorted_df.reset_index(inplace = True, drop = True) 
    
    return sorted_df

def df_slicer(data_frame, sort_factor, cond_rhs, condition):
    if condition == "LESS_THAN_EQUAL":
        slice_df = data_frame.loc[data_frame[sort_factor] <= cond_rhs]
    elif condition == "GREATER_THAN":
        slice_df = data_frame.loc[data_frame[sort_factor] > cond_rhs]
    
    return slice_df

def redone_gantt_chart(sorted_schd_list, passed_time = 0):    
    gantt_list = []
    passed_time = 0
    end_times = dict()

    def redone_match_ATPT(curr_passed_time, next_arr_time):
        if curr_passed_time < next_arr_time:
            if curr_passed_time == 0:
                gantt_list.extend([curr_passed_time, "\033[38;5;225midle", next_arr_time])
            else:
                gantt_list.extend(['\033[38;5;225midle', next_arr_time])
            return next_arr_time
            
        elif curr_passed_time == 0:
            gantt_list.append(curr_passed_time)
        return curr_passed_time

    for i in sorted_schd_list:
        passed_time = redone_match_ATPT(passed_time, i[1])
        passed_time += i[2]
        gantt_list.extend(['\033[38;5;225m' +'P' + str(i[0]), passed_time])
        end_times.update({i[0]:passed_time})
    # print(gantt_list)

    def print_gantt(gantt_list):
        for i in gantt_list:
            if i != gantt_list[-1]:
                print(i, "\033[1;90m-> \033[0m", end = "")
            else:
                print(i, end = "")
    print("\033[4m\033[38;5;225mGantt Chart\033[0m")
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
    return avg_TAT

def waiting_time(sorted_df):
    indv_WT = []       #in FCFS, the waiting time of the first process will be always 0
    
    #! using formula WT = TAT - BT 
    #(alternatively, formula can be WT = FTprev - ATcurr)
    for i in range(0, len(sorted_df)):
        TAT = sorted_df["Turnaround Time"][i]
        BT = sorted_df["Initial Burst Time"][i]
        indv_WT.append(TAT - BT)
    
    avg_WT = np.average(indv_WT)
    sorted_df["Waiting Time"] = indv_WT
    return avg_WT

def SRTF(raw_df):
    AT_sorted_full_df = sort_df(raw_df, "Arrival Time")
    backup = AT_sorted_full_df.copy()
    
    curr_passed_time = 0
    per_process_passed_time = 0      
    fully_scheduled = 0
    schdlist = []
    noofprocess = raw_df.shape[0]
    previously_running_proc_no = -1

    while(fully_scheduled != noofprocess):
        AT_sliced_df = df_slicer(AT_sorted_full_df, "Arrival Time", curr_passed_time, "LESS_THAN_EQUAL")
        
        if len(AT_sliced_df) == 0:
            curr_passed_time += 1
            continue

        RT_sliced_df = sort_df(AT_sliced_df, "Remaining Time")
        running_proc_no = RT_sliced_df["Process No."].iloc[0]
    
        if(running_proc_no != previously_running_proc_no and previously_running_proc_no != -1 and 
           (len(AT_sorted_full_df.loc[AT_sorted_full_df["Process No."] == previously_running_proc_no]) != 0)): 
            to_schd = AT_sorted_full_df.loc[AT_sorted_full_df["Process No."] == previously_running_proc_no, ["Process No.", "Arrival Time", "Initial Burst Time"]].values.tolist()[0]
            to_schd[2] = per_process_passed_time
            schdlist.append(to_schd)
            per_process_passed_time = 0

        previously_running_proc_no = running_proc_no

        AT_sorted_full_df.loc[AT_sorted_full_df["Process No."] == running_proc_no, "Remaining Time"] -= 1
        curr_passed_time += 1
        per_process_passed_time += 1

        if(int(AT_sorted_full_df.loc[AT_sorted_full_df["Process No."] == running_proc_no, "Remaining Time"]) == 0):
            to_schd = AT_sorted_full_df.loc[AT_sorted_full_df["Process No."] == running_proc_no, ["Process No.", "Arrival Time", "Initial Burst Time"]].values.tolist()[0]
            to_schd[2] = per_process_passed_time
            schdlist.append(to_schd)
            fully_scheduled += 1
            per_process_passed_time = 0
            AT_sorted_full_df.drop(AT_sorted_full_df.loc[AT_sorted_full_df["Process No."] == running_proc_no].index, inplace = True)
    
    end_times = redone_gantt_chart(schdlist)
    new_df = backup
    new_df["Remaining Time"], new_df["Finish Time"] = [0 for i in range(len(new_df))], [0 for i in range(len(new_df))]

    for i in end_times.keys():   
        for j in range(0, len(new_df)):                 
            if(int(new_df.loc[j, "Process No."]) == i):
                new_df.loc[j, "Finish Time"] = end_times[i]
    
    avg_turnaround_time = turnaround_time(new_df)
    avg_waiting_time = waiting_time(new_df)
    print("\n\n", new_df)
    print("\nAverage Waiting Time: \033[1m\033[4m\033[38;5;50m{}\033[0m\nAverage Turnaround Time: \033[1m\033[4m\033[38;5;50m{}\033[0m".format(avg_waiting_time, avg_turnaround_time))

def round_robin(raw_df, quantum = 3):
    AT_sorted_full_df = sort_df(raw_df, "Arrival Time")
    backup = AT_sorted_full_df.copy()

    curr_passed_time = AT_sorted_full_df.loc[0, "Arrival Time"]
    per_process_passed_time = 0      
    fully_scheduled = 0
    schdlist = []
    noofprocess = raw_df.shape[0]
    is_preempted = {key: 0 for key in [i for i in range(0, noofprocess)]}
    i_flag = 0
    backup_i = -999
    i = 0

    while(fully_scheduled != noofprocess):
        if i == noofprocess:
            i = 0    
            
        if(i != 0 and i_flag == 1):
            i -= 1
            i_flag = 0
        
        if(AT_sorted_full_df["Arrival Time"].iloc[i] > curr_passed_time):
            #check the queue first
            backup_i = copy.deepcopy(i)
            for k in range(0, i):
                if(AT_sorted_full_df["Remaining Time"].iloc[k] > 0 and is_preempted[k] >= 1):
                    i = k
                    break
            
            if(backup_i == i):
                curr_passed_time += 1
                backup_i = -999
                i += 1
                i_flag = 1
                continue

        for j in range(0, quantum):
            if(is_preempted[i] != -1):
                AT_sorted_full_df.iloc[i, 3] -= 1
                curr_passed_time += 1
                per_process_passed_time += 1
                    
                if(int(AT_sorted_full_df.iloc[i, 3]) == 0):
                    to_schd = AT_sorted_full_df.iloc[i, [0, 1, 2]].values.tolist()
                    to_schd[2] = per_process_passed_time
                    schdlist.append(to_schd)
                    fully_scheduled += 1
                    per_process_passed_time = 0
                    is_preempted[i] = -1
                    break

                elif(per_process_passed_time == quantum):
                    to_schd = AT_sorted_full_df.iloc[i, [0, 1, 2]].values.tolist()
                    to_schd[2] = per_process_passed_time
                    schdlist.append(to_schd)
                    is_preempted[i] += 1
                    per_process_passed_time = 0    
        i += 1            

    end_times = redone_gantt_chart(schdlist)
    new_df = backup
    new_df["Remaining Time"], new_df["Finish Time"] = [0 for i in range(len(new_df))], [0 for i in range(len(new_df))]

    for i in end_times.keys():       
        for j in range(0, len(new_df)):                 
            if(int(new_df.loc[j, "Process No."]) == i):
                new_df.loc[j, "Finish Time"] = end_times[i]
    
    avg_turnaround_time = turnaround_time(new_df)
    avg_waiting_time = waiting_time(new_df)
    print("\n\n", new_df)
    print("\nAverage Waiting Time: \033[1m\033[4m\033[38;5;50m{}\033[0m\nAverage Turnaround Time: \033[1m\033[4m\033[38;5;50m{}\033[0m".format(avg_waiting_time, avg_turnaround_time))

def caller():
    system("cls")
    data, schd_type, time_quantum = take_input()
    data_frame = pd.DataFrame(data)
    print("\nRaw DataFrame:\n", data_frame, "\n")
    if schd_type == 1:
        SRTF(data_frame)
    elif schd_type == 2:
        round_robin(data_frame, time_quantum)
    else:
        print("Invalid Choice!")

caller()