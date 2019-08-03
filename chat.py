#!/usr/bin/env python3

from string import punctuation

database = []

def analyze(query):
	query = query.lower()
	query2 = ''
	for s in query:
		if s in punctuation:
			pass
		else:
			query2 += s
	if query2 in database:
		try:
			print(database[database.index(query2)+1])
		except:
			pass
	else:
		database.append(query2)
		print('tell me more...')

print('hello')
while True:
	query = input("> ")
	analyze(query)
