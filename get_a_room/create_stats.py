from random import randint
import sys

lines = open(sys.argv[1]).read().split('\n')

for line in lines:
	print line
	numPeople = int(line.split(' ')[2])
	new = randint(-5,5) + numPeople
	if new < 0:
		new = randint(0,10)
	print line.split()[0] + ' ' + line.split()[1] + ' ' + str(new)