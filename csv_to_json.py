#!/usr/local/bin/python3.1
import pandas as pd
import argparse
import pprint
import json
import sys
sys.setrecursionlimit(10000)

# Example call: python csv_to_json.py --filepath "data/all_data.csv" --group-by 3

#-------------------------------------------
# Functions
#-------------------------------------------
def diff(a, b):
    return [aa for aa in a if aa not in set(b)]
    
def inner_loop(data, array, current_level, total_levels):
    
    #generate column name and levels
    colname = list(data.columns.values)[(current_level - 1)]
    levels = data[colname].drop_duplicates().values.tolist()
    original_data = data
    i = 0
    mapping = [0, 0, 0, 0]
    
    #Loop through levels
    for level in levels:
        mapping[current_level - 1] = i
        
        # Nesting string
        nesting = "array"
        j = 1
        
        while j <= current_level:
            if j <= current_level:
                nesting = nesting + "[\"children\"]" + "[" + str(mapping[j-1]) + "]"
            #elif j == current_level:
            #    nesting = nesting + "[\"children\"]"
            j = j + 1
        
        query = nesting + "[\"name\"] = \"" + level + "\""
        print(query)
        exec query
       
        query = nesting + "[\"value\"] = data[\"Total\"].sum()"
        exec query
        
        query = nesting + "[\"overun_%\"] = data[\"overun_%\"].mean()"
        exec query
        
        query = nesting + "[\"children\"] = []"
        exec query

        # If further nesting required
        if current_level < total_levels:
            new_level = current_level + 1
            data = data.loc[data.loc[ : , colname] == level, : ]
            subarray = inner_loop(data, array, new_level, total_levels)
            query = nesting + "[\"children\"] = subarray"
            exec query
            
        # Else if all nesting completed
        elif current_level == total_levels:
            query = nesting + "[\"children\"] = {\"Item 1\":\"A\", \"Item 2\":\"B\",\"Item 3\":\"C\"}"
            exec query
            
        data = original_data
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

# Load in Dataset
data = pd.read_csv(args.filepath, header=0, delimiter=",", quoting=1, index_col=0 )
data = data[1000:1100]

# Initialize Recursion
array = {"name": "Procurement Data"
        , "overun_%" : 0.5
        , "value": 1000
        , "children": [{}]
    }
total_levels = args.group_by
current_level = 1

array = inner_loop(data = data
    , array = array
    , current_level = current_level
    , total_levels  = total_levels
    )

pp = pprint.PrettyPrinter(indent=4)
pp.pprint(array)
#with open("my.json","w") as f:
#    json.dump(array,f, check_circular = False)




