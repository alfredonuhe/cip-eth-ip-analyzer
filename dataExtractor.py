import json
import numpy as np
import pandas as pd
from progressBar import *

iteration = 0
totalPayloads = 0

# Stack all elements with the same payloadpath from a JSON
# file.
def gatherJSONData(filePath, payloadPath):
	global totalPayloads
	# Open JSON file containing network data sample.
	with open(filePath) as f:
		# Load sample to Python List object
		d = json.load(f)

		# Set variables needed for later.
		totalPayloads = calcNumOfPayloads(d, totalPayloads)
		payload = getJSONData(d, payloadPath)
		length = len(payload.split(":"))
		narray = np.zeros(length)
		
		# Extract from the JSON file the propietary protocol payload for 
		# each packet, and add it to a data matrix.
		#	printProgressBar (i, len(d) - 1, 'Progress', 'Complete')
		narray = stackPayloads(d, payloadPath, narray)

		# Remove the first row of zeros and store the matrix in a DataFrame.
		narray = narray[1:]
		df = pd.DataFrame(narray)

		return df 

# Scan the JSON file and stack all items accesible by payloadPath
# inside a ndarray.
def stackPayloads(jObj, payloadPath, narray):
	global iteration
	if isinstance(jObj, list):
		for i in range(0, len(jObj)):
			narray = stackPayloads(jObj[i], payloadPath[1:], narray)
	else:
		payload = getJSONData(jObj, payloadPath)
		payload = payload.split(":")
		payload = hexToIntList(payload)	
		narray = np.vstack((narray, payload))
		iteration += 1	
		printProgressBar (iteration, totalPayloads, 'Progress', 'Complete')
	return narray

# Calculate the number of payloads.
def calcNumOfPayloads(jObj, counter):
	aux = jObj
	if isinstance(aux, list):
		for i in range(0, len(aux)):
			counter = calcNumOfPayloads(jObj[i], counter)
	else:
		counter += 1
	return counter 	

# Query the JSON file using an specific path
def getJSONData(jsonObject, path):
	result = jsonObject
	for i in range(0, len(path)):
		result = result[path[i]]
	return result

# Function to transform list with hex values into integer values.
def hexToIntList(hexList):
	for j in range(0, len(hexList)):
		hexList[j] = int(hexList[j], 16)
	
	return hexList

# Main routine
if __name__ == "__main__":
	print("This is the dataExtractor.")