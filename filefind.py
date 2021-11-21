#!/usr/bin/python3
## Author:  Owen Cocjin
## Version: 0.1
## Date: 2020.11.20
## Description:    Find any magic bytes in
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
					print(f"  [{hex(f.tell()-len(mb.magic))}] \033[92m{mb}\033[0m")
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
