import csv
import numpy
from numpy import array
import sys
import warnings
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
	return (numpy.array(times), numpy.array(thrust))

warnings.simplefilter('ignore', numpy.RankWarning)

if len(sys.argv) < 3:
	print ''
	print textwrap.fill('The file path of the csv file containing the digitized ' + \
		'thrust curve (the first argument) and the location of the output ' + \
		'file (the second argument) must be provided.', 75)
	print ''
	print 'Try again...'
else:
	inputFileName = sys.argv[1]
	outputFileName = sys.argv[2]
	times, thrust = readFile(inputFileName)


	for degree in range(3, 19):
		lsf = numpy.polyfit(times, thrust, degree)
		