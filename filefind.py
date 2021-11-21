#!/usr/bin/python3
## Author:  Owen Cocjin
## Version: 0.1
## Date: 2020.11.20
## Description:    Find any magic bytes in a given file
import magicdata

from ProgMenu.progmenu import MENU
import menuentries

PARSER=MENU.parse(True,strict=True)
vprint=MENU.verboseSetup(['v'])

MY_NAME=__file__[__file__.rfind('/')+1:-3]

def main():
	#Open file
	try:
		f=open(PARSER["file"],'rb')
	except FileNotFoundError:
		print(f"[|X:{MY_NAME}]: Can't find file: {PARSER['file']}")
		exit(1)

	#Start reading each byte and check if the byte is in magicdata
	print(f"[|X:{MY_NAME}]: Starting search...")
	if PARSER["exclude"]!=[]:
		print(f"[|X:{MY_NAME}]: Ignoring: {PARSER['exclude']}")
	while True:
		cur_byte=f.read(1)
		# print(f"[|X:{MY_NAME}]: Checking {cur_byte}({f.tell()})")
		if cur_byte==b'':  #EOF
			break
		try:
			for mb in magicdata.magic_table[cur_byte]:
				# print(f"[|X:{MY_NAME}]: Testing {mb.filetype}({mb.magic})")
				#Verify each magic bytes
				f.seek(-1,1)  #Include cur_byte
				if mb.verify(f) and mb.filetype not in PARSER["exclude"]:  #Print data
					length=len(mb.magic)
					print(f"  [{hex(f.tell()-length)}] \033[92m{mb}\033[0m")
					#Try to parse, if one exists
					if mb.parser!=None:
						#Seek back by length of magic bytes
						f.seek(-length,1)
						parse_return=mb.parser(f)
						if parse_return!=None:
							print(parse_return)
						#Seek one as if moving past the initally read byte
						f.seek(1,1)
					break
		except KeyError:  #Byte isn't in table
			continue

	print("\033[42m    Done!    \033[0m")
	f.close()


if __name__=="__main__":
	try:
		main()
	except KeyboardInterrupt:
		print('\r\033[K',end='')
