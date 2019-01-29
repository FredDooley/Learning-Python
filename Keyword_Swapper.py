import csv

with open('Santee-Surrounding-Cities.csv','w',newline = '') as f:
    thewriter = csv.writer(f)

file = input('Please enter raw.csv: ')
opened = open(file)

file2 = input('Please enter new.txt: ')
opened2 = open(file2)

s = str()
old = ['san diego','santee','del mar','carlsbad','san marcos','encinitas','pendleton']
new = list()
x = list()

#Creating List of New Cities that will replace old cities
for line in opened2:
    new.append(line.rstrip())

#Creating File where completed date will be printed to
with open('Santee-Surrounding-Cities.csv','w',newline = '') as f:
    thewriter = csv.writer(f)

    thewriter.writerow(['Keyword','Ad Group'])

    for line in opened:
        x = line.split(',')
        s = x[1]
        count = 0



        for old_city in old:
            count = count + 1
            if old_city in s:
                for new_city in new:
                    thewriter.writerow([s.replace(old_city, new_city),x[2]])
                    count = count + 1
                #if old_city is old[0] or old[1]:
                #    thewriter.writerow([s,x[2]])
            elif count is 7:
                    thewriter.writerow([s,x[2]])
            else:
                continue
