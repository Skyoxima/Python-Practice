def sort_by_pattern(pattern, string): 
    priority = list(pattern)
    priority_dict = {priority[i] : i for i in range(len(priority))}
    string_list = list(string)
    string_list.sort(key = lambda x: priority_dict[x])
    string_list.reverse()
    sorted_string = ''.join(string_list)
    return sorted_string

pattern = "asbcklfdmegnot"
string = "eksge"
decoded_str = sort_by_pattern(pattern, string)
print(decoded_str)