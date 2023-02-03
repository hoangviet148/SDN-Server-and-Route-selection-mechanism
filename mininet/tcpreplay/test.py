import numpy as np

list_of_lists = [[1, 2, 3], [1, 2]]


# Determine the maximum length of the lists
max_len = max(len(lst) for lst in list_of_lists)

# Pad each list with the default value (0 in this case)
padded_list_of_lists = [lst + [0] * (max_len - len(lst)) for lst in list_of_lists]

# Convert the list of lists to a 2D NumPy array
array = np.array(padded_list_of_lists)

print(array)