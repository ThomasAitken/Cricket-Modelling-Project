import requests
import lxml.html as lh
from bs4 import BeautifulSoup
import csv

url='http://www.relianceiccrankings.com/datespecific/odi/?stattype=bowling&day=01&month=10&year=2013'

print('10-12 2013')

page = requests.get(url)

doc = lh.fromstring(page.content)

#rows of the table
tr_elements = doc.xpath('//tr')

soup = BeautifulSoup(requests.get(url).text, 'lxml')

special = soup.find_all('td', {'class': 'top100nation'})

data_array = [[] for _ in range(len(tr_elements))]

del tr_elements[0]

i=0
for t in tr_elements[0]:
	if i == 4:
		continue
	name=t.text_content()
	print(name)
	data_array[0].append(name)
	i+=1

#printing out first row of table, to check correctness
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
			data = special[j-1]['title']

		data_array[j].append(data)
		i+=1

#printing last row to check correctness
print(data_array[len(tr_elements)-1])


with open('list3,13','w') as file:
	writer = csv.writer(file)

	for i in range(0,len(tr_elements)):
		writer.writerow(data_array[i])

