## Author:  Owen Cocjin
## Version: 0.1
## Date: 2020.11.20
## Description:    Magic bytes of each file type
## Notes:
##  - Might need to add a try/except around MagicBytes.verify() (length exception?)
import parsing

MY_NAME=__file__[__file__.rfind('/')+1:-3]

class MagicBytes():
	def __init__(self,magic,filetype,descr='N/D',trailer=None,parser=None):
		self.magic=magic  #The magic bytes of the file, as a bytes-object
		self.filetype=filetype
		self.descr=descr
		self.parser=parser
		self.trailer=None

	def __str__(self):
		return f"{self.filetype}: {self.descr}"
	def __repr__(self):
		return self.__str__

	def parse(self,target):
		'''Tries to parse the file for specific header info.
		A parser function should only return a string.
		Any formatting and colouring must be done in the parsing function'''
		return self.parser(target)
	def verify(self,target):
		'''Takes a fd and checks if the next n bytes correspond to self.magic'''
		for i in range(len(self.magic)):
			menu=target.read(1)[0]  #Convert to int
			# print(f"[|X:{MY_NAME}:MagicBytes:verify]: {menu} - {self.magic[i]}")
			if menu!=self.magic[i]:
				#Seek back i bytes in the file
				target.seek(-i,1)
				return False
		#No need to seek at the end because there shouldn't exist "nested" magic bytes
		return True

magic_0x50=[
	MagicBytes(b'\x50\x4b\x03\x04',"ZIP","(APK/JAR/KMZ/KWD/ODT/OXPS/SXC/WMZ/XPI/XPS/XPT)",parser=parsing.zipParse)
]
magic_0x7f=[
	MagicBytes(b'\x7f\x45\x4c\x46',"ELF")
]
magic_0x89=[
	MagicBytes(b'\x89\x50\x4e\x47\x0d\x0a\x1a\x0a',"PNG","Portable Network Graphics",trailer=b'\x49\x45\x4e\xae\x42\x60\x82')
]
magic_0xff=[
	MagicBytes(b'\xff\xd8\xff\xdb',"JPEG","Standard File",trailer=b'\xff\xd9'),
	MagicBytes(b'\xff\xd8\xff\xe0',"JPEG","Standard File",trailer=b'\xff\xd9'),
	MagicBytes(b'\xff\xd8\xff\xe1',"JPEG","Standard File w/ exif",trailer=b'\xff\xd9'),
	MagicBytes(b'\xff\xd8\xff\xe2',"JPEG","Canon Camera Image File Format",trailer=b'\xff\xd9'),
	MagicBytes(b'\xff\xd8\xff\xe8',"JPEG","Still Picture Interchange File Format",trailer=b'\xff\xd9')
]

magic_table={
	b'\x50':magic_0x50,
	b'\x7f':magic_0x7f,
	b'\x89':magic_0x89,
	b'\xff':magic_0xff
}
