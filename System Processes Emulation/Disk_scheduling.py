import numpy as np
from os import system

def take_input():
    req_sequence = [int(i) for i in input("Enter the request sequence: ").split()]
    initial_rest = int(input("Enter the initial resting of the head: "))
    seek_multiplier = int(input("Enter the cost for travelling a single track: "))
    total_nooftracks = int(input("Enter the total number of tracks available: "))

    return req_sequence, initial_rest, seek_multiplier, total_nooftracks

def final_ans(total_seek_time, disk_schedule, initial_rest, algo_name):
    print("\033[1m\033[4m\033[38;5;229m" + str(algo_name) + "\033[0m")
    print("\033[1m\033[38;5;85mDisk Pointer Trace: \033[0m")
    print("\033[1m\033[38;5;213m"+ str(initial_rest) + "\033[0m -> ", end = "")
    for i in disk_schedule:
        if i != disk_schedule[-1]:
            print(i, "-> ", end = "")
        else:
            print(i)
    
    print("Total Seek Time: \033[1m\033[4m\033[38;5;217m"+ str(total_seek_time) + "\033[0m msecs\n\n")

def fcfs_dschd(req_sequence, curr_rest, per_track_seek_cost, total_nooftracks = 200):
    initial_rest = curr_rest
    total_seek_time = 0
    disk_schedule = []

    for i in req_sequence:
        disk_schedule.append(i)
        total_seek_time += np.abs(i - curr_rest) * per_track_seek_cost
        curr_rest = i 

    final_ans(total_seek_time, disk_schedule, initial_rest, "First Come First Serve (FCFS)")

def sstf_dschd(req_sequence, curr_rest, per_track_seek_cost, total_nooftracks = 200):
    initial_rest = curr_rest
    total_seek_time = 0
    nooftracks = len(req_sequence)
    min_cost = 9999
    to_schd = -1
    temp_cost = 0
    disk_schedule = []

    while len(disk_schedule) != nooftracks:
        for i in req_sequence:
            temp_cost = np.abs(i - curr_rest) * per_track_seek_cost
            if temp_cost < min_cost:
                min_cost = temp_cost
                to_schd = i
            
        req_sequence.remove(to_schd)
        total_seek_time += min_cost
        min_cost = 9999
        disk_schedule.append(to_schd)
        curr_rest = to_schd

    final_ans(total_seek_time, disk_schedule, initial_rest, "Shortest Serving Time First (SSTF)")

def scan_dschd(req_sequence, curr_rest, per_track_seek_cost, total_nooftracks = 200):
    initial_rest = curr_rest
    total_seek_time = 0
    disk_schedule = []
    
    sorted_req_sequence = list(sorted(req_sequence))
    left_tracks = [i for i in sorted_req_sequence if i < curr_rest]
    right_tracks = [i for i in sorted_req_sequence if i > curr_rest]
    
    #* to choose side, nearest end is chosen
    diff_1 = curr_rest - 0
    diff_2 = (total_nooftracks - 1) - curr_rest
    
    if(diff_1 <= diff_2):
        left_tracks.insert(0, 0)
        for i in range(len(left_tracks) - 1, -1, -1): #? reverse traversing the left tracks first
            disk_schedule.append(left_tracks[i])
            total_seek_time += (curr_rest - left_tracks[i]) * per_track_seek_cost
            curr_rest = left_tracks[i]

        for i in range(0, len(right_tracks)):         #? then go for the right tracks ascendingly
            disk_schedule.append(right_tracks[i])
            total_seek_time += (right_tracks[i] - curr_rest) * per_track_seek_cost
            curr_rest = right_tracks[i]
    
    else:
        right_tracks.append(total_nooftracks - 1)
        for i in range(0, len(right_tracks)):         #* go for the right tracks first ascendingly
            disk_schedule.append(right_tracks[i])
            total_seek_time += (right_tracks[i] - curr_rest) * per_track_seek_cost
            curr_rest = right_tracks[i]

        for i in range(len(left_tracks) - 1, -1, -1):   #* then go for the left tracks descendingly
            disk_schedule.append(left_tracks[i])
            total_seek_time += (curr_rest - left_tracks[i]) * per_track_seek_cost
            curr_rest = left_tracks[i]

    final_ans(total_seek_time, disk_schedule, initial_rest, "SCAN")

def cscan_dschd(req_sequence, curr_rest, per_track_seek_cost, total_nooftracks = 200):
    initial_rest = curr_rest
    total_seek_time = 0
    disk_schedule = []
    
    sorted_req_sequence = list(sorted(req_sequence))
    left_tracks = [i for i in sorted_req_sequence if i < curr_rest]
    right_tracks = [i for i in sorted_req_sequence if i > curr_rest]
    
    #* to choose side, nearest end is chosen
    diff_1 = curr_rest - 0
    diff_2 = (total_nooftracks - 1) - curr_rest

    if(diff_1 <= diff_2): #! left side
        left_tracks.insert(0, 0)
        for i in range(len(left_tracks) - 1, -1, -1):           #? reverse traversing the left tracks first
            disk_schedule.append(left_tracks[i])
            total_seek_time += np.abs(curr_rest - left_tracks[i]) * per_track_seek_cost
            curr_rest = left_tracks[i]

        curr_rest = total_nooftracks - 1                       #! Do not penalize for ends-change step
        for i in range(len(right_tracks) - 1, -1, -1):         #? then go for the right tracks also reverse
            disk_schedule.append(right_tracks[i])
            total_seek_time += np.abs(right_tracks[i] - curr_rest) * per_track_seek_cost
            curr_rest = right_tracks[i]
    
    else: #! right side
        right_tracks.append(total_nooftracks - 1)
        for i in range(0, len(right_tracks)):         #* go for the right tracks first ascendingly
            disk_schedule.append(right_tracks[i])
            total_seek_time += np.abs(right_tracks[i] - curr_rest) * per_track_seek_cost
            curr_rest = right_tracks[i]
        
        curr_rest = 0                                       #! Do not penalize for ends-change step
        for i in range(0, len(left_tracks)):         #* then go for the left tracks also ascendingly
            disk_schedule.append(left_tracks[i])
            total_seek_time += np.abs(curr_rest - left_tracks[i]) * per_track_seek_cost
            curr_rest = left_tracks[i]

    final_ans(total_seek_time, disk_schedule, initial_rest, "C-SCAN")

