import os
import csv
import pandas as pd

# converts the csv file into a Python list
def csv_to_list(filename, delim=','):
    filename = filename
    file_obj = open(filename, "r")
    data = list(csv.reader(file_obj, delimiter=delim, quoting=csv.QUOTE_NONE))
    file_obj.close()
        
    return data

# fixes new line breaks from the csv list
def fix_line_breaks(data):
    i = 0
    while i < len(data) - 1:
        while len(data[i]) < num_cols:
            if len(data[i+1]) == 0:
                data.pop(i+1)
            else:
                data[i][-1] += f" {data[i+1][0]}"
                to_add = data.pop(i+1)
                data[i] += to_add[1:]
        i += 1
    return data

# checks if all rows match the necessary number of columns
def check_line_breaks(filename, data, num_cols):
    print(filename)
    for i in range(len(data)):
        if len(data[i]) != num_cols:
            print(f"{filename} - row:{i}, numcols:{num_cols}, length:{len(data[i])}")

# save python list as csv
def save_to_csv(filename, data, delim=','):
    with open(filename, "w") as f:
        w = csv.writer(f, delimiter=delim)
        w.writerow(data[0])
        w.writerows(data[1:])

if __name__ == "__main__":
    delim = '|'
    files = [f for f in os.listdir('.') if os.path.isfile(f) and f.startswith('RD_')]
    
    for f in files:
        data = csv_to_list(f, delim=delim)
        num_cols = len(data[0])
        data_fixed = fix_line_breaks(data)
        check_line_breaks(f,data_fixed, num_cols)
        save_to_csv(f, data_fixed, delim=delim)
