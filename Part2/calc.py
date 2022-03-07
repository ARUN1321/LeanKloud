import csv


def Main(l):
    l.sort(key=lambda x: x[1])
    a = l[-1]
    print("Topper in Maths "+a[0])
    l.sort(key=lambda x: x[2])
    a = l[-1]
    print("Topper in Biology "+a[0])
    l.sort(key=lambda x: x[3])
    a = l[-1]
    print("Topper in English "+a[0])
    l.sort(key=lambda x: x[4])
    a = l[-1]
    print("Topper in Physics "+a[0])
    l.sort(key=lambda x: x[5])
    a = l[-1]
    print("Topper in Chemistry "+a[0])
    l.sort(key=lambda x: x[6])
    a = l[-1]
    print("Topper in Hindi "+a[0])
    o = []
    for i in l:
        p = []
        c = int(i[1])+int(i[2])+int(i[3])+int(i[4])+int(i[5])+int(i[6])
        p.append(i[0])
        p.append(c)
        o.append(p)
    o.sort(key=lambda x: x[1])
    c = []
    for i in o:
        c.append(i[0])
    print("Best student in the class are "+c[-1]+", "+c[-2]+", "+c[-3]+".")


l = []
with open('Marks.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    for line in csv_reader:
        l.append(line)
Main(l)

# Big_O notation
# there are two for loops in my algorithum
# so, O(n+n)
# therefore; o(n)
