#!/usr/bin/env python3

from string import whitespace,punctuation
from random import seed,randint
import pyttsx3

# databases of responses, prepopulated (add more as we go)
#			  repsonse,previ,nexti
database = [ ["hello",[0,1],[0,1]],
			 ["hi",[0,1],[0,1]] ]

def cleanup(query):
#	nicer input
	query = query.lower()
	query = query.strip()
	query = " ".join(query.split())
	
#	forget whitespace (except single whitespaces)
	query2 = ''
	for s in query:
		if s not in whitespace.strip():
			query2  += s

#	forget punctuation
	query3 = ''
	for s in query2:
		if s not in punctuation:
			query3 += s

	return query3



def analyze(query,previ):	

#	loop through database for response
	for i,data in enumerate(database):

#		find if in the database
		if query == data[0]:

#			set previous query iteration
			if len(data[1]) < 48:
				database[i][1].append(previ)
			else:
				database[i][1][i%48] = previ

#			set next query iteration for the previous
			if len(data[2]) < 48:
				database[previ][2].append(i)
			else:
				database[previ][2][previ%48] = i

#			set var for next query iteration
			previ = i

#			if next responses exist...
			if len(data[2]) > 0:
#				...get random response num from given database choices
				outnum = data[2][randint(0,len(data[2]))-1]

#				get reponse
				out = database[outnum][0]

#				print response to terminal
				print(out)

#				speak response to speakers
				engine.say(out)
				engine.runAndWait()

#			break out of for loop
			break
			
	else:

#		else append query to database with previous response
		database.append([query,[previ],[]])

#		add next query response to previous
		database[previ][2].append(len(database)-1)

#		set var for next query iteration
		previ = len(database)-1

	return previ




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
previ = 0

#main loop
while True:
#	get user input
	query = input("> ")
	if query == "":
		continue
#	cleanup the query
	query = cleanup(query)
#	check for exit command
	if query == 'exit':
		break
#	else analyze query and set index for next loop iteration
	previ = analyze(query,previ)

