## Author:  Owen Cocjin
## Version: 0.1
## Date:    2022.04.18
## Description:    Simple way to parse byte data
from FileTypeData.parsing import ParseData,bToI

def parseBytes(target,data:list,process=lambda b:str(b),btoi=True):
	'''Returns a ParseData object.
	target is an fd of a bytes file.
	data is a list of tuples (str key,int byte size,func process).
	If no function is present in the tuple, default to str
	process is a function that is applied to the byte data.
	If btoi is true, convert the byte to an int first'''
	toret=ParseData()

	for d in data:
		read_data=target.read(d[1])
		if btoi:
			read_data=bToI(read_data)

		try:
			toret.addData(d[0],read_data,d[2])
		except IndexError:
			toret.addData(d[0],read_data,process)

	return toret

def gap(size=1):
	'''Return a tuple representing a default value'''
	return ("No value",size)
