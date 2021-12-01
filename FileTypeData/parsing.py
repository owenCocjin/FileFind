## Author:  Owen Cocjin
## Version: 1.0
## Date: 2020.12.01
## Description:    Holds functions related to data parsing
## Notes:
##  - Any parsing function must return a fully formatted string, or None if no data was found.
##  - Parsing functions must also return to their previous seek position before returning
##  - All parsing assumes from start of magic bytes
## Updates:
##  - Added print formatting

def INFO(s):
	'''Returns a string wrapped in INFO-style edits'''
	return f"    \033[94m[{s}]\033[0m"
def SUBINFO(s):
	'''Returns a string wrapped in SUBINFO-style edits'''
	return f"      \033[94m[{s}]\033[0m"
def NAME(s):
	'''Returns a string wrapped in NAME-style edits'''
	return f"\033[92m{s}\033[0m"
def SUBSET(s):
	'''Returns a string wrapped in SUBSET-style edits'''
	return f"\033[93m{s}\033[0m"

class ParseData():
	def __init__(self,*args):
		self.data={}
		for a in args:
			self.data[a]=invalid
	def __getitem__(self,key):
		return self.data[key]
	def __eq__(self,other):
		'''Returns True if any items are equal to other'''
		return any([self.data[a]==other for a in self.data])
	def __ne__(self,other):
		'''Returns True if all items aren't equal to other.
		Good for finding any "invalid" items'''
		return all([self.data[a]!=other for a in self.data])

	def addData(self,ref,new,data_type=str):
		'''Tries to add the passed data to the data dict as the specified type.
		Default type is str.
		Returns None if the type didn't work or if the data type returns None, returns the new data otherwise'''
		try:
			temp_data=data_type(new)
			if temp_data!=None:
				self.data[ref]=temp_data
		except ValueError:
			return None
		return self.data[ref]

def bToI(b,endian=False):
	'''Returns an int.
	If endian is True (little endian), invert the bytes first'''
	if endian:
		b=b[::-1]
	toret=0
	for i in b:
		toret=(toret<<8)+i
	return toret

invalid="\033[91mUnknown\033[0m"


if __name__=="__main__":
	data=ParseData("a","b")
	print(data["a"])
	print(data.addData("a",'c',int))
	print(data["a"])
	print(data.addData("a",1,int))
