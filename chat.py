#!/usr/bin/env python3

from string import punctuation

def analyze(query):
	query = query.lower()
	query2 = ''
	
	for s in query:
		if s in punctuation:
			pass
		else:
			query2 += s
	
	if query2[:4] == "what":
	    print("what do you think?")
	elif query2[:5] == "where":
	    print("where do you think?")
	elif query2[:4] == "when":
	    print("when do you think?")
	elif query2[:3] == "why":
	    print("why do you think?")
	elif query2[:3] == "how":
	    print("how do you think?")
	else:
		print('tell me more...')

#main program

print('hello')
while True:
	query = input("> ")
	analyze(query)
