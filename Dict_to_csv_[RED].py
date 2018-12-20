import csv
import xlrd
import pandas as pd
from collections import defaultdict

#load file
fl = xlrd.open_workbook('PATH/TO/DIR/art_extract.xlsx')

#load sheet (needs to be done first to specify where Python looks for data)
ffl = fl.sheet_by_index(0)

#Extract data from a specific row. In this case we want to grab the dict values in column 9 (technically column 10)
dvals = ffl.col_values(9)

#creating a dummy dictionary
ddg = defaultdict(list)

#For loop to iterate through all of the values from column 9
#each "value" is actually a dictionary so we're going to have to deconstruct each one
for i in range(len(dvals)):
	#Remove quotes so that python doesn't think it's a giant string
	dg = dvals[i].replace('"', '')
	#Removing their curly brackets because we want to build/append a single dictionary
	dg = dg.replace("{", "")
	dg = dg.replace("}", "")
	#splitting the values at the comma [and a space to remove whitespace from the values]. 
	dg = dg.split(', ')
	#for loop for each item that we generated by splitting by commas
	for tt in dg:
		#checking to make sure that the item is a key/value pair, which are always seperated by a colon
		if ':' in tt:	
			#we find the colon and we split the string there [again with a space to get rid of whitespace]
			tt = tt.split(': ')
			#If statement to check if the key exists in our dictionary yet
			if tt[0] in ddg:
				#if it does, then we just call the key values that correspond to that key and append the new value to the end of the list
				ddg[tt[0]].append(tt[1])
			else:
				#if not, then we create a new list of values for that new key
				ddg[tt[0]] = [tt[1]]

#Now we need to build the dataframe that will become the csv
#Because there are different numbers of values per column, we need to 
#tell python to generate a whole bunch of NAs to make each column the 
#same length as the longest column. -- 'min_length'

#create dummy list
llf = []
#iterate through each key in the dictionary or each column in the upcoming df
for q in ddg.keys():
	#Grab the number of values for each iterated key
	lk = len(ddg[q])
	#spit that number of values into the dummy list
	llf.append(lk)
#the 'min_length' is the highest number from that list
min_length = max(llf)

#writing the dataframe. This part gets a little weird to look at but
#what it's doing is taking each key (k), and saying that we need to
#iterate each key from 0 to our min_length. It then applies that logic
#to a mini for loop that goes though each key's values (v) and saves them
#as a value in the column. 

#If a k only has 12 vs but our min_length is 14, it will keep appending 
#rows 13 and 14 to column of name k with the values it pulls from calling
#k[13] which doesn't exist, so it will be an NA. This way we can fill in 
#the blank cells and allow the data to appear rectangular.

df = pd.DataFrame({k:pd.Series(v[:min_length]) for k,v in ddg.items()})
#Print it for the fun of it
print (df)

#save it to a location, index=False is the same as row.names = FALSE, meaning
#it won't also write a column of row numbers to the csv.
df.to_csv('PATH/TO/SAVE/DIR/art_extract_Parsed.csv', index = False)

#Boom!