import pandas as pd
import argparse

def diff(a, b):
    return [aa for aa in a if aa not in set(b)]

# Example call: python csv_to_json.py --filepath "data/all_data.csv" --group-by 3

parser = argparse.ArgumentParser(description='Convert CSV to JSON with nesting')
parser.add_argument('--filepath', type=str)
parser.add_argument('--group-by', type=int, default=0)
args = parser.parse_args()

data = pd.read_csv(args.filepath, header=0, delimiter=",", quoting=1, index_col=0 )

data = data[:100]

data.to_json("data.json", orient="records")


"""
columns = len(data)

if args.group_by >= columns:
    print("Specified columns to group by larger than number number of columns in the dataset")

# Get Column Names from Dataset
all_cols = list(data.columns.values)
grouping_cols = all_cols[0:(args.group_by)]
value_cols = diff(all_cols, grouping_cols)

# Get Unique Combinations from Grouping Columns
unique_data = data[grouping_cols]
combinations = unique_data.drop_duplicates()

#print(combinations.loc[1:2])

#print(combinations.at[1, "Municipality"])
#print(data.loc[(data[grouping_cols[0]] == combinations.at[1, grouping_cols[0]]) & (data[grouping_cols[1]] == combinations.at[1, grouping_cols[1]])])

# Loop Through Records Matching Against Criteria
final_output = {}
j = 0

#for rows in combinations.index:
while j <= 1:
    query = ""
    nesting_start = ""
    nesting_end = ""
    i = 0
    index = combinations.index[j]
    while i <= (args.group_by - 1):
        if i == 0:
            query = query + "records = (data.loc[(data[grouping_cols[" + str(i) + "]] == combinations.at[" + str(index) + ", grouping_cols[" + str(i) + "]])"
            nesting_start = nesting_start + "{\"" + grouping_cols[i] + "\": \"" + combinations.at[index, grouping_cols[i]] + "\", \"Children\": "
        else:
            query = query + "\n& (data[grouping_cols[" + str(i) + "]] == combinations.at[" + str(index) + ", grouping_cols[" + str(i) + "]])"
            nesting_start = nesting_start + "[{\"" + grouping_cols[i] + "\": \"" + combinations.at[index, grouping_cols[i]] + "\", \"Children\": "
        nesting_end = nesting_end + "}]"
        i = i + 1
    query = query + "])"
    exec query
    records = records.to_dict(orient="records")
    print(nesting_start + str(records) + nesting_end)
    #final_dict = nesting + str() + 
    #records = {}
    #final_output = final_output + {records
    j = j + 1

#print(final_output)

#values = {}
#for col in grouping_cols:
#    values[col] = {"values":list(data[col].unique())}
#    df.loc[df['column_name'] == some_value]
"""
        


