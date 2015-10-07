#!/usr/local/bin/python3.1
import pandas as pd
import argparse
import json

# Example call: python csv_to_json.py --filepath "data/all_data.csv" --group-by 3

#-------------------------------------------
# Recursive Function
#-------------------------------------------
def inner_loop(data, array, current_level, total_levels, name = "name", children="children", sum_value = None, avg_value = None, count_field = True):
    
    #generate column name and levels
    colname = list(data.columns.values)[(current_level - 1)]
    levels = data[colname].drop_duplicates().values.tolist()
    i = 0
    
    #Loop through levels
    for level in levels:
        
        # Create empty children subarray
        array[children].insert(i, {})
        array[children][i][children] = {}
        
        # If further nesting required
        if current_level < total_levels:
            new_level = current_level + 1
            subdata = data.loc[data.loc[ : , colname] == level, : ]
            new_array = {children : []}
            subarray = inner_loop(subdata, new_array, new_level, total_levels, name, children, sum_value, avg_value, count_field)
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
args = parser.parse_args()

name_field = "name"
child_field = "children"
sum_field = "value"
avg_field = "overun_%"
root_node = "Procurement Data"

# Load in Dataset
data = pd.read_csv(args.filepath, header=0, delimiter=",", quoting=1, index_col=0 )
#data = data[1000:1050]

root_avg = data.loc[ : , avg_field].mean()

# Initialize Recursion
array = {name_field: root_node
        , avg_field : root_avg
        , child_field : []
    }

total_levels = args.group_by
current_level = 1

array = inner_loop(data = data
    , array = array
    , current_level = current_level
    , total_levels  = total_levels
    , name = name_field
    , children = child_field
    , sum_value = sum_field
    , avg_value = avg_field
    )

json_array = json.dumps(array, indent = 4, ensure_ascii = False)
print(json_array)

