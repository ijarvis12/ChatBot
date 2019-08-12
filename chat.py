#!/usr/bin/env python3

from string import whitespace,punctuation
from random import seed,randint
import pyttsx3

# databases of responses, prepopulated
database = [ ["hello",[0,1]],
			 ["hi",[0,1]] ]

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
#		if in the database, print response
		if query == data[0]:
#			set previous query iteration
			if len(data[1]) < 48:
				database[i][1].append(previ)
			else:
				database[i][1][i%48] = previ
#			set var for next query iteration
			previ = i
#			random response from given choices in database	        
			outnum = data[1][randint(0,len(data[1]))-1]
#			get reponse
			out = database[outnum][0]
#			print response to terminal
			print(out)
#			speak response to speakers
			engine.say(out)
			engine.runAndWait()
#			break out of for loop
			break
			
#	else append query to database with previous response
	else:
		database.append([query,[previ]])
		
#		set var for next query iteration
		previ = len(database)-1


	return previ





# main program start

#starting necesseties
seed()
engine = pyttsx3.init()
# getting details of current speaking rate
rate = engine.getProperty('rate')
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
#	cleanup the query
	query = cleanup(query)
	#check for exit command
	if query == 'exit':
		break
#	else analyze query and set index for next loop iteration
	previ = analyze(query,previ)
	
