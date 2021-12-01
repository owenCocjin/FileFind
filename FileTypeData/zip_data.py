## Author:  Owen Cocjin
## Version: 1.0
## Date: 2020.12.01
## Description:    Holds functions/data related to zip parsing
## Notes:
##  - All functions that seek MUST return to original seek position
## Updates:
##  - Added EoCD and CD headers parsing

from FileTypeData.parsing import ParseData,invalid,bToI,returnSeek,INFO,SUBINFO

def zipParse(target):
	'''Returns file name.
	Data is stored in little-endian'''
	start=target.tell()
	data=ParseData("compression_method","comp_size","uncomp_size","file_name","compression_rate","extra_fields")
	#Seek to get compression method
	target.seek(8,1)
	readbuff=target.read(2)
	data.addData("compression_method",bToI(readbuff,True),zip_comp_method)
	#Seek 0x08 to get comressed size
	target.seek(8,1)
	compressed_size=bToI(target.read(4),True)
	data.addData("comp_size",compressed_size,int)
	uncompressed_size=bToI(target.read(4),True)
	data.addData("uncomp_size",uncompressed_size,int)
	rate=(1-(compressed_size/uncompressed_size))*100
	data.addData("compression_rate",rate,lambda i:f"{i:.2f}")
	#Get file name length
	file_name_len=bToI(target.read(2),True)
	extra_field_len=bToI(target.read(2),True)
	data.addData("file_name",target.read(file_name_len).decode())
	#Get extra data if any exists
	if extra_field_len>0:
		#Parse through fields and save them
		data.addData("extra_fields",zipParseExtraFields(target,extra_field_len),list)
	#Return seek
	returnSeek(start,target)

	if data!=invalid:
		toret=f"""{INFO("compression")}:  {data["compression_method"]}
{INFO("comp rate")}:    {data["uncomp_size"]} -> {data["comp_size"]} ({data["compression_rate"]}%)
{INFO("file name")}:    {data["file_name"]}"""
		if len(data["extra_fields"])==0:
			return toret
		toret+=f"\n{INFO('extra fields')}: "
		for f in data["extra_fields"]:
			toret+=f"""\n{SUBINFO(f[0])}: {f[1]}"""
		return toret
	return None
def zip_comp_method(d):
	'''Returns supl_data_zip[d], or invalid if doesn't exist'''
	try:
		return supl_data_zip[d]
	except KeyError:
		return None
def zipCDParse(target):
	'''Returns Central Directory data of a zip file'''
	start=target.tell()
	data=ParseData("compressed_size","uncompressed_size","file_name_len","file_name","relative_offset")
	#Seek to compressed size
	target.seek(28,1)
	data.addData("file_name_len",target.read(2)[::-1],bToI)
	#Seek to relative offset
	target.seek(12,1)
	data.addData("relative_offset",target.read(4)[::-1],bToI)
	data.addData("file_name",target.read(data["file_name_len"]).decode())
	#Return seek
	returnSeek(start,target)
	return f"""{INFO("name")}:         {data["file_name"]}
{INFO("start offset")}: {data["relative_offset"]} ({hex(data["relative_offset"])})"""
def zipEOCDParse(target):
	'''Returns End of Central Directory data of a zip file'''
	start=target.tell()
	data=ParseData("no_records","dir_size","dir_offset")
	#Seek to get entries
	target.seek(10,1)
	data.addData("no_records",target.read(2)[::-1],bToI)
	data.addData("dir_size",target.read(4)[::-1],bToI)
	data.addData("dir_offset",target.read(4)[::-1],bToI)
	returnSeek(start,target)
	return f"""{INFO("records")}: {data["no_records"]}
{INFO("size")}:    {data["dir_size"]} ({hex(data["dir_size"])})
{INFO("offset")}:  {data["dir_offset"]} ({hex(data["dir_offset"])})"""
def zipParseExtraFields(target,length):
	'''Returns a list of extra fields and their data'''
	#0xaabb -> signature (in extra_data_field dict)
	#0xccdd -> data length
	toret=[]
	#Get field info
	sig=bToI(target.read(2))  #Keep little endian, the extra_data_field dict is little end
	length=bToI(target.read(2),True)
	if not length or not sig:  #Neither should be 0
		toret.append("Bad Field",None)
		return toret
	#Get the rest of the data
	data=target.read(length)
	#Add data to toret
	try:
		toret.append((extra_data_field[sig],data))
	except KeyError:
		toret.append((f"Unknown Field: {sig}",data))
	return toret

supl_data_zip={0:"No compression",
1:"Shrunk",
2:"Reduced w/ comp factor 1",
3:"Reduced w/ comp factor 2",
4:"Reduced w/ comp factor 3",
5:"Reduced w/ comp factor 4",
6:"Imploded",
8:"Deflate"}

#This dict's keys are in little endian
extra_data_field={0x0001:"ZIP64 Extended Info",
0x0007:"AV Info",
0x0009:"OS/2 (Info-ZIP)",
0x000a:"NTFS (Win9x/WinNT FileTimes)",
0x000c:"OpenVMS",
0x000d:"Unix",
0x000f:"Patch Descriptor",
0x0014:"PKCS#7 Store for x.509 Certs",
0x0015:"X.509 Cert ID & Signature for Individual File",
0x0016:"X.509 Cert ID for Central Directory",
0x5554:"Extended Timestamp",
0x7855:"Info-ZIP Unix"}
#https://fossies.org/linux/zip/proginfo/extrafld.txt
#This link has a list of extra field signatures
