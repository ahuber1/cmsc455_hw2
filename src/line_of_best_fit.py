import csv
import sys
import textwrap

def readFile(fileName):
	times = []
	thrust = []
	f = open(fileName)

	csv_f = csv.reader(f)
	r = 0

	for row in csv_f:
		if len(row) >= 2:
			times.insert(r, float(row[0]))
			thrust.insert(r, float(row[1]))
			r = r + 1

	f.close
	return (times, thrust)

if len(sys.argv) < 3:
	print ''
	print textwrap.fill('The file path of the csv file containing the digitized ' + \
		'thrust curve (the first argument) and the location of the output ' + \
		'file (the second argument) must be provided.', 75)
	print ''
	print 'Try again...'
else:
	print readFile(sys.argv[1])