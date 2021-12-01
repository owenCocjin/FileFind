## Author:  Owen Cocjin
## Version: 1.0
## Date: 2020.12.01
## Description:    Holds functions/data related to zip parsing
## Notes:
## Updates:
##  - Added EoCD and CD headers parsing

from FileTypeData.parsing import ParseData,invalid,bToI,INFO,SUBINFO

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
		return f"""{INFO("compression")}: {data["compression_method"]}
{INFO("comp rate")}\033[0m:   {data["compression_rate"]}%
{INFO("file name")}\033[0m:   {data["file_name"]}"""
	return None
def zip_comp_method(d):
	'''Returns supl_data_zip[d], or invalid if doesn't exist'''
	try:
		return supl_data_zip[d]
	except KeyError:
		return None
def zipCDParse(target):
	'''Returns Central Directory data of a zip file'''
	data=ParseData("compressed_size","uncompressed_size","file_name_len","file_name","relative_offset")
	#Seek to compressed size
	target.seek(28,1)
	data.addData("file_name_len",target.read(2)[::-1],bToI)
	#Seek to relative offset
	target.seek(12,1)
	data.addData("relative_offset",target.read(4)[::-1],bToI)
	data.addData("file_name",target.read(data["file_name_len"]).decode())
	return f"""{INFO("name")}:         {data["file_name"]}
{INFO("start offset")}: {data["relative_offset"]} ({hex(data["relative_offset"])})"""
def zipEOCDParse(target):
	'''Returns End of Central Directory data of a zip file'''
	data=ParseData("no_records","dir_size","dir_offset")
	#Seek to get entries
	target.seek(10,1)
	data.addData("no_records",target.read(2)[::-1],bToI)
	data.addData("dir_size",target.read(4)[::-1],bToI)
	data.addData("dir_offset",target.read(4)[::-1],bToI)
	return f"""{INFO("records")}: {data["no_records"]}
{INFO("size")}:    {data["dir_size"]} ({hex(data["dir_size"])})
{INFO("offset")}:  {data["dir_offset"]} ({hex(data["dir_offset"])})"""

supl_data_zip={0:"No compression",
8:"Deflate"}
