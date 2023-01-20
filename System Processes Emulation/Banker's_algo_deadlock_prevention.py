from os import system
from prettytable import PrettyTable

def take_input():
    machine_instances = [int(i) for i in input("Enter the machine instances: ").split()]
    noofprocesses = int(input("Enter the No. of processes: "))
    allocations = []
    max_needs = []

    for i in range(0, noofprocesses):
        print(f"\nFor Process P{i + 1}: ")
        temp = [int(x) for x in input("Enter Allocation instances: ").split()][:len(machine_instances)] #! slicing done to prevent overfilling
        allocations.append(temp)

        temp = [int(x) for x in input("Enter Max Need instances: ").split()][:len(machine_instances)]
        max_needs.append(temp)

    return machine_instances, allocations, max_needs

def calculate_available_inst_1(machine_instances, allocations):
    sumof_allocations = []
    col_sum = 0
    
    for i in range(0, len(machine_instances)):
        for j in range(0, len(allocations)):
            col_sum += allocations[j][i]
        sumof_allocations.append(col_sum)
        col_sum = 0
    
    return ([k - l for k, l in zip(machine_instances, sumof_allocations)])

def calculate_remaining_needs(max_needs, allocations):
    remaining_needs = []
    
    for i, j in zip(max_needs, allocations):
        indv_remaining_needs = [k - l for k, l in zip(i, j)]
        remaining_needs.append(indv_remaining_needs)
    
    return remaining_needs

def table_print(allocations, max_needs, remaining_needs):
    noofprocesses = len(max_needs)
    Table = PrettyTable(["Process No", "Allocation", "Max", "Remaining"])
    
    for i in range(noofprocesses):
        allocations_str = ""
        for c in allocations[i]:
            allocations_str += (str(c) + " ")
        
        max_needs_str = ""
        for c in max_needs[i]:
            max_needs_str += (str(c) + " ")
        
        remaining_needs_str = ""
        for c in remaining_needs[i]:
            remaining_needs_str += (str(c) + " ")
        
        Table.add_row([i + 1, allocations_str, max_needs_str, remaining_needs_str])
    
    return Table

def bankers_algorithm():
    system("cls")
    machine_instances, allocations, max_needs = take_input()
    remaining_needs = calculate_remaining_needs(max_needs, allocations)
    available = []
    available.append(calculate_available_inst_1(machine_instances, allocations))
    noofprocesses = len(max_needs)
    
    Table = table_print(allocations, max_needs, remaining_needs)
    print("\033[1m\033[4m\033[38;5;177mGiven Information: \033[0m\n", Table)
    print("Initial available resources: ", available[0])

    i = 0
    j = 0
    deadlock = 0
    scheduled = 0
    prev_cycle_scheduled = 0
    schd_list = []
    is_completed = [False for i in allocations]

    while(deadlock != 1 and (scheduled != noofprocesses)): #* while it is not a deadlock and not all processes have been scheduled
        if(is_completed[i] == False):
            pa = allocations[i]
            rn = remaining_needs[i]
            av = available[j]
            can_fulfill = True

            for m, n in zip(rn, av):
                if m > n:
                    can_fulfill = False
            
            if(can_fulfill == True):
                available.append((lambda a, b: [k + l for k, l in zip(a, b)])(pa, av)) #* returns a list which has the sum of individual elements of pa and av
                j += 1
                is_completed[i] = True
                scheduled += 1
                schd_list.append(i + 1)

        i += 1    
        if(i == noofprocesses):  
            if(prev_cycle_scheduled == scheduled):
                deadlock = 1
            else:
                prev_cycle_scheduled = scheduled
                i = 0
    
    if deadlock == 1:
        print("\n\033[1m\033[38;5;196mDeadlock Occurred! The system is in an unsafe state!\033[0m")
    else:
        print("\n\033[1m\033[38;5;158mThe system is in a safe state!\n\033[38;5;225m\033[4mSafe sequence:\033[0m")
        for i in schd_list:
            if i != schd_list[-1]:
                print("P" + str(i) + "\033[38;5;216m ⮞ \033[0m", end = "")
            else:
                print("P" + str(i))

bankers_algorithm()