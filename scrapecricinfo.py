import requests
import lxml.html as lh
import csv

url='http://stats.espncricinfo.com/ci/engine/stats/index.html?class=2;filter=advanced;host=1;host=15;host=19;host=2;host=20;host=25;host=26;host=27;host=29;host=3;host=30;host=4;host=5;host=6;host=7;host=8;host=9;orderby=start;page=2;size=200;spanmax1=01+jan+2014;spanmin1=1+jan+2011;spanval1=span;team=1;team=15;team=19;team=2;team=20;team=25;team=26;team=27;team=29;team=3;team=30;team=4;team=40;team=5;team=6;team=7;team=8;team=9;template=results;type=aggregate;view=results'

page = requests.get(url)

doc = lh.fromstring(page.content)

tr_elements = doc.xpath('//tr')

#deleting first 6 elements
del tr_elements[:6]

#deleting last 5 elements
del tr_elements[-10:]

data_array = [[] for _ in range(len(tr_elements))]

for t in tr_elements[0]:
	name=t.text_content()
	if name == "":
		continue
	print(name)
	data_array[0].append(name)

print(data_array[0])
	
for j in range(1,len(tr_elements)):
	T=tr_elements[j]
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


print(data_array[len(tr_elements)-1])

with open('secondpage11-13.csv','w') as file:
	writer = csv.writer(file)

	for i in range(0,len(tr_elements)):
		writer.writerow(data_array[i])


