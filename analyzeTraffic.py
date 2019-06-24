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
	maxPayloads = 1000

	# Num of matrix stats
	numMStats = 5
	
	# Check if file is accessible
	if not os.access(path, os.R_OK):
		print("Error, the file path ", path, " isn't accessible.")
		exit()
	
	# Import payloads from the JSON file
	print("Opening JSON file at path " + path + " ...\n")		
	di = DataImporter(path, infoPath, 1, 2000)
	di.init()
	df = di.df
	
	# Create array containing the data statistics
	statArray = np.zeros(numMStats)	
	
	print("Calculating stats ...")
	
	# Payload Numpy array loop to calculate statistics
	for i in range(0, df.shape[1]):
		auxStats = []
		changeProb = 0
		mean = df.loc[0,i]
		variance = 0
		values = [df.loc[0,i]]

		for j in range(1, df.shape[0]):
			mean += df.loc[j,i]
			variance += abs(df.loc[j - 1,i] - df.loc[j,i])
			if (df.loc[j - 1,i] != df.loc[j,i]): changeProb += 1
			if df.loc[j,i] not in values: values.append(df.loc[j,i])

		auxStats.append([i + 1, mean, variance, changeProb, len(values)])
		statArray = np.vstack((statArray, auxStats))
		statArray[i + 1, 1] = statArray[i + 1, 1] / (df.shape[0])
		statArray[i + 1, 2:4] = np.round(statArray[i + 1, 2:4] / (df.shape[0] - 1), 3) 
		printProgressBar (i, df.shape[1] - 1, 'Progress', 'Complete')
	
	# Remove first line of zeros and store the statistics
	# array into a pandas DataFrame
	statArray = statArray[1:, :] 
	result = pd.DataFrame(columns= [str(bitLength) + "-bit Index", "Mean", "Variance", "Change Prob", "Num of Values"], data = statArray)
	
	# Calculate entire process duration
	timeDuration = time.time() - startTime
	
	# Display results in the terminal
	print("######################## ANALYSIS RESULTS ########################\n")
	print("Calculation time (s):\t\t", round(timeDuration, 2))
	print("Number of items processed:\t", df.shape[0])
	print("Payload bit size:\t\t", df.shape[1] * bitLength)
	print("Number of " + str(bitLength) + "-bit units:\t\t", df.shape[1])
	print("Bit length:\t\t\t", bitLength)
	print("\nStats per " + str(bitLength) + "-bit unit:\n\n",result)
	print("\n###################### END ANALYSIS RESULTS ######################\n")

# Main function
if __name__ == "__main__":
    main()