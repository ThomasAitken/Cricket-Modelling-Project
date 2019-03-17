import requests
import lxml.html as lh
import csv

url='[insert Statsguru url here]'

page = requests.get(url)

doc = lh.fromstring(page.content)

tr_elements = doc.xpath('//tr')

#deleting first few elements, because there are table row elements (with '//tr' signature in html) above the table per se. 
#how many elements you need to delete actually depends on what you searched on Statsguru, unfortunately.. tinkering necessary
del tr_elements[:6]

#deleting last 5 elements. same caveat applies as above
del tr_elements[-10:]

data_array = [[] for _ in range(len(tr_elements))]

#checking what's what with row 1
for t in tr_elements[0]:
	name=t.text_content()
	if name == "":
		continue
	data_array[0].append(name)

#and this should print the column headings in one line. if so, you're in business!	
print(data_array[0])
	
for j in range(1,len(tr_elements)):
	T=tr_elements[j]
	#don't care about abandoned or no-result games
	if T[1].text_content() in ['aban','n/r']:
		continue
	i=0

	for t in T.iterchildren():
		data=t.text_content()
		if i != 3:
			if data == "":
				continue
		data_array[j].append(data)
		i+=1

#this prints the last row of the table. sanity check
print(data_array[len(tr_elements)-1])

with open('[insert cute .csv filename here]','w') as file:
	writer = csv.writer(file)

	for i in range(0,len(tr_elements)):
		writer.writerow(data_array[i])


