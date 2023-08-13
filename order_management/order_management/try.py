import os
# create a function that reads the file and returns the number of lines
def count_lines(file_name):
    with open(file_name, 'r') as f:
        return len(f.readlines())

# create a function that reads the file and returns the number of characters
def count_characters(file_name):
    with open(file_name, 'r') as f:
        return len(f.read())


#access the file in the folder data out of the order_management folder

current_folder = os.path.dirname(os.path.abspath(__file__))
data_folder = os.path.abspath(os.path.join(current_folder, '../../data')) 


print(count_lines(file_name))
print(count_characters(file_name))