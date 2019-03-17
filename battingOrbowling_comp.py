#how to get a measure of batting or bowling strength? why it's simple!
#take top-100 rankings list at given period... what is score held by #1 player?
#normalise against this score (i.e. this score now equivalent to 1)
#add up top 8 normalised scores for each nation's top 8 players in top 100
#(8 an arbitrary number yes, but seems to be fair, on the evidence
#(8 players in top 100 means good depth, but above 8 we just bias nations...
#that chop and change, and ingrain bias against minnows))
#now we normalise against nation with highest total of normalised scores..
#this nation has overall bowling/batting strength 1... others have 0.a

import csv

maindict = { "AUS":[0,0], "SA":[0,0], "IND":[0,0], "NZ":[0,0], "WI":[0,0], "PAK":[0,0], "BAN": [0,0], "AFG": [0,0], "SL": [0,0], "IRE": [0,0], "ZIM": [0,0], "ENG": [0,0], "SCO": [0,0], "CAN": [0,0], "NED": [0,0], "KEN": [0,0]}

j = 0

topValue = 0
with open('[insert cute name for list of 100 rankings here]') as file:
	reader = csv.reader(file)
	for row in reader:
		if j == 0:
			j += 1
			continue
		if j == 1:
			topValue = int(row[1])
			print('[insert cute heading for output here]\n' + row[1])
			j += 1
		#excluding the super miniature minnows... these three countries are the ones to ...
		#leave out from 2011-2013, but the last three in the dict should be swapped..
		#with these three for the years 2014-the present
		if row[3] == 'P.N.G.' or row[3] == 'U.A.E.' or row[3] == 'H.K.':
			continue
		x = maindict[row[3]]
		normalValue = int(row[1])/topValue
		if x[1] < 8:
			x[0] += normalValue
			x[1] += 1


print(maindict)
print('\n')
biggestValue = 0
for entries in maindict:
	x = maindict[entries][0]
	if x > biggestValue:
		biggestValue = x

for entries in maindict:
	maindict[entries] = maindict[entries][0]/biggestValue

print(maindict)



