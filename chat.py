#!/usr/bin/env python3

from string import whitespace,punctuation
from random import seed,randint
import pyttsx3

# databases of responses, prepopulated (add more as we go)
#     db = [ [repsonse,[previdx],[nextidx]], ... ]
database = [ ["hello",[0,1],[0,1]],
			 ["hi",[0,1],[0,1]] ]

def cleanup(query):
#	nicer input
	query = query.lower()
	query = query.strip()
	query = " ".join(query.split())
	
#	remove whitespace (except single whitespaces)
	query2 = ''
	for s in query:
		if s not in whitespace.strip():
			query2  += s

#	remove punctuation
	query3 = ''
	for s in query2:
		if s not in punctuation:
			query3 += s

	return query3



def analyze(query,previdx):	

#	loop through database for response
	for i,data in enumerate(database):

#		find if in the database
		if query == data[0]:

#			set previous query index to current query
			if len(data[1]) < 48:
				database[i][1].append(previdx)
			else:
				database[i][1][randint(0,47)] = previdx

#			set current query index for next index
			nextidx = i

#			if next responses exist...
			if len(data[2]) > 0:
#				...get random response num from given database choices
				nextidx = data[2][randint(0,len(data[2])-1)]

#				get reponse
				out = database[nextidx][0]

#				print response to terminal
				print(out)

#				speak response to speakers
				engine.say(out)
				engine.runAndWait()

#				set next query index to current query
				if len(database[i][2]) < 48:
					database[i][2].append(nextidx)
				else:
					database[i][2][randint(0,47)] = nextidx

#			break out of for loop
			break
			
	else:

#		else append query to database with previous response index
		database.append([query,[previdx],[]])

#		put this response as the next query index of the previous query 
		currentidx = len(database)-1
		if len(database[previdx][2]) < 48:
			database[previdx][2].append(currentidx)
		else:
			database[previdx][2][randint(0,47)] = currentidx

#		set current query index for next query index
		nextidx = currentidx

	return nextidx




#					 #
# main program start #
#					 #


#starting necesseties
seed()
engine = pyttsx3.init()

#set speaking rate
engine.setProperty('rate', 160)

#get details of current voice
voices = engine.getProperty('voices')
#set voice
engine.setProperty('voice', voices[3].id)

#greeting, and off we go!
print("hello")
engine.say("hello")
engine.runAndWait()
previdx = 0

#main loop
while True:

#	get user input
	query = input("> ")

#	if no user input, continue
	if query == "":
		continue

#	cleanup the query
	query = cleanup(query)

#	check for exit command
	if query == 'exit' or query == 'quit':
		exit()

#	else analyze query and set index for next loop iteration
	previdx = analyze(query,previdx)

