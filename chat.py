#!/usr/bin/env python3

from string import whitespace,punctuation
from random import seed,randint

#databases of responses, prepopulated
database = [ ["hello",[0,1]],
			 ["hi",[0,1]] ]

def analyze(query,previ):
#   nicer input
	query = query.lower()
	query = query.strip()
	query = " ".join(query.split())
	
#	forget whitespace (except single whitespaces)
	query2 = ''
	for s in query:
		if s not in whitespace.strip():
			query2  += s

#   forget punctuation
	query3 = ''
	for s in query2:
		if s not in punctuation:
			query3 += s

#	cleanup
	query = query3
	del query2
	del query3
	
#   loop through database for response
	for i,data in enumerate(database):
#       if in the database, print response
		if query == data[0]:
			if len(data[1]) < 48:
				database[i][1].append(previ)
			else:
				database[i][1][i%48] = previ
#			set var for next query iteration
			previ = i
#           random response from given choices in database	        
			outnum = data[1][randint(0,len(data[1]))-1]
			out = database[outnum][0]
			print(out)
			break
			
#   else append query to database with previous response
	else:
		database.append([query,[previ]])
		
#		set var for next query iteration
		previ = len(database)-1


	return previ





#main program

seed()
print("print 'hello' or 'hi' to start")
query = input("> ")
previ = analyze(query,0)
while True:
	query = input("> ")
	previ = analyze(query,previ)
