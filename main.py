import os
import csv
import pandas as pd

# converts the csv file into a Python list
def csv_to_list(filename, delim=','):
    filename = filename
    file_obj = open(filename, "r")
    data = list(csv.reader(file_obj, delimiter=delim, quoting=csv.QUOTE_NONE)) # using QUOTE_NONE means we can only run this script once, or else each iteration would add extra quotes
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

# html encoding quotes where quote count is uneven due to mistake in data entries
def fix_quotes(data):
    
    for i in range(1, len(data)):
        for j in range(len(data[i])):
            quote_count = data[i][j].count("\"")
            # if uneven amount of quotes replace all
            if quote_count % 2 != 0:
                data[i][j] = data[i][j].replace("\"", "&quot;")
                continue
                
            # replace all quotes not in first and last position if even
            if len(data[i][j]) > 2:
                first_char = data[i][j][0]
                last_char = data[i][j][-1]
                ignore_first_last = data[i][j][1:-1]
                data[i][j] = first_char + ignore_first_last.replace('\"', '&quot;') + last_char
                
                # if data[i][j] is still uneven at this point that means that any quote at the first or last position
                # is part of the string
                if data[i][j].count("\"") % 2 != 0:
                    data[i][j] = data[i][j].replace("\"", "&quot;")
    
                # an issue that may arise if quote1 and quote2 are not surrounded by extra quotes:
                # "quote1" and "quote2"
                # "quote1&quot; and &quot;quote2"
                if data[i][j][0] == "\"" and data[i][j][-1] == "\"":
                    data[i][j] = data[i][j][1:-1]
                    
            if data[i][j].count("&quot;") % 2 != 0:
                print(f"imbalanced quotes in row {i} col {j}: {data[i][j]}") 
                
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
        try:
            w = csv.writer(f, delimiter=delim)
            w.writerow(data[0])
            w.writerows(data[1:])
        except:
            print(f"error rewriting csv in: {filename}")
        

if __name__ == "__main__":
    delim = '|'
    files = [f for f in os.listdir('.') if os.path.isfile(f) and f.startswith('RD_')] #and f.startswith('RD_')
    
    for f in files:
        data = csv_to_list(f, delim=delim)
        num_cols = len(data[0])
        data_fixed = fix_line_breaks(data)
        data_fixed_quotes = fix_quotes(data_fixed)
        check_line_breaks(f,data_fixed_quotes, num_cols)
        save_to_csv(f, data_fixed_quotes, delim=delim)