def look_dschd(req_sequence, curr_rest, per_track_seek_cost, total_nooftracks = 200):
    initial_rest = curr_rest
    total_seek_time = 0
    disk_schedule = []
    
    sorted_req_sequence = list(sorted(req_sequence))
    left_tracks = [i for i in sorted_req_sequence if i < curr_rest]
    right_tracks = [i for i in sorted_req_sequence if i > curr_rest]
    
    #* to choose side, nearest end is chosen
    diff_1 = curr_rest - 0
    diff_2 = (total_nooftracks - 1) - curr_rest
    
    if(diff_1 <= diff_2):
        for i in range(len(left_tracks) - 1, -1, -1): #? reverse traversing the left tracks first
            disk_schedule.append(left_tracks[i])
            total_seek_time += (curr_rest - left_tracks[i]) * per_track_seek_cost
            curr_rest = left_tracks[i]

        for i in range(0, len(right_tracks)):         #? then go for the right tracks ascendingly
            disk_schedule.append(right_tracks[i])
            total_seek_time += (right_tracks[i] - curr_rest) * per_track_seek_cost
            curr_rest = right_tracks[i]
    
    else:
        for i in range(0, len(right_tracks)):         #* go for the right tracks first ascendingly
            disk_schedule.append(right_tracks[i])
            total_seek_time += (right_tracks[i] - curr_rest) * per_track_seek_cost
            curr_rest = right_tracks[i]

        for i in range(len(left_tracks) - 1, -1, -1):   #* then go for the left tracks descendingly
            disk_schedule.append(left_tracks[i])
            total_seek_time += (curr_rest - left_tracks[i]) * per_track_seek_cost
            curr_rest = left_tracks[i]

    final_ans(total_seek_time, disk_schedule, initial_rest, "LOOK")

def clook_dschd(req_sequence, curr_rest, per_track_seek_cost, total_nooftracks = 200):
    initial_rest = curr_rest
    total_seek_time = 0
    disk_schedule = []
    
    sorted_req_sequence = list(sorted(req_sequence))
    left_tracks = [i for i in sorted_req_sequence if i < curr_rest]
    right_tracks = [i for i in sorted_req_sequence if i > curr_rest]
    
    #* to choose side, nearest end is chosen
    diff_1 = curr_rest - 0
    diff_2 = (total_nooftracks - 1) - curr_rest

    if(diff_1 <= diff_2): #! left side
        for i in range(len(left_tracks) - 1, -1, -1):           #? reverse traversing the left tracks first
            disk_schedule.append(left_tracks[i])
            total_seek_time += np.abs(curr_rest - left_tracks[i]) * per_track_seek_cost
            curr_rest = left_tracks[i]

        curr_rest = right_tracks[-1]               #! Do not penalize (or penalize less (alpha)) for ends-change step, also end is not the last track but the last requested track
        for i in range(len(right_tracks) - 1, -1, -1):         #? then go for the right tracks also reverse
            disk_schedule.append(right_tracks[i])
            total_seek_time += np.abs(right_tracks[i] - curr_rest) * per_track_seek_cost
            curr_rest = right_tracks[i]
    
    else: #! right side
        for i in range(0, len(right_tracks)):         #* go for the right tracks first ascendingly
            disk_schedule.append(right_tracks[i])
            total_seek_time += np.abs(right_tracks[i] - curr_rest) * per_track_seek_cost
            curr_rest = right_tracks[i]
        
        curr_rest = left_tracks[0]                  #!
        for i in range(0, len(left_tracks)):   #* then go for the left tracks also ascendingly
            disk_schedule.append(left_tracks[i])
            total_seek_time += np.abs(curr_rest - left_tracks[i]) * per_track_seek_cost
            curr_rest = left_tracks[i]

    final_ans(total_seek_time, disk_schedule, initial_rest, "C-LOOK")

def caller():
    system("cls")
    req_sequence, initial_rest, seek_multiplier, total_nooftracks = take_input()
    backup_req_sequence = list(req_sequence)
    print("\n\033[1m\033[38;5;183mThis program chooses the direction of scheduling by determining the nearest end from the initial resting and going towards the nearer one.\nAlso, in C-SCAN and C-LOOK, this program is not counting the end-to-end track change.\n\033[0m")
    algorithms = {"1": fcfs_dschd, "2": sstf_dschd, "3": scan_dschd, "4": cscan_dschd, "5": look_dschd, "6":clook_dschd}
    for i in algorithms:
        algorithms[i](req_sequence, initial_rest, seek_multiplier, total_nooftracks)
        req_sequence = list(backup_req_sequence)

caller()