#!/usr/bin/env python3

from string import punctuation
from random import seed,randint

database = [ ["hello",[0,1]],
			 ["hi",[0,1]] ]

def analyze(query):
#   nicer input
	query = query.lower()

#   forget punctuation
	query2 = ''
	for s in query:
		if s in punctuation:
			pass
		else:
			query2 += s
	
#   loop through database for response
	for data in database:
#       if in the database, print response
		if query2 is data[0]:
#           random response from given choices in database	        
			outnum = data[1][randint(0,len(data[1]))-1]
			out = database[outnum][0]
			print(out)
			
#   else append query with random response
	else:
		database.append([query2,[randint(0,len(database))-1]])
        


#main program

seed()
print("print 'hello' or 'hi' to start")
while True:
	query = input("> ")
	analyze(query)
