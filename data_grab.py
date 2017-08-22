########################################################################
# in intilization get the data from the website And convert it into 
# the table that I can work with. Then build a function that will allow 
# me to isolate individual groupings of data for graphical use.
########################################################################

import requests
from bs4 import BeautifulSoup

class Data_Grab():
	
	def __init__(self):
		self.webpage = 'https://archive.ics.uci.edu/ml/machine-learning-databases/auto-mpg/auto-mpg.data'
		self.page = requests.get(self.webpage)
		self.rawSoup = BeautifulSoup(self.page.content, 'html.parser')
		
########################################################################
# Time to process the soup by stiching all the necessary values together
# and getting rid of anything that at the time won't be useful. 
# I should stress that the name's of the cars may be useful but 
# as a first (and second) pass I'm not going to try and create a filter
# for the various car names. 
########################################################################

		self.soupProcess = []
		valAllow = ['0','1','2','3','4','5','6','7','8','9','.','?']
		placeHold = 0
		stitch = ""
		exception = 0
		
		while placeHold < 30275:
			for mark in self.rawSoup:
				
########################################################################
# this line will be used to get rid of the car name strings. This is 
# done because some of the car names have numbers and periods in them 
# which will screw up my current algorithm.
########################################################################

				if mark[placeHold] == '"':
					exception = exception +1

				if mark[placeHold] in valAllow and exception % 2 == 0:
					stitch = stitch + mark[placeHold]

########################################################################
# line 43-44 is to issolate all of the numbers and convert them into a
# string which will be recorded once the first space mark is hit below.
# an exception was made for the "?" that's in the horse power section 
# which will need to be accounted for at a later date. The exception is 
# being used to keep me out of the car name strings.
########################################################################

				elif ((mark[placeHold] == " " or 
				mark[placeHold] == "	") and mark[placeHold -1] in 
				valAllow and exception % 2 == 0):
					self.soupProcess.append(stitch)
					stitch = ""

########################################################################
# the logic is supposed to be: if (see space or tab) and (the previous
# vallue was allowed) and you're not inside a car name then record the 
# generated string and reset stitch for the next set of numbers. My 
# testing from yesterday showed that this will get rid of the 
# unnecessary lines.
########################################################################
			
			placeHold = placeHold + 1

	def dataOfInterest(self, valueOfInterest):

		self.processedData = []
		placeHold = 0
		
########################################################################
# Here's the idea, I'm going to have this run through each of the rows 
# the way to choose the index will be: 8*placeHold + valueOfInterest.
# As the index cycles through it'll grab the string in soupProcess, 
# check to make sure it's not one of the "?" exceptions in there and 
# convert the value to a float (should it not be "?"). And then kick out
# this list. Those list will be what I will use to develop the various
# graphs.
########################################################################

		while placeHold < 398:
			iterator = 8 * placeHold + valueOfInterest
			if self.soupProcess[iterator] != "?":
				self.processedData.append(float(self.soupProcess[iterator]))
			else:
				self.processedData.append(self.soupProcess[iterator])
			
			placeHold = placeHold + 1
