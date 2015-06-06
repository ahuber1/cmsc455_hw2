import csv
import numpy
import os
import pylab
import sys
import warnings
import textwrap
from numpy import array
from pylab import *

# Reads the text file at a certain path (fileName)
def readFile(fileName):
	times = []
	thrust = []
	f = open(fileName)

	csv_f = csv.reader(f)

	for row in csv_f:
		if len(row) >= 2: # if there are at least two values (time and thrust)
			times.append(float(row[0])) # append the time value in the times list
			thrust.apppend(float(row[1])) # append the thrust value in the thrust list

	f.close
	return (numpy.array(times), numpy.array(thrust))

# A traditional f(x) mathematical function. x is the x value in f(x) and the 
# coefficients are the equation's coefficients (e.g., in y = ax + b, a and b are the 
# coefficients)
def f(x, coefficients):
	degree = coefficients.size - 1.0
	s = 0.0

	for c in coefficients:
		s = s + (c * (x ** degree))
		degree = degree - 1.0

	return s

# Calculates the average of a list of values (values)
def average(values):
	s = 0.0
	n = 0.0

	for v in values:
		s = s + v
		n = n + 1.0

	return s / n

# Calculates the maximum error, average error, and RMS error
#	times - the time values in the thrust curve (in seconds)
#	thrusts - the thrust values in the thrust curve (in newtons)
#	coefficients - the coefficients in the line of best fit equation
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
# ======================================================================================================
# SCRIPT STARTS HERE
# ======================================================================================================
warnings.simplefilter('ignore', numpy.RankWarning) # numpy raises a warning; we will ignore it

# print an error message if not enough command line arguments were provided
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
	# get the command line arguments
	inputFileName = os.path.abspath(sys.argv[1])
	outputFileName = os.path.abspath(sys.argv[2])
	outputDir = os.path.abspath(sys.argv[3])

	# make the output directory (the one that will contain the images of graphs) if it does not exist
	if not os.path.exists(outputDir):
		os.makedirs(outputDir)

	# complete the file path of the output directory by appending a forward slash if already not completed
	if not outputDir.endswith('/'):
		outputDir = outputDir + '/'

	times, thrust = readFile(inputFileName) # read the csv file
	startDegree = 3 # the lowest degree that we will use
	endDegree = 17 # the highest degree that we will use
	outputFile = open(outputFileName, 'w') # open the output text file; 
										   # create it if necessary; 
										   # overwrite if necessary

	for degree in range(startDegree, endDegree + 1):
		p = np.array(numpy.polyfit(times, thrust, degree)) # calculate line of best fit

		# make plot
		pylab.plot(times, thrust, 'bo')
		pylab.xlabel('Times (in seconds)')
		pylab.ylabel('Thrust (in newtons)')
		pylab.grid(True)
		pylab.title('Thrust Data: Degree = {0:2d}'.format(degree))
		pylab.plot(times, polyval(p, times), 'g')

		filePath = outputDir + 'polyfit_degree_' + str(degree); # make file path of image
		pylab.savefig(filePath) # save image
		pylab.close() # close current figure so a new one can be made

		maxErr, avgErr, rmsErr = calculateError(times, thrust, p) # calculate the errors

		# write results to output file
		outputFile.write('degree = {0:2d}: maxError = {1:.2f}\n'.format(degree, maxErr)) 
		outputFile.write('degree = {0:2d}: avgError = {1:.2f}\n'.format(degree, avgErr))
		outputFile.write('degree = {0:2d}: rmsError = {1:.2f}\n\n'.format(degree, rmsErr))

		# calculate current progress of program execution
		progress = ((degree - startDegree + 0.0) / (endDegree - startDegree)) * 100 
		print '{0:.2f}% complete...'.format(progress) # print progress

	outputFile.close # close the output file
	print 'Done!'