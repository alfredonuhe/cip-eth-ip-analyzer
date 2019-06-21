import json, os, sys, time
from random import randint
import numpy as np
import pandas as pd
from progressBar import *
from DataImporter import DataImporter

def main():
	#Initiate process duration timer
	startTime = time.time()
	
	# Verify that an argument has been
	# provided by the user
	if (len(sys.argv) != 2):
			print("Error, A single file must be entered.")
			exit()

	# File path to JSON file
	path = sys.argv[1]
	
	# JSON structure path to desired information. 
	infoPath = [0, "_source", "layers", "cipcls", "Command Specific Data", "cip.data"]

	# Bit length to represent the binary data in the 
	# pandas DataFrame
	bitLength = 8

	# Maximum number of payloads to import
	maxPayloads = 100

	# Num of matrix stats
	windowSize = 10
	
	# Check if window size is valid.
	if (windowSize < 1 or windowSize % 2 != 0 or windowSize >= maxPayloads):
		print("Error, please enter an even positive window size. It must be smaller than the maximum number of payloads.")
		exit()	
	
	# Import payloads from the JSON file
	print("Opening JSON file at path " + path + " ...\n")		
	di = DataImporter(path, infoPath, bitLength, maxPayloads)
	di.init()
	df = di.df
	
	# Create array containing the data statistics
	statArray = np.zeros(windowSize)	
	
	print("Calculating stats ...")
	
	# Payload Numpy array loop to calculate statistics
	for i in range(0, df.shape[0]):
		rowCorr = calculateCorrelation(df, windowSize, i)
		statArray = np.vstack((statArray, rowCorr))
		printProgressBar (i ,df.shape[0] - 1, 'Progress', 'Complete')

	
	# Remove first line of zeros and store the statistics
	# array into a pandas DataFrame
	statArray = statArray[1:, :] 
	result = pd.DataFrame(data = statArray)
	
	# Calculate entire process duration
	timeDuration = time.time() - startTime
	
	# Display results in the terminal
	print("######################## ANALYSIS RESULTS ########################\n")
	print("Calculation time (s):\t\t", round(timeDuration, 2))
	print("Number of items processed:\t", df.shape[0])
	print("Number of " + str(bitLength) + "-bit units:\t\t", df.shape[1])
	print("Bit length:\t\t\t", bitLength)
	print("Correlation window size:\t", windowSize)
	print("\nStats per " + str(bitLength) + "-bit unit:\n\n",result)
	print("\n###################### END ANALYSIS RESULTS ######################\n")

def calculateCorrelation(df, windowSize, index):
	#sIndex = 0 if(index - (windowSize/2) <= 0) else int(index - (windowSize/2))
	#eIndex = df.shape[0] if(index + (windowSize/2) >= df.shape[0]) else int(index + (windowSize/2))

	if(index - (windowSize/2) <= 0):
		sIndex = 0
		eIndex = sIndex + windowSize
	elif(index + (windowSize/2) >= df.shape[0]):
		eIndex = df.shape[0] - 1
		sIndex = eIndex - windowSize
	else:
		sIndex = int(index - (windowSize/2))
		eIndex = int(index + (windowSize/2))

	streak = False
	result = []

	for i in range(sIndex, eIndex):
		aux = 0
		for j in range(0, df.shape[1]):		
			if(df.loc[index, j] == df.loc[i, j]):
				if(streak):			
					aux += 1
				else:
					aux += 1
				streak = True
			else:
				streak = False
		result.append(aux/df.shape[1])
	return result


# Main function
if __name__ == "__main__":
    main()