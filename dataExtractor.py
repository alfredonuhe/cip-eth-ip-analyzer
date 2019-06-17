import json, os, time
from random import randint
import numpy as np
import pandas as pd
from progressBar import *

iteration = 0
totalIterations = 0

# Stack all elements with the same payloadpath from a JSON
# file.
def importJSONData(filePath, payloadPath, bitLength, maxPayloads):

	if(bitLength != 1 and bitLength != 4 and bitLength != 8):
		print("Please enter a valid bitLength. Either 1, 4 or 8 bits.")
		exit()

	global totalIterations
	# Open JSON file containing network data sample.
	with open(filePath) as f:
		# Load sample to Python List object
		d = json.load(f)

		# Set variables needed for later.
		totalIterations = min(calcTotalPayloads(d, totalIterations), maxPayloads)
		payload = getJSONData(d, payloadPath)
		payload = payload.replace(":", "")
		narray = np.zeros(int(len(payload)*(4/bitLength)))
		
		# Extract from the JSON file the propietary protocol payload for 
		# each packet, and add it to a data matrix.
		#	printProgressBar (i, len(d) - 1, 'Progress', 'Complete')
		narray = stackPayloads(d, payloadPath, narray, bitLength, maxPayloads)

		# Remove the first row of zeros and store the matrix in a DataFrame.
		narray = narray[1:]
		df = pd.DataFrame(narray)

		return df 

# Scan the JSON file and stack all items accesible by payloadPath
# inside a ndarray.
def stackPayloads(jObj, payloadPath, narray, bitLength, maxPayloads):
	global iteration

	if (iteration == maxPayloads):
		return narray

	if isinstance(jObj, list):
		for i in range(0, len(jObj)):
			narray = stackPayloads(jObj[i], payloadPath[1:], narray, bitLength, maxPayloads)
	else:
		payload = getJSONData(jObj, payloadPath)
		payload = payload.replace(":", "")
		payload = hexToBitLength(payload, bitLength)	
		narray = np.vstack((narray, payload))
		iteration += 1	
		printProgressBar (iteration, totalIterations, 'Progress', 'Complete')
	return narray

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

# Function to transform list with hex values into integer values.
def hexToBitLength(payload, bitLength):
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

	hexS = ""

	for i in range(0, 600):
		num = randint(16,127)
		hexS += hex(num)[2:4]

	print(hexS, " length: ", len(hexS))

	start = time.time()
	hexToBitLength(hexS, 1)
	print(i, ": ", time.time() - start, " seconds.")

	start = time.time()
	hexToBitLength(hexS, 4)
	print(i, ": ", time.time() - start, " seconds.")

	start = time.time()
	hexToBitLength(hexS, 8)
	print(i, ": ", time.time() - start, " seconds.")
	