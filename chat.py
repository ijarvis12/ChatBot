#!/usr/bin/env python3

from string import whitespace,punctuation
from random import seed,randint
import pyttsx3

# database of responses, prepopulated (add more as we go)
#     db = [ [repsonse,[previdx],[nextidx]], ... ]
database = []

def extractdbinfo():
#	open db file
	try:
		file = open("chatdb.dat",'r')
	except:
		file = open("chatdb.dat",'x')
		file.write("['hello', [0], [0]]\n")
		file.close()
		file = open("chatdb.dat",'r')

#	extract data
	for line in file:

#		extraction list from data line in file
		extract = line[1:-2].split(", ")

#		extract response
		response = extract[0].strip("'")

#		extract previous response indices
		pindices = extract[1].strip("[]").split(",")
		previdcs = []
		for indx in pindices:
			previdcs.append(int(indx))

#		extract next response indices
		nindices = extract[2].strip("[]").split(",")
		nextidcs = []
		if nindices[0] != '':
			for indx in nindices:
				nextidcs.append(int(indx))

#		add to db in memory
		database.append([response,previdcs,nextidcs])

#	close db file
	file.close()



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

#	initialize next response index
	nextidx = 0

#	loop through database for response
	for currentidx,data in enumerate(database):

#		find if in the database
		if query == data[0]:

#			set previous response index to current response
			if len(data[1]) < 48:
				database[currentidx][1].append(previdx)
			else:
				database[currentidx][1][randint(0,47)] = previdx

#			set current response index for next index
			nextidx = currentidx

#			if next responses exist...
			if len(data[2]) > 0:
#				...get random response index from given database choices
				nextidx = data[2][randint(0,len(data[2])-1)]

#				get reponse
				out = database[nextidx][0]

#				print response to terminal
				print(out)

#				speak response to speakers
				engine.say(out)
				engine.runAndWait()

#				set next response index to current response
				if len(database[currentidx][2]) < 48:
					database[currentidx][2].append(nextidx)
				else:
					database[currentidx][2][randint(0,47)] = nextidx

#			break out of for loop
			break
			
	else:

#		else append query to database with previous response index
		database.append([query,[previdx],[]])

#		set the new index as the next response index of the previous response
		newidx = len(database)-1
		if len(database[previdx][2]) < 48:
			database[previdx][2].append(newidx)
		else:
			database[previdx][2][randint(0,47)] = newidx

#		set new index to next response index
		nextidx = newidx

#	return next response index (tuns into previous response index in main loop)
	return nextidx




#					 #
# main program start #
#					 #


#starting necesseties
seed()
engine = pyttsx3.init()
extractdbinfo()

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

#		write database to file for future
		file = open("chatdb.dat",'w')
		for data in database:
			file.write(str(data)+"\n")

		#close db file
		file.close()

#		quit
		exit()


#	else analyze query and set index for next loop iteration
	previdx = analyze(query,previdx)

