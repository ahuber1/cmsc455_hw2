import csv
import numpy
import os
import pylab
import sys
import warnings
import textwrap
from numpy import array
from pylab import *

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

def f(x, coefficients):
	degree = coefficients.size - 1.0
	s = 0.0

	for c in coefficients:
		s = s + (c * (x ** degree))
		degree = degree - 1.0

	return s

def average(values):
	s = 0.0
	n = 0.0

	for v in values:
		s = s + v
		n = n + 1.0

	return s / n

def calculateError(times, thrusts, coefficients):
	errors = []
	squareErrors = []
	maxErr = 0.0
	length = times.size

	for i in range(0, length):
		err = f(times[i], coefficients) - thrusts[i]
		errors.append(err)
		squareErrors.append(err ** 2)

		if err > maxErr:
			maxErr = err

	avgErr = average(errors)
	rmsErr = average(squareErrors) ** 0.5

	if maxErr != 0:
		maxErr = abs(maxErr)
	if avgErr != 0:
		avgErr = abs(avgErr)
	if rmsErr != 0:
		rmsErr = abs(rmsErr)

	return maxErr, avgErr, rmsErr

warnings.simplefilter('ignore', numpy.RankWarning)

if len(sys.argv) < 4:
	print ''
	print 'The following three command line arguments must be provided:'
	print ''
	print '1. The file path of the csv file containing the digitized thrust curve'
	print '2. The file path of the output file'
	print '3. The path to a directory where the images of the ploys will be'
	print '   created and stored'
	print ''
	print 'Try again...'
else:
	inputFileName = os.path.abspath(sys.argv[1])
	outputFileName = os.path.abspath(sys.argv[2])
	outputDir = os.path.abspath(sys.argv[3])

	if not os.path.exists(outputDir):
		os.makedirs(outputDir)
	if not outputDir.endswith('/'):
		outputDir = outputDir + '/'

	times, thrust = readFile(inputFileName)
	startDegree = 3
	endDegree = 17
	outputFile = open(outputFileName, 'w')

	for degree in range(startDegree, endDegree + 1):
		p = np.array(numpy.polyfit(times, thrust, degree))
		pylab.plot(times, thrust, 'bo')
		pylab.xlabel('Times (in seconds)')
		pylab.ylabel('Thrust (in newtons)')
		pylab.grid(True)
		pylab.title('Thrust Data: Degree = {0:2d}'.format(degree))
		pylab.plot(times, polyval(p, times), 'g')
		filePath = outputDir + 'polyfit_degree_' + str(degree);
		pylab.savefig(filePath)
		pylab.close()

		maxErr, avgErr, rmsErr = calculateError(times, thrust, p)
		outputFile.write('degree = {0:2d}: maxError = {1:.2f}\n'.format(degree, maxErr))
		outputFile.write('degree = {0:2d}: avgError = {1:.2f}\n'.format(degree, avgErr))
		outputFile.write('degree = {0:2d}: rmsError = {1:.2f}\n\n'.format(degree, rmsErr))

		progress = ((degree - startDegree + 0.0) / (endDegree - startDegree)) * 100
		print '{0:.2f}% complete...'.format(progress)

	print 'Done!'
