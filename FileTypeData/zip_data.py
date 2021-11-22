## Author:  Owen Cocjin
## Version: 0.1
## Date: 2020.11.21
## Description:    Holds functions/data related to zip parsing
from FileTypeData.parsing import ParseData,invalid,bToI

def zipParse(target):
	'''Returns file name.
	Data is stored in little-endian'''
	data=ParseData("compression_method","file_name","compression_rate")
	#Seek to get compression method
	target.seek(8,1)
	readbuff=target.read(2)
	data.addData("compression_method",bToI(readbuff,True),zip_comp_method)
	#Seek 0x08 to get comressed size
	target.seek(0x08,1)
	readbuff=target.read(4)
	compressed_size=bToI(readbuff,True)
	readbuff=target.read(4)
	uncompressed_size=bToI(readbuff,True)
	rate=(1-(compressed_size/uncompressed_size))*100
	data.addData("compression_rate",rate,lambda i:f"{i:.2f}")
	#Get file name length
	readbuff=target.read(2)
	file_name_len=bToI(readbuff,True)
	#Seek to 0x1e to get actual name
	target.seek(2,1)
	data.addData("file_name",target.read(file_name_len).decode())
	#Return seek
	target.seek((-file_name_len)-0x1e,1)

	if data!=invalid:
		return f"""    \033[94m[compression]\033[0m: {data["compression_method"]}
    \033[94m[comp rate]\033[0m:   {data["compression_rate"]}%
    \033[94m[file name]\033[0m:   {data["file_name"]}"""
	return None
def zip_comp_method(d):
	'''Returns supl_data_zip[d], or invalid if doesn't exist'''
	try:
		return supl_data_zip[d]
	except KeyError:
		return None

supl_data_zip={0:"No compression",
8:"Deflate"}
