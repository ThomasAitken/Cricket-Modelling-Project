import requests
import lxml.html as lh
from bs4 import BeautifulSoup
import csv

#have to use BeautifulSoup for this one in addition to lxml because of...
#pesky flag images that I needed to convert into country prefixes.. you'll see

url='http://www.relianceiccrankings.com/[insert rest of url here]'

#some kind of heading for the scraped data
print('Top 100 bowlers Jan 2013')

page = requests.get(url)

doc = lh.fromstring(page.content)

#rows of the table
tr_elements = doc.xpath('//tr')

soup = BeautifulSoup(requests.get(url).text, 'lxml')

#ok, this basically creates a strange array that allows me to...
#get each player's country as part of the entry... sorry that it's confusing
special = soup.find_all('td', {'class': 'top100nation'})

data_array = [[] for _ in range(len(tr_elements))]

del tr_elements[0]

i=0
for t in tr_elements[0]:
	if i == 4:
		continue
	name=t.text_content()
	data_array[0].append(name)
	i+=1

#printing out first row of table, to check correctness.. 
#obviously should see the column names
print(data_array[0])
							
for j in range(1,len(tr_elements)):
	T=tr_elements[j]

	i=0

	for t in T.iterchildren():

		#column is not at issue
		if i == 4: 
			continue
		elif i != 3:
			data=t.text_content()
		#image-based column
		else:
			#'special[j-1]['title']' is the address for the national prefix..
			#(that is, 'AUS', 'IND', etc) for the player in question
			data = special[j-1]['title']

		data_array[j].append(data)
		i+=1

#printing last row to check correctness. should see final entry
print(data_array[len(tr_elements)-1])


with open('[insert cute textfile filename here]','w') as file:
	writer = csv.writer(file)

	for i in range(0,len(tr_elements)):
		writer.writerow(data_array[i])

