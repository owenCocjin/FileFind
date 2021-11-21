## Author:  Owen Cocjin
## Version: 0.1
## Date: 2020.11.21
## Description:    Holds functions related to data parsing
## Notes:
##  - Any parsing function must return a fully formatted string, or None if no data was found.
##  - Parsing functions must also return to their previous seek position before returning
##  - All parsing assumes from start of magic bytes

def genericParser(target,offsets:list,labels:list)->dict:
	'''Returns a dict of {labels:data}.
	offsets is a list of lists: [offset,length]'''
	return None

def zipParse(target):
	'''Returns file name.
	Data is stored in little-endian'''
	#Seek to 0x1a to get name length
	target.seek(0x1a,1)
	readbuff=target.read(2)
	file_name_len=(readbuff[1]<<8)+readbuff[0]
	#Seek to 0x1e to get actual name
	target.seek(2,1)
	file_name=target.read(file_name_len).decode()
	#Return seek
	target.seek((-file_name_len)-0x1e,1)
	if file_name!='':
		return f"    \033[94m[file name]:\033[0m {file_name}"
	return None
