import os
import time
import json
from random import randint
import numpy as np
import pandas as pd
from progressBar import *

class DataImporter:
	fileP = None
	jsonP = None
	bitL = None
	maxP = None
	maxPS = None
	jOb = None
	df = None
	nArray = None
	totalIter = 0
	currentIter = 0

	def __init__(self, filepath, jsonPath, bitLength = 1, maxPayloads = 100):
		# Check if file is valid.
		if not os.access(filepath, os.R_OK):
			print("Error: the file path ", filepath, " isn't accessible.")
			exit()
		
		# Check if the json path is valid.
		if not self.isJSONPathValid(filepath, jsonPath):
			print("Error, the json path '", jsonPath, "' is invalid. Please revise for errors.")
			exit()

		# Check if bitLength is valid.
		if(bitLength != 1 and bitLength != 4 and bitLength != 8):
			print("Please enter a valid bitLength. Either 1, 4 or 8 bits.")
			exit()

		# Check if maxPayloads is valid.
		if(type(maxPayloads) is not int or maxPayloads < 0):
			print("Please enter a valid integer as maximum of payloads. It must be a positive value.")
			exit()

		self.fileP = filepath
		self.jsonP = jsonPath
		self.bitL = bitLength
		self.maxP = maxPayloads

	def init(self):
		print("Storing JSON file data in a pandas DataFrame ... ")
		# Open JSON file containing network data sample.
		with open(self.fileP) as f:
			# Load sample to Python List object
			self.jOb = json.load(f)

			# Set variables needed for later.
			self.maxPS = self.calcMaxPayloadSize(self.jOb, self.jsonP)
			self.totalIter = min(self.calcTotalPayloads(self.jOb), self.maxP)
			payload = self.getJSONData(self.jOb, self.jsonP)
			payload = payload.replace(":", "")
			narray = np.zeros(self.maxPS)
			
			# Extract from the JSON file the propietary protocol payload for 
			# each packet, and add it to a data matrix.
			#	printProgressBar (i, len(d) - 1, 'Progress', 'Complete')
			narray = self.stackPayloads(self.jOb, self.jsonP, narray)

			# Remove the first row of zeros and store the matrix in a DataFrame.
			narray = narray[1:]
			self.df = pd.DataFrame(narray)

	# Calculate the maximum paylaod size to fill smaller payloads
	# with null values at the end.
	def calcMaxPayloadSize(self, jOb, jsonP, result = 0):
		if isinstance(jOb, list):
			for i in range(0, len(jOb)):
				result = self.calcMaxPayloadSize(jOb[i], jsonP[1:], result)
		else:
			payload = self.getJSONData(jOb, jsonP)
			payload = payload.replace(":", "")
			payloadSize = int(len(payload) * (4 / self.bitL))
			if result < payloadSize: result = payloadSize
		return result

	# Calculate the number of payloads.
	def calcTotalPayloads(self, jOb, counter = 0):
		if isinstance(jOb, list):
			for i in range(0, len(jOb)):
				counter = self.calcTotalPayloads(jOb[i], counter)
		else:
			counter += 1
		return counter

	# Query the JSON file using an specific path
	def getJSONData(self, jOb, jsonP):
		result = jOb
		for i in range(0, len(jsonP)):
			result = result[jsonP[i]]
		return result

	# Function to check if JSON path is valid
	def isJSONPathValid(self, fileP, jsonP):
		with open(fileP) as f:
			# Load sample to Python List object
			jOb = json.load(f)
			for i in range(0, len(jsonP)):
				try:
					jOb = jOb[jsonP[i]]
				except:
					return False
			return True			

	# Scan the JSON file and stack all items accesible by jsonPath
	# inside a ndarray.
	def stackPayloads(self, jOb, jsonP, narray):
		if (self.currentIter == self.maxP):
			return narray

		if isinstance(jOb, list):
			for i in range(0, len(jOb)):
				narray = self.stackPayloads(jOb[i], jsonP[1:], narray)
		else:
			payload = self.getJSONData(jOb, jsonP)
			payload = payload.replace(":", "")
			payload = self.convertHexToBitLength(payload)
			narray = np.vstack((narray, payload))
			self.currentIter += 1	
			printProgressBar (self.currentIter, self.totalIter, 'Progress', 'Complete')
		return narray

	# Function to transform list with hex values into integer values.
	def convertHexToBitLength(self, payload):
		result = []
		
		if (self.bitL == 1):
			result = self.convertHextoBits(payload)
		elif (self.bitL == 4):
			for j in range(0, len(payload)):
				result.append(int(payload[j], 16))
		elif (self.bitL == 8):
			if(len(payload)%2 != 0):
				print("Error, hex values aren't even. 8 bit length string can't be calculated")
				exit()
		
			for j in range(0, int(len(payload)/2)):
				index = j*2
				result.append(int(payload[index:index + 2], 16))
		else:
			print("Error invalid bitLength")
			exit()

		for i in range(len(result), self.maxPS):
			result.append(None)
		
		return result
	
	# Convert a hexadecimal string to an integer bits list
	def convertHextoBits(self, hexString):
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

""" Main routine
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
	maxPayloads = 2000

	# Num of matrix stats
	numMStats = 5
	
	# Check if file is accessible
	if not os.access(path, os.R_OK):
		print("Error, the file path ", path, " isn't accessible.")
		exit()
	
	# Import payloads from the JSON file
	print("Opening JSON file at path " + path + " ...\n")		
	di = DataImporter(path, infoPath, bitLength, maxPayloads)
	di.initiate()
	print(di.df)
"""		