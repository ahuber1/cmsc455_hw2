import csv
import sys

def readFile(fileName):
	values=[][]
	with open (fileName, 'rb') as csvFile:
		reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
		for row in reader:
			rowHalves=row.split(sep=',', maxsplit=1)
			rowValues=[]
			for half in rowHalves:
				rowValues.append(float(half))
			values.append(rowValues)
	return values

