import json, os, time
from random import randint
import numpy as np
import pandas as pd
from progressBar import *

iteration = 0
totalIterations = 0

# Stack all elements with the same jsonPath from a JSON
# file.
def importJSONData(filePath, jsonPath, bitLength = 1, maxPayloads = 100):

	# Check if file is valid.
	if not os.access(path, os.R_OK):
		print("Error: the file path ", path, " isn't accessible.")
		exit()
	
	# Check if the json path is valid.
	try:
		checkJSONPath(filePath, jsonPath)
	except KeyError:
		print("Error: the path '", jsonPath,"' is invalid. Please revise the json path for errors." )
		exit()

	# Check if bitLength is valid.
	if(bitLength != 1 and bitLength != 4 and bitLength != 8):
		print("Please enter a valid bitLength. Either 1, 4 or 8 bits.")
		exit()

	global totalIterations

	print("Storing JSON file data in a pandas DataFrame ... ")
	# Open JSON file containing network data sample.
	with open(filePath) as f:
		# Load sample to Python List object
		d = json.load(f)

		# Set variables needed for later.
		maxPayloadSize = calcMaxPayloadSize(d, jsonPath, bitLength)
		totalIterations = min(calcTotalPayloads(d, totalIterations), maxPayloads)
		payload = getJSONData(d, jsonPath)
		payload = payload.replace(":", "")
		narray = np.zeros(maxPayloadSize)
		
		# Extract from the JSON file the propietary protocol payload for 
		# each packet, and add it to a data matrix.
		#	printProgressBar (i, len(d) - 1, 'Progress', 'Complete')
		narray = stackPayloads(d, jsonPath, bitLength, maxPayloads, maxPayloadSize, narray)

		# Remove the first row of zeros and store the matrix in a DataFrame.
		narray = narray[1:]
		df = pd.DataFrame(narray)

		return df

# Calculate the maximum paylaod size to fill smaller payloads
# with null values at the end.
def calcMaxPayloadSize(jObj, jsonPath, bitLength, result = 0):
	if isinstance(jObj, list):
		for i in range(0, len(jObj)):
			result = calcMaxPayloadSize(jObj[i], jsonPath[1:], bitLength, result)
	else:
		payload = getJSONData(jObj, jsonPath)
		payload = payload.replace(":", "")
		payloadSize = int(len(payload) * (4 / bitLength))
		if result < payloadSize: result = payloadSize
	return result

# Calculate the number of payloads.
def calcTotalPayloads(jObj, counter):
	aux = jObj
	if isinstance(aux, list):
		for i in range(0, len(aux)):
			counter = calcTotalPayloads(jObj[i], counter)
	else:
		counter += 1

	return counter

# Query the JSON file using an specific path
def getJSONData(jsonObject, path):
	result = jsonObject
	for i in range(0, len(path)):
		result = result[path[i]]
	return result

# Function to check if JSON path is valid
def checkJSONPath(filePath, jsonPath):
	with open(filePath) as f:
		# Load sample to Python List object
		d = json.load(f)
		for i in range(0, len(jsonPath)):
			d = d[jsonPath[i]]

# Scan the JSON file and stack all items accesible by jsonPath
# inside a ndarray.
def stackPayloads(jObj, jsonPath, bitLength, maxPayloads, maxPayloadSize, narray):
	global iteration

	if (iteration == maxPayloads):
		return narray

	if isinstance(jObj, list):
		for i in range(0, len(jObj)):
			narray = stackPayloads(jObj[i], jsonPath[1:], bitLength, maxPayloads, maxPayloadSize, narray)
	else:
		payload = getJSONData(jObj, jsonPath)
		payload = payload.replace(":", "")
		payload = hexToBitLength(payload, bitLength, maxPayloadSize)
		narray = np.vstack((narray, payload))
		iteration += 1	
		printProgressBar (iteration, totalIterations, 'Progress', 'Complete')
	return narray

# Function to transform list with hex values into integer values.
def hexToBitLength(payload, bitLength, maxPayloadSize):
	result = []
	
	if (bitLength == 1):
		result = hextoBits(payload)
	elif (bitLength == 4):
		for j in range(0, len(payload)):
			result.append(int(payload[j], 16))
	elif (bitLength == 8):
		if(len(payload)%2 != 0):
			print("Error, hex values aren't even. 8 bit length string can't be calculated")
	
		for j in range(0, int(len(payload)/2)):
			index = j*2
			result.append(int(payload[index:index + 2], 16))
	else:
		print("Error invalid bitLength")
		exit()

	for i in range(len(result), maxPayloadSize):
		result.append(None)
	
	return result

def hextoBits(hexString):
	result = []
	
	for i in range(0, len(hexString)):
		if (hexString[i] == "0"):
			result.extend((0,0,0,0))
		elif (hexString[i] == "1"):
			result.extend((0,0,0,1))
		elif (hexString[i] == "2"):
			result.extend((0,0,1,0))
		elif (hexString[i] == "3"):
			result.extend((0,0,1,1))
		elif (hexString[i] == "4"):
			result.extend((0,1,0,0))
		elif (hexString[i] == "5"):
			result.extend((0,1,0,1))
		elif (hexString[i] == "6"):
			result.extend((0,1,1,0))
		elif (hexString[i] == "7"):
			result.extend((0,1,1,1))
		elif (hexString[i] == "8"):
			result.extend((1,0,0,0))
		elif (hexString[i] == "9"):
			result.extend((1,0,0,1))
		elif (hexString[i] == "a"):
			result.extend((1,0,1,0))
		elif (hexString[i] == "b"):
			result.extend((1,0,1,1))
		elif (hexString[i] == "c"):
			result.extend((1,1,0,0))
		elif (hexString[i] == "d"):
			result.extend((1,1,0,1))
		elif (hexString[i] == "e"):
			result.extend((1,1,1,0))
		elif (hexString[i] == "f"):
			result.extend((1,1,1,1))
		else:
			print("Error invalid hex character: ", hexString[i])
			exit()
	
	return result

# Main routine
if __name__ == "__main__":
	print("This file is dataExtractor.py")
	
	# File path to JSON file
	path = "./Process2PCData/Process2PC.json"
	
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
	df = importJSONData(path, infoPath, bitLength, maxPayloads)

	print(df)