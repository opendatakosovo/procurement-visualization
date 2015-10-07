#!/usr/local/bin/python3.1
import pandas as pd
import argparse
import json

# Example calls: 
# python csv_to_json.py --filepath "data/all_data.csv" --group-by 3
# python csv_to_json.py --filepath "data/all_data.csv" --colnames Municipality Fund\ Source --filter-col Year --filter-val 2011 --limit 50

#-------------------------------------------
# Recursive Function
#-------------------------------------------
def inner_loop(data, array, current_level, total_levels, nest_cols=None, name = "name", children="children", sum_value = None, avg_value = None, count_field = True):
    
    #Extract column name
    if nest_cols == None:
        colname = list(data.columns.values)[(current_level - 1)]
    else:
        colname = nest_cols[current_level - 1]   
    
    # Extract Levels for Current Column
    levels = data[colname].drop_duplicates().values.tolist()
    
    #Loop through levels
    i = 0
    for level in levels:
        
        # Create empty children subarray
        array[children].insert(i, {})
        array[children][i][children] = {}
        
        # If further nesting required
        if current_level < total_levels:
            new_level = current_level + 1
            subdata = data.loc[data.loc[ : , colname] == level, : ]
            new_array = {children : []}
            subarray = inner_loop(subdata, new_array, new_level, total_levels, nest_cols, name, children, sum_value, avg_value, count_field)
            array[children][i] = subarray
            
        # Else if all nesting completed
        elif current_level == total_levels:
            other_values = data.loc[data.loc[ : , colname] == level, : ].to_dict(orient = "records")
            array[children][i][children] = other_values
        
        # Add Meta Values for current Level
        array[children][i][name] = level
        if sum_value != None:
            array[children][i][sum_value] = data.loc[data.loc[ : , colname] == level, sum_value].sum()
        if avg_value != None:
            array[children][i][avg_value] = data.loc[data.loc[ : , colname] == level, avg_value].mean()
        if count_field:
            array[children][i]["count"] = len(data.loc[data.loc[ : , colname] == level, ].index)
        
        i += 1
    
    return array

#-------------------------------------------
# Script
#-------------------------------------------

# Process Arguments
parser = argparse.ArgumentParser(description='Convert CSV to JSON with nesting')
parser.add_argument('--filepath', type=str)
parser.add_argument('--group-by', type=int, default=0)
parser.add_argument('--colnames', type=str, nargs='*')
parser.add_argument('--filter-col', type=str)
parser.add_argument('--filter-val', type=str)
parser.add_argument('--limit', type=int)

args = parser.parse_args()

# Initialize field names
name_field = "name"
child_field = "children"
sum_field = "value"
avg_field = "overun_%"
root_node = "Procurement Data"
current_level = 1

# Load in Dataset
data = pd.read_csv(args.filepath, header=0, delimiter=",", quoting=1, index_col=0)

if args.filter_col and args.filter_val:
    data = data.loc[data.loc[ : , args.filter_col].astype(str) == str(args.filter_val), : ]
    
if args.limit:
    data = data[:args.limit]

root_avg = data.loc[ : , avg_field].mean()

# Check if column names were passed and use if able
if args.colnames:
    col_names = args.colnames
    total_levels = len(col_names)
else: 
    col_names = None
    total_levels = args.group_by

#Initialize Array
array = {name_field: root_node
        , avg_field : root_avg
        , child_field : []
    }

# Begin Recursion
array = inner_loop(data = data
    , array = array
    , current_level = current_level
    , total_levels  = total_levels
    , nest_cols = col_names
    , name = name_field
    , children = child_field
    , sum_value = sum_field
    , avg_value = avg_field
    )

# Convert to JSON format
json_array = json.dumps(array, indent = 4, ensure_ascii = False)
print(json_array)

