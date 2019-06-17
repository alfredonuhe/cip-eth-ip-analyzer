# Code to detect differences between JSON files

import sys, os, time
import json
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from progressBar import *
from dataExtractor import *

def main():
	startTime = time.time()
	dfList = []	
	jsonPath = [0, "_source", "layers", "cipcls", "Command Specific Data", "cip.data"]
	
	if (len(sys.argv) < 3):
			print("Error, two or more file paths must be entered.")
			exit()
	
	paths = sys.argv[1:]
	
	for path in paths:
		if not os.access(path, os.R_OK):
			print("Error, the file path ", path, " isn't accessible.")
			exit()

		print("Opening JSON file at path " + path + " ... ", end = "")

		# Open JSON file containing network data sample.
		with open(path) as f:
			# Load sample to Python List object
			d = json.load(f)
			print("Done.\n")		
			
			# Stack all network payloads from JSON file into a pandas
			# Dataframe.
			print("Storing JSON file data in a pandas DataFrame ... ")
			df = gatherJSONData(path, jsonPath)
			dfList.append(df)
	
	checkDfShapes(dfList)

	shape = dfList[0].shape
	total = calcProgressTotal(dfList)
	iteration = 0
	numDiff = 0

	print("Calculating differences ... ")
	diff = []
	for i in range(0, len(dfList)):
		aux = []
		for j in range(0, len(dfList)):
			if (j <= i):
				diff.append("None")
			else:
				dataf = pd.DataFrame(np.zeros(shape))
				for n in range(0, shape[1]):
					for m in range(0, shape[0]):
						if(dfList[i][n][m] != dfList[j][n][m]): 					
							dataf[n][m] = 1.0
							numDiff += 1
					iteration += 1				
					printProgressBar (iteration, total, 'Progress', 'Complete')	
				diff.append(dataf)

	timeDuration = time.time() - startTime

	print("############ RESULTS ############\n")
	print("Number of files processed:\t",len(dfList))
	print("Number of bytes processed:\t", len(dfList) * shape[0] * shape[1])	
	print("Number of different bytes:\t", numDiff)
	print("Time duration in seconds:\t", round(timeDuration, 2))
	print("\n########## END RESULTS ##########\n")

def checkDfShapes(dfList):
	shape = dfList[0].shape
	for df in dfList:
		if(shape != df.shape):
			print("Error, DataFrames have diferent shapes (", shape, ", ", df.shape, ").")
			exit()

def calcProgressTotal(dfList):
	result = 0
	length = len(dfList) - 1
	for i in range(0, length):
		result += length - i
	return result * dfList[0].shape[1]

# Main function
if __name__ == "__main__":
    main()