from os import system

def take_input():
    ref_string = [int(i) for i in input("Enter the Reference String: ").split()]
    memory = [-1 for i in range(0, int(input("Enter the no. of frames in the memory: ")))]

    return ref_string, memory

def fifo_page_rpmt(ref_string, memory):
    faults = 0
    hits = 0
    to_place_index = 0
    flag = 0
    noofrefs = len(ref_string)
    noofframes = len(memory)
    print("\n")

    for ref in ref_string:
        for frame in memory:
            if(frame == ref):
                hits += 1
                flag = 1
        
        if(flag == 0):
            faults += 1
            memory[to_place_index] = ref
            to_place_index = (to_place_index + 1) % (noofframes)
        flag = 0                    
        print("| Reference: \033[1m\033[38;5;117m{}\033[0m | Current Memory: {} | Fault count: \033[1m\033[38;5;196m{}\033[0m | Hit count: \033[1m\033[38;5;156m{}\033[0m".format(ref, memory, faults, hits))
    
    print("\n\033[1m\033[4m\033[38;5;122mResults\033[0m")
    print(f"No. of Hits: \033[38;5;156m{hits}\033[0m\nNo. of Faults(Miss): \033[38;5;196m{faults}\033[0m\nHit Ratio: \033[38;5;156m{hits}/{noofrefs}\033[0m\nFault(Miss) Ratio: \033[38;5;196m{faults}/{noofrefs}\033[0m\n")

def lru_page_rpmt(ref_string, memory):
    faults = 0
    hits = 0
    to_place_index = 0
    flag = 0
    noofrefs = len(ref_string)
    page_in_frame_age = [(i + 996) for i in range(len(memory)-1, -1, -1)]
    print("\n")

    for ref in ref_string:
        for frame in memory:
            if(frame == ref):
                hits += 1
                page_in_frame_age[memory.index(ref)] = 0        #! resetting age, when hit
                flag = 1

        if(flag == 0):
            faults += 1
            to_place_index = page_in_frame_age.index(max(page_in_frame_age))
            page_in_frame_age[to_place_index] = 0 
            memory[to_place_index] = ref
        flag = 0    
        page_in_frame_age = list(map(lambda x: x + 1, page_in_frame_age)) #! incrementing all pages in frame's age at the end of each iteration
        print("| Reference: \033[1m\033[38;5;117m{}\033[0m | Current Memory: {} | Fault count: \033[1m\033[38;5;196m{}\033[0m | Hit count: \033[1m\033[38;5;156m{}\033[0m".format(ref, memory, faults, hits))

    print("\n\033[1m\033[4m\033[38;5;122mResults\033[0m")
    print(f"No. of Hits: \033[38;5;156m{hits}\033[0m\nNo. of Faults(Miss): \033[38;5;196m{faults}\033[0m\nHit Ratio: \033[38;5;156m{hits}/{noofrefs}\033[0m\nFault(Miss) Ratio: \033[38;5;196m{faults}/{noofrefs}\033[0m\n")

def optimal_page_rpmt(ref_string, memory):
    faults = 0
    hits = 0
    to_place_index = 0
    flag = 0
    noofrefs = len(ref_string)
    curr_pages_in_frames_future = [-1 for i in memory]
    
    def find_future_occurence():
        for i in range(0, len(memory)):
            try:
                curr_pages_in_frames_future[i] = ref_string[curr_index:].index(memory[i])
            except ValueError:                          #there is no future occurence of page in frame in memory[i], highest priority to replace
                curr_pages_in_frames_future[i] = 999
    
    curr_index = 0    #simpler to control the for-in loop in this case
    for ref in ref_string:
        for frame in memory:
            if(frame == ref):
                hits += 1
                flag = 1
        
        if(flag == 0):
            faults += 1
            find_future_occurence()
            to_place_index = curr_pages_in_frames_future.index(max(curr_pages_in_frames_future))
            memory[to_place_index] = ref
        flag = 0
        curr_index += 1
        
        print("| Reference: \033[1m\033[38;5;117m{}\033[0m | Current Memory: {} | Fault count: \033[1m\033[38;5;196m{}\033[0m | Hit count: \033[1m\033[38;5;156m{}\033[0m".format(ref, memory, faults, hits))
    
    print("\n\033[1m\033[4m\033[38;5;122mResults\033[0m")
    print(f"No. of Hits: \033[38;5;156m{hits}\033[0m\nNo. of Faults(Miss): \033[38;5;196m{faults}\033[0m\nHit Ratio: \033[38;5;156m{hits}/{noofrefs}\033[0m\nFault(Miss) Ratio: \033[38;5;196m{faults}/{noofrefs}\033[0m\n")

def caller():
    system("cls")
    ref_string, memory = take_input()
    algorithms = {1: fifo_page_rpmt, 2: lru_page_rpmt, 3: optimal_page_rpmt}
    algorithms[int(input("Enter the algorithm to be used:\n1. FIFO\n2. LRU\n3. Optimal: "))](ref_string, memory) #! calling a value of the dictionary which is a function hence parameters are also passed here

caller() 