#!/usr/bin/env python3

from random import seed,randint
import pyttsx3
import sqlite3

# main database table
# responses
# id | response
#
# supporting database tables
# [query]_prev
# previdx
#
# [query]_next
# nextidx

#turn query into table name
def turn(query):
	return "_".join(query.split(" "))



#create the db and/or connect
def createDBifnone():

#	try to connect to db and retrieve entry
	try:
		c.execute('SELECT * FROM responses LIMIT 1')

	except:

#		create responses table and populate with one entry
		c.execute('''CREATE TABLE responses
		(id INT PRIMARY KEY NOT NULL, response VARCHAR(255) NOT NULL)''')
		c.execute("INSERT INTO responses VALUES (0,'hello')")

#		create previous response index table for first response
		c.execute('CREATE TABLE hello_prev(previdx INT NOT NULL)')
		c.execute("INSERT INTO hello_prev VALUES (0)")

#		create next response index table for first response
		c.execute('CREATE TABLE hello_next(nextidx INT)')
		c.execute("INSERT INTO hello_next VALUES (0)")

#		commit changes
		conn.commit()

		return



#cleanup the query
def cleanup(query):

#	nicer input
	query = query.lower()
	query = query.strip()
	query = " ".join(query.split())
	
#	only keep alpha numerics
	query2 = ''
	for char in query:
		if char.isalnum():
			query2 += char
		elif char == ' ':
			query2 += char

	return query2



#query search, display, add to db
def searchdisplayadd(query,previdx):	

#	initialize next response index
	nextidx = 0

#	table name and query tuple
	table = turn(query)
	query = (query,)

#	try searching and getting current query index
	try:
		c.execute('SELECT * FROM responses WHERE response=?', query)
		currentidx = int(c.fetchone()[0])

#		add previous response index to current response table
		c.execute("INSERT INTO {} VALUES (?)".format(table+"_prev"),(previdx,))

#		set current response index for next index
		nextidx = currentidx

#		if next responses exist...
		try:
			c.execute("SELECT * FROM {}".format(table+"_next"))
			options = c.fetchall()

#			...get random response index from given database choices
			nextidx = int(options[randint(0,len(options)-1)][0])
			c.execute("SELECT * FROM responses WHERE id=?", (nextidx,))
			out = str(c.fetchone()[1])

#			print response
			print(out)

#			speak response
			engine.say(out)
			engine.runAndWait()

#			set next response index to current response
			c.execute("INSERT INTO {} VALUES (?)".format(table+"_next"),(nextidx,))

#		...otherwise skip
		except:
			pass

#	if no entry add it to dbs
	except:
		c.execute('SELECT COUNT(id) FROM responses')
		idnum = int(c.fetchone()[0])
		c.execute('INSERT INTO responses VALUES (?,?)', (idnum,query[0]))
		c.execute('CREATE TABLE {}(previdx INT NOT NULL)'.format(table+"_prev"))
		c.execute("INSERT INTO {} VALUES (?)".format(table+"_prev"), (previdx,))
		c.execute('CREATE TABLE {}(nextidx INT)'.format(table+"_next"))

#		set the new index as the next response index of the previous response
		newidx = idnum
		c.execute('SELECT * FROM responses WHERE id=?', (previdx,))
		prevresponse = str(c.fetchone()[1])
		prevresponse = turn(prevresponse)
		c.execute("INSERT INTO {} VALUES (?)".format(prevresponse+"_next"),(newidx,))

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
conn = sqlite3.connect('chat.db')
c = conn.cursor()
createDBifnone()

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

#		close db connection
		c.close()
		conn.close()

#		quit
		exit()

#	else analyze query and set index for next loop iteration
	previdx = searchdisplayadd(query,previdx)

#	save changes to dbs
	conn.commit()

