## Author:  Owen Cocjin
## Version: 0.1
## Date: 2020.11.21
## Description:    Menu entries for FileFind
## Notes:
## Updates:
##  - Made exclude flag args case-insensitive

from ProgMenu.progmenu import EntryArg,EntryFlag

def excludeFunc(e):
	'''Returns a list of filetypes to ignore'''
	return [i.upper() for i in e.split(',')]
def helpFunc():
	print('''filefind.py [-efh]
  Find magic bytes in a file.

  -e; --exclude=<t>: Exclude filetypes.
                     Separate by comma
  -f; --file=<file>:   File to scan
  -h; --help:        Prints this page''')

EntryArg("exclude",['e','x',"exclude","ignore"],excludeFunc,default=[])
EntryArg("file",['f',"file","target"],lambda f:f,strict=True)
EntryFlag("help",['h',"help"],helpFunc)
